from __future__ import annotations

from typing import TYPE_CHECKING, Any

from githarbor.repositories import create_repository


if TYPE_CHECKING:
    from githarbor.core.base import Repository
    from githarbor.core.models import Branch, Commit, Issue, PullRequest


class GitRepository:
    """High-level repository interface wrapping provider-specific implementations."""

    def __init__(self, url: str, **kwargs: Any) -> None:
        """Initialize repository wrapper.

        Args:
            url: Repository URL
            **kwargs: Provider-specific configuration
        """
        self._repo: Repository = create_repository(url, **kwargs)

    @property
    def name(self) -> str:
        """Repository name."""
        return self._repo.name

    @property
    def default_branch(self) -> str:
        """Default branch name."""
        return self._repo.default_branch

    def get_branch(self, name: str) -> Branch:
        return self._repo.get_branch(name)

    def get_issue(self, number: int) -> Issue:
        return self._repo.get_issue(number)

    def get_latest_commits(self, n: int = 10) -> list[Commit]:
        """Get the n most recent commits."""
        commits = self._repo.list_commits()
        return commits[:n]

    def find_issues_by_label(self, label: str) -> list[Issue]:
        """Find all issues with a specific label."""
        return [
            issue
            for issue in self._repo.list_issues()
            if any(l.name == label for l in issue.labels)
        ]

    def get_active_pull_requests(self) -> list[PullRequest]:
        """Get all open pull requests with recent activity."""
        from datetime import datetime, timedelta

        prs = self._repo.list_pull_requests(state="open")
        week_ago = datetime.now() - timedelta(days=7)
        return [pr for pr in prs if pr.updated_at and pr.updated_at > week_ago]


if __name__ == "__main__":
    repo = GitRepository("https://github.com/phil65/mknodes")

    # Basic operations
    branch = repo.get_branch("main")
    issue = repo.get_issue(1)

    # Higher level operations
    recent_commits = repo.get_latest_commits(5)
    bug_issues = repo.find_issues_by_label("bug")
    active_prs = repo.get_active_pull_requests()
