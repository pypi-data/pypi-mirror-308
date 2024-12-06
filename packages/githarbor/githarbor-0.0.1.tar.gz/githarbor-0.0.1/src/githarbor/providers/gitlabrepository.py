from __future__ import annotations

from datetime import datetime
import os
from typing import Any, ClassVar
from urllib.parse import urlparse

import gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabGetError

from githarbor.core.base import Repository
from githarbor.core.models import (
    Branch,
    Commit,
    Issue,
    Label,
    PullRequest,
    User,
    Workflow,
    WorkflowRun,
)
from githarbor.exceptions import AuthenticationError, ResourceNotFoundError


class GitLabRepository(Repository):
    """GitLab repository implementation."""

    url_patterns: ClassVar[list[str]] = ["gitlab.com"]

    def __init__(
        self,
        owner: str,
        name: str,
        token: str | None = None,
        url: str = "https://gitlab.com",
    ):
        try:
            t = token or os.getenv("GITLAB_TOKEN")
            if not t:
                msg = "GitLab token is required"
                raise ValueError(msg)

            self._gl = gitlab.Gitlab(url=url, private_token=t)
            self._gl.auth()
            self._repo = self._gl.projects.get(f"{owner}/{name}")
            self._owner = owner
            self._name = name

        except GitlabAuthenticationError as e:
            msg = f"GitLab authentication failed: {e!s}"
            raise AuthenticationError(msg) from e

    @classmethod
    def from_url(cls, url: str, **kwargs: Any) -> GitLabRepository:
        """Create from URL like 'https://gitlab.com/owner/repo'."""
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:  # noqa: PLR2004
            msg = f"Invalid GitLab URL: {url}"
            raise ValueError(msg)

        return cls(
            owner=parts[0],
            name=parts[1],
            token=kwargs.get("token"),
            url=f"{parsed.scheme}://{parsed.netloc}",
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_branch(self) -> str:
        return self._repo.default_branch

    def get_branch(self, name: str) -> Branch:
        try:
            branch = self._repo.branches.get(name)
            return Branch(
                name=branch.name,
                sha=branch.commit["id"],
                protected=branch.protected,
                created_at=None,  # GitLab doesn't provide branch creation date
                updated_at=None,  # GitLab doesn't provide branch update date
            )
        except GitlabGetError as e:
            msg = f"Branch {name} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def _parse_datetime(self, dt_str: str | None) -> datetime | None:
        """Helper to consistently parse GitLab datetime strings."""
        if not dt_str:
            return None
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_pull_request(self, number: int) -> PullRequest:
        try:
            mr = self._repo.mergerequests.get(number)
            return PullRequest(
                number=mr.iid,
                title=mr.title,
                description=mr.description or "",
                state=mr.state,
                source_branch=mr.source_branch,
                target_branch=mr.target_branch,
                created_at=self._parse_datetime(mr.created_at),
                updated_at=self._parse_datetime(mr.updated_at),
                merged_at=self._parse_datetime(mr.merged_at),
                closed_at=self._parse_datetime(mr.closed_at),
                # ... rest of implementation
            )
        except GitlabGetError as e:
            msg = f"Merge request #{number} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def list_pull_requests(self, state: str = "open") -> list[PullRequest]:
        try:
            mrs = self._repo.mergerequests.list(state=state, all=True)
            return [self.get_pull_request(mr.iid) for mr in mrs]
        except GitlabGetError as e:
            msg = f"Failed to list merge requests: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def get_issue(self, issue_id: int) -> Issue:
        try:
            issue = self._repo.issues.get(issue_id)
            return Issue(
                number=issue.iid,
                title=issue.title,
                description=issue.description or "",
                state=issue.state,
                created_at=datetime.strptime(issue.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                updated_at=datetime.strptime(issue.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                if issue.updated_at
                else None,
                closed_at=datetime.strptime(issue.closed_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                if issue.closed_at
                else None,
                closed=issue.state == "closed",
                author=User(
                    username=issue.author["username"],
                    name=issue.author["name"],
                    avatar_url=issue.author["avatar_url"],
                )
                if issue.author
                else None,
                assignee=User(
                    username=issue.assignee["username"],
                    name=issue.assignee["name"],
                    avatar_url=issue.assignee["avatar_url"],
                )
                if issue.assignee
                else None,
                labels=[Label(name=lbl) for lbl in issue.labels],
            )
        except GitlabGetError as e:
            msg = f"Issue #{issue_id} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def list_issues(self, state: str | None = None) -> list[Issue]:
        if state == "open":
            state = "opened"
        try:
            issues = self._repo.issues.list(state=state, all=True)
            return [self.get_issue(issue.iid) for issue in issues]
        except GitlabGetError as e:
            msg = f"Failed to list issues: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def get_commit(self, sha: str) -> Commit:
        try:
            commit = self._repo.commits.get(sha)
            return Commit(
                sha=commit.id,
                message=commit.message,
                created_at=datetime.strptime(commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                author=User(
                    username=commit.author_name,
                    email=commit.author_email,
                    name=commit.author_name,
                ),
                url=commit.web_url,
            )
        except GitlabGetError as e:
            msg = f"Commit {sha} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def list_commits(
        self,
        branch: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        author: str | None = None,
        path: str | None = None,
        max_results: int | None = None,
    ) -> list[Commit]:
        """List commits for the repository.

        Args:
            branch: Branch to get commits from. Defaults to default branch.
            since: Only commits after this date will be returned
            until: Only commits before this date will be returned
            path: Only commits containing this file path will be returned
            author: Filter commits by author name/email
            max_results: Maximum number of commits to return

        Returns:
            List of Commit objects

        Raises:
            ResourceNotFoundError: If commits cannot be retrieved
        """
        try:
            kwargs: dict[str, Any] = {}
            if branch:
                kwargs["ref_name"] = branch
            if since:
                kwargs["since"] = since.isoformat()
            if until:
                kwargs["until"] = until.isoformat()
            if path:
                kwargs["path"] = path
            if author:
                kwargs["author"] = author
            if max_results:
                kwargs["per_page"] = max_results
                kwargs["page"] = 1
            else:
                kwargs["all"] = True

            commits = self._repo.commits.list(**kwargs)

            # Convert to list to materialize the results
            commits = list(commits)

            return [self.get_commit(c.id) for c in commits]

        except GitlabGetError as e:
            msg = f"Failed to list commits: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def get_workflow(self, workflow_id: str) -> Workflow:
        try:
            pipeline = self._repo.pipelines.get(workflow_id)
            return Workflow(
                id=str(pipeline.id),
                name=pipeline.ref,
                path="",  # GitLab doesn't have workflow paths
                state=pipeline.status,
                created_at=datetime.strptime(
                    pipeline.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                updated_at=None,
            )
        except GitlabGetError as e:
            msg = f"Pipeline {id} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def list_workflows(self) -> list[Workflow]:
        try:
            pipelines = self._repo.pipelines.list()
            return [self.get_workflow(str(p.id)) for p in pipelines]
        except GitlabGetError as e:
            msg = f"Failed to list pipelines: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def get_workflow_run(self, run_id: str) -> WorkflowRun:
        try:
            job = self._repo.jobs.get(run_id)
            return WorkflowRun(
                id=str(job.id),
                name=job.name,
                workflow_id=str(job.pipeline["id"]),
                status=job.status,
                conclusion=job.status,
                branch=job.ref,
                created_at=datetime.strptime(job.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                started_at=datetime.strptime(job.started_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                if job.started_at
                else None,
                completed_at=datetime.strptime(job.finished_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                if job.finished_at
                else None,
            )
        except GitlabGetError as e:
            msg = f"Job {id} not found: {e!s}"
            raise ResourceNotFoundError(msg) from e

    def download(
        self,
        path: str | os.PathLike[str],
        destination: str | os.PathLike[str],
        recursive: bool = False,
    ):
        """Download a file or directory from this GitLab repository.

        Args:
            path: Path to the file or directory we want to download.
            destination: Path where file/directory should be saved.
            recursive: Download all files from a folder (and subfolders).
        """
        import upath

        dest = upath.UPath(destination)
        dest.mkdir(exist_ok=True, parents=True)

        if recursive:
            # For recursive downloads, we need to get all files in the directory
            try:
                items = self._repo.repository_tree(path=str(path), recursive=True)
                for item in items:
                    if item["type"] == "blob":  # Only download files, not directories
                        file_path = item["path"]
                        try:
                            content = self._repo.files.get(
                                file_path=file_path, ref=self.default_branch
                            )
                            # Create subdirectories if needed
                            file_dest = dest / file_path
                            file_dest.parent.mkdir(exist_ok=True, parents=True)
                            # Save the file content
                            file_dest.write_bytes(content.decode())
                        except GitlabGetError:
                            continue
            except GitlabGetError as e:
                msg = f"Failed to download directory {path}: {e!s}"
                raise ResourceNotFoundError(msg) from e
        else:
            # For single file download
            try:
                content = self._repo.files.get(
                    file_path=str(path), ref=self.default_branch
                )
                file_dest = dest / upath.UPath(path).name
                file_dest.write_bytes(content.decode())
            except GitlabGetError as e:
                msg = f"Failed to download file {path}: {e!s}"
                raise ResourceNotFoundError(msg) from e


if __name__ == "__main__":
    repo = GitLabRepository("phil65", "test")
    print(repo.list_issues())
