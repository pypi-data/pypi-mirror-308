

    def create_pull_request(
            self,
            repo_name: str,
            source_branch: str,
            target_branch: str,
            title: str,
            description: str = "",
        ) -> PullRequest:
            try:
                gl_project = self.client.projects.get(repo_name)
                mr = gl_project.mergerequests.create({
                    "source_branch": source_branch,
                    "target_branch": target_branch,
                    "title": title,
                    "description": description,
                })

                return PullRequest(
                    id=str(mr.iid),
                    title=mr.title,
                    description=mr.description,
                    source_branch=mr.source_branch,
                    target_branch=mr.target_branch,
                    status=mr.state,
                    created_at=datetime.strptime(mr.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(mr.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    merged_at=datetime.strptime(mr.merged_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if mr.merged_at
                    else None,
                    closed_at=None,  # GitLab doesn't provide closed_at separately
                )
            except GitlabGetError as e:
                msg = f"Could not create merge request: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_branches(self, repo_name: str) -> list[Branch]:
            try:
                gl_project = self.client.projects.get(repo_name)
                default_branch = gl_project.default_branch
                return [
                    Branch(
                        name=branch.name,
                        sha=branch.commit["id"],
                        protected=branch.protected,
                        default=(branch.name == default_branch),
                    )
                    for branch in gl_project.branches.list()
                ]
            except GitlabGetError as e:
                msg = f"Could not get branches: {e!s}"
                raise ResourceNotFoundError(msg)

    def get_pull_request(self, repo_name: str, pr_id: str) -> PullRequest:
            try:
                gl_project = self.client.projects.get(repo_name)
                mr = gl_project.mergerequests.get(pr_id)

                return PullRequest(
                    id=str(mr.iid),
                    title=mr.title,
                    description=mr.description,
                    source_branch=mr.source_branch,
                    target_branch=mr.target_branch,
                    status=mr.state,
                    created_at=datetime.strptime(mr.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(mr.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    merged_at=datetime.strptime(mr.merged_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if mr.merged_at
                    else None,
                    closed_at=None,
                )
            except GitlabGetError as e:
                msg = f"Could not get merge request: {e!s}"
                raise ResourceNotFoundError(msg)

        def merge_pull_request(self, repo_name: str, pr_id: str) -> bool:
            try:
                gl_project = self.client.projects.get(repo_name)
                mr = gl_project.mergerequests.get(pr_id)
                return mr.merge()
            except GitlabGetError as e:
                msg = f"Could not merge request: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflows(self, repo_name: str) -> list[Workflow]:
            try:
                project = self.client.projects.get(repo_name)
                pipelines = project.pipelineschedules.list()
                return [
                    Workflow(
                        id=str(pl.id),
                        name=pl.description or f"Pipeline {pl.id}",
                        path=pl.ref,
                        state=pl.active and "active" or "inactive",
                        created_at=datetime.strptime(pl.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        updated_at=datetime.strptime(pl.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    )
                    for pl in pipelines
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get workflows: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow(self, repo_name: str, workflow_id: str) -> Workflow:
            try:
                project = self.client.projects.get(repo_name)
                pl = project.pipelineschedules.get(workflow_id)
                return Workflow(
                    id=str(pl.id),
                    name=pl.description or f"Pipeline {pl.id}",
                    path=pl.ref,
                    state=pl.active and "active" or "inactive",
                    created_at=datetime.strptime(pl.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(pl.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get workflow: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow_runs(
            self, repo_name: str, workflow_id: str, branch: str = None
        ) -> list[WorkflowRun]:
            try:
                project = self.client.projects.get(repo_name)
                pipelines = (
                    project.pipelines.list(ref=branch) if branch else project.pipelines.list()
                )

                return [
                    WorkflowRun(
                        id=str(run.id),
                        name=f"Pipeline {run.id}",
                        workflow_id=str(workflow_id),
                        status=run.status,
                        conclusion=run.status,
                        branch=run.ref,
                        commit_sha=run.sha,
                        url=run.web_url,
                        created_at=datetime.strptime(run.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        updated_at=datetime.strptime(run.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        started_at=None,
                        completed_at=None,
                    )
                    for run in pipelines
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get workflow runs: {e!s}"
                raise ResourceNotFoundError(msg)

        def trigger_workflow(
            self, repo_name: str, workflow_id: str, branch: str, inputs: dict = None
        ) -> WorkflowRun:
            try:
                project = self.client.projects.get(repo_name)
                pipeline = project.pipelines.create({
                    "ref": branch,
                    "variables": inputs or {},
                })

                return WorkflowRun(
                    id=str(pipeline.id),
                    name=f"Pipeline {pipeline.id}",
                    workflow_id=str(workflow_id),
                    status=pipeline.status,
                    conclusion=pipeline.status,
                    branch=pipeline.ref,
                    commit_sha=pipeline.sha,
                    url=pipeline.web_url,
                    created_at=datetime.strptime(
                        pipeline.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    updated_at=datetime.strptime(
                        pipeline.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    started_at=None,
                    completed_at=None,
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not trigger workflow: {e!s}"
                raise ResourceNotFoundError(msg)

        def cancel_workflow_run(self, repo_name: str, run_id: str) -> bool:
            try:
                project = self.client.projects.get(repo_name)
                pipeline = project.pipelines.get(run_id)
                pipeline.cancel()
                return True
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not cancel workflow run: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow_run_logs(self, repo_name: str, run_id: str) -> str:
            try:
                project = self.client.projects.get(repo_name)
                pipeline = project.pipelines.get(run_id)
                jobs = pipeline.jobs.list()
                logs = []
                for job in jobs:
                    logs.append(f"=== Job: {job.name} ===\n{job.trace()}")
                return "\n".join(logs)
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get workflow run logs: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_collaborators(self, repo_name: str) -> list[User]:
            try:
                project = self.client.projects.get(repo_name)
                members = project.members.list()
                return [
                    User(
                        username=member.username,
                        name=member.name,
                        email=member.email,
                        avatar_url=member.avatar_url,
                        created_at=datetime.strptime(
                            member.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    )
                    for member in members
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get collaborators: {e!s}"
                raise ResourceNotFoundError(msg)

        def add_collaborator(
            self, repo_name: str, username: str, permission: str = "pull"
        ) -> bool:
            try:
                access_level_map = {
                    "pull": gitlab.GUEST_ACCESS,
                    "push": gitlab.DEVELOPER_ACCESS,
                    "admin": gitlab.MAINTAINER_ACCESS,
                }
                project = self.client.projects.get(repo_name)
                project.members.create({
                    "user_id": self.client.users.list(username=username)[0].id,
                    "access_level": access_level_map.get(permission, gitlab.GUEST_ACCESS),
                })
                return True
            except gitlab.exceptions.GitlabError:
                return False

        def get_comments(
            self, repo_name: str, target_id: str, target_type: str = "pr"
        ) -> list[Comment]:
            try:
                project = self.client.projects.get(repo_name)
                if target_type == "pr":
                    target = project.mergerequests.get(target_id)
                else:
                    target = project.issues.get(target_id)

                notes = target.notes.list()
                return [
                    Comment(
                        id=str(note.id),
                        body=note.body,
                        author=User(
                            username=note.author["username"],
                            name=note.author["name"],
                            email=None,  # GitLab API doesn't provide email in notes
                            avatar_url=note.author["avatar_url"],
                            created_at=datetime.strptime(
                                note.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                        ),
                        created_at=datetime.strptime(
                            note.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        updated_at=datetime.strptime(
                            note.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    )
                    for note in notes
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get comments: {e!s}"
                raise ResourceNotFoundError(msg)

        def add_labels(
            self, repo_name: str, target_id: str, labels: list[str], target_type: str = "pr"
        ) -> list[Label]:
            try:
                project = self.client.projects.get(repo_name)
                if target_type == "pr":
                    target = project.mergerequests.get(target_id)
                else:
                    target = project.issues.get(target_id)

                target.labels = list(set(target.labels + labels))
                target.save()

                return [
                    Label(
                        name=label, color="", description=""
                    )  # GitLab API doesn't return label details in this context
                    for label in labels
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not add labels: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_label(
            self, repo_name: str, name: str, color: str, description: str = ""
        ) -> Label:
            try:
                project = self.client.projects.get(repo_name)
                gl_label = project.labels.create({
                    "name": name,
                    "color": color,
                    "description": description,
                })
                return Label(
                    name=gl_label.name,
                    color=gl_label.color,
                    description=gl_label.description or "",
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not create label: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_commits(self, repo_name: str, branch: str | None = None) -> list[Commit]:
            try:
                project = self.client.projects.get(repo_name)
                commits = (
                    project.commits.list(ref=branch) if branch else project.commits.list()
                )
                return [
                    Commit(
                        sha=commit.id,
                        message=commit.message,
                        author=User(
                            username=commit.author_name,
                            name=commit.author_name,
                            email=commit.author_email,
                            avatar_url=None,
                            created_at=datetime.strptime(
                                commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                        ),
                        committer=User(
                            username=commit.committer_name,
                            name=commit.committer_name,
                            email=commit.committer_email,
                            avatar_url=None,
                            created_at=datetime.strptime(
                                commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                            ),
                        ),
                        created_at=datetime.strptime(
                            commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        url=commit.web_url,
                    )
                    for commit in commits
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get commits: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_commit(self, repo_name: str, commit_sha: str) -> Commit:
            try:
                project = self.client.projects.get(repo_name)
                commit = project.commits.get(commit_sha)
                return Commit(
                    sha=commit.id,
                    message=commit.message,
                    author=User(
                        username=commit.author_name,
                        name=commit.author_name,
                        email=commit.author_email,
                        avatar_url=None,
                        created_at=datetime.strptime(
                            commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    ),
                    committer=User(
                        username=commit.committer_name,
                        name=commit.committer_name,
                        email=commit.committer_email,
                        avatar_url=None,
                        created_at=datetime.strptime(
                            commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    ),
                    created_at=datetime.strptime(commit.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    url=commit.web_url,
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get commit: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_branch(
            self, repo_name: str, branch_name: str, source_branch: str
        ) -> Branch:
            try:
                project = self.client.projects.get(repo_name)
                branch = project.branches.create({
                    "branch": branch_name,
                    "ref": source_branch,
                })
                return Branch(
                    name=branch.name,
                    sha=branch.commit["id"],
                    protected=branch.protected,
                    default=False,
                )
            except (gitlab.exceptions.GitlabError, Exception) as e:
                msg = f"Could not create branch: {e!s}"
                raise ResourceNotFoundError(msg)

        def delete_branch(self, repo_name: str, branch_name: str) -> bool:
            try:
                project = self.client.projects.get(repo_name)
                project.branches.delete(branch_name)
                return True
            except (gitlab.exceptions.GitlabError, Exception):
                return False

        def protect_branch(self, repo_name: str, branch_name: str) -> bool:
            try:
                project = self.client.projects.get(repo_name)
                branch = project.branches.get(branch_name)
                branch.protect()
                return True
            except (gitlab.exceptions.GitlabError, Exception):
                return False

        def create_repository(
            self,
            name: str,
            private: bool = False,
            description: str = "",
            **kwargs: Any,
        ) -> Repository:
            try:
                visibility = "private" if private else "public"
                gl_project = self.client.projects.create({
                    "name": name,
                    "description": description,
                    "visibility": visibility,
                    **kwargs,
                })

                return Repository(
                    name=gl_project.name,
                    url=gl_project.web_url,
                    description=gl_project.description,
                    private=gl_project.visibility == "private",
                    default_branch=gl_project.default_branch,
                    created_at=datetime.strptime(
                        gl_project.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    updated_at=datetime.strptime(
                        gl_project.last_activity_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not create repository: {e!s}"
                raise ResourceNotFoundError(msg)

        def delete_repository(self, repo_name: str) -> bool:
            try:
                project = self.client.projects.get(repo_name)
                project.delete()
                return True
            except gitlab.exceptions.GitlabError:
                return False

        def get_pull_requests(self, repo_name: str, state: str = "open") -> list[PullRequest]:
            try:
                project = self.client.projects.get(repo_name)
                merge_requests = project.mergerequests.list(state=state)

                return [
                    PullRequest(
                        id=str(mr.iid),
                        title=mr.title,
                        description=mr.description,
                        source_branch=mr.source_branch,
                        target_branch=mr.target_branch,
                        status=mr.state,
                        created_at=datetime.strptime(mr.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        updated_at=datetime.strptime(mr.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        merged_at=datetime.strptime(mr.merged_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                        if mr.merged_at
                        else None,
                        closed_at=None,
                    )
                    for mr in merge_requests
                ]
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get pull requests: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_issue(self, repo_name: str, title: str, description: str = "") -> Issue:
            try:
                project = self.client.projects.get(repo_name)
                issue = project.issues.create({"title": title, "description": description})

                return Issue(
                    id=str(issue.id),
                    number=str(issue.iid),
                    title=issue.title,
                    description=issue.description,
                    state=issue.state,
                    created_at=datetime.strptime(issue.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(issue.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    closed_at=None,
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not create issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_issue(self, repo_name: str, issue_id: str) -> Issue:
            try:
                project = self.client.projects.get(repo_name)
                issue = project.issues.get(issue_id)

                return Issue(
                    id=str(issue.id),
                    number=str(issue.iid),
                    title=issue.title,
                    description=issue.description,
                    state=issue.state,
                    created_at=datetime.strptime(issue.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(issue.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    closed_at=datetime.strptime(issue.closed_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if issue.closed_at
                    else None,
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def close_issue(self, repo_name: str, issue_id: str) -> bool:
            try:
                project = self.client.projects.get(repo_name)
                issue = project.issues.get(issue_id)
                issue.state_event = "close"
                issue.save()
                return True
            except gitlab.exceptions.GitlabError:
                return False

        def add_comment(
            self, repo_name: str, target_id: str, comment: str, target_type: str = "pr"
        ) -> Comment:
            try:
                project = self.client.projects.get(repo_name)
                if target_type == "pr":
                    target = project.mergerequests.get(target_id)
                else:
                    target = project.issues.get(target_id)

                note = target.notes.create({"body": comment})

                return Comment(
                    id=str(note.id),
                    body=note.body,
                    author=User(
                        username=note.author["username"],
                        name=note.author["name"],
                        avatar_url=note.author["avatar_url"],
                        created_at=datetime.strptime(
                            note.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                    ),
                    created_at=datetime.strptime(note.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(note.updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not add comment: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_user(self) -> User:
            try:
                user = self.client.user
                return User(
                    username=user.username,
                    name=user.name,
                    email=user.email,
                    avatar_url=user.avatar_url,
                    created_at=datetime.strptime(user.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    bio=user.bio,
                    location=user.location,
                )
            except gitlab.exceptions.GitlabError as e:
                msg = f"Could not get user: {e!s}"
                raise ResourceNotFoundError(msg)



def test_get_branches(gitlab_provider, mock_branch):
    # Setup
    mock_gl_branch = Mock()
    mock_gl_branch.name = mock_branch.name
    mock_gl_branch.commit.id = mock_branch.sha
    mock_gl_branch.protected = mock_branch.protected

    mock_project = Mock()
    mock_project.branches.list.return_value = [mock_gl_branch]
    mock_project.default_branch = "main"

    gitlab_provider.client.projects.get.return_value = mock_project

    # Execute
    branches = gitlab_provider.get_branches("owner/repo")

    # Assert
    assert len(branches) == 1
    assert branches[0].name == mock_branch.name
    assert branches[0].sha == mock_branch.sha


def test_create_pull_request(gitlab_provider, mock_pull_request):
    # Setup
    mock_mr = Mock()
    mock_mr.iid = int(mock_pull_request.id)
    mock_mr.title = mock_pull_request.title
    mock_mr.description = mock_pull_request.description
    mock_mr.source_branch = mock_pull_request.source_branch
    mock_mr.target_branch = mock_pull_request.target_branch
    mock_mr.state = mock_pull_request.status
    mock_mr.created_at = mock_pull_request.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    mock_mr.updated_at = mock_pull_request.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    mock_project = Mock()
    mock_project.mergerequests.create.return_value = mock_mr
    gitlab_provider.client.projects.get.return_value = mock_project

    # Execute
    pr = gitlab_provider.create_pull_request(
        repo_name="owner/repo",
        source_branch=mock_pull_request.source_branch,
        target_branch=mock_pull_request.target_branch,
        title=mock_pull_request.title,
        description=mock_pull_request.description,
    )

    # Assert
    assert pr.id == mock_pull_request.id
    assert pr.title == mock_pull_request.title
    assert pr.source_branch == mock_pull_request.source_branch
