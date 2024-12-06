
    def create_repository(
            self, name: str, private: bool = False, description: str = ""
        ) -> Repository:
            try:
                gh_repo = self.client.get_user().create_repo(
                    name=name, private=private, description=description
                )
                return Repository(
                    name=gh_repo.name,
                    url=gh_repo.html_url,
                    description=gh_repo.description,
                    private=gh_repo.private,
                    default_branch=gh_repo.default_branch,
                    created_at=gh_repo.created_at,
                    updated_at=gh_repo.updated_at,
                )
            except GithubException as e:
                msg = f"Could not create repository: {e!s}"
                raise ResourceNotFoundError(msg)

    def delete_repository(self, repo_name: str) -> bool:
        try:
            repo = self.client.get_repo(repo_name)
            repo.delete()
            return True
        except GithubException:
            return False

    def get_branches(self, repo_name: str) -> list[Branch]:
        try:
            gh_repo = self.client.get_repo(repo_name)
            default_branch = gh_repo.default_branch
            return [
                Branch(
                    name=branch.name,
                    sha=branch.commit.sha,
                    protected=branch.protected,
                    default=(branch.name == default_branch),
                )
                for branch in gh_repo.get_branches()
            ]
        except GithubException as e:
            msg = f"Could not get branches: {e!s}"
            raise ResourceNotFoundError(msg)


    def create_branch(
            self, repo_name: str, branch_name: str, source_branch: str
        ) -> Branch:
            try:
                repo = self.client.get_repo(repo_name)
                source = repo.get_branch(source_branch)
                repo.create_git_ref(f"refs/heads/{branch_name}", source.commit.sha)
                new_branch = repo.get_branch(branch_name)
                return Branch(
                    name=new_branch.name,
                    sha=new_branch.commit.sha,
                    protected=new_branch.protected,
                    default=False,
                )
            except GithubException as e:
                msg = f"Could not create branch: {e!s}"
                raise ResourceNotFoundError(msg)

        def delete_branch(self, repo_name: str, branch_name: str) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                ref = repo.get_git_ref(f"heads/{branch_name}")
                ref.delete()
                return True
            except GithubException:
                return False

        def protect_branch(self, repo_name: str, branch_name: str) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                branch = repo.get_branch(branch_name)
                branch.edit_protection(strict=True, contexts=[], enforce_admins=True)
                return True
            except GithubException:
                return False

        def create_pull_request(
            self,
            repo_name: str,
            source_branch: str,
            target_branch: str,
            title: str,
            description: str = "",
        ) -> PullRequest:
            try:
                gh_repo = self.client.get_repo(repo_name)
                gh_pr = gh_repo.create_pull(
                    title=title, body=description, base=target_branch, head=source_branch
                )
                return PullRequest(
                    id=str(gh_pr.number),
                    title=gh_pr.title,
                    description=gh_pr.body or "",
                    source_branch=gh_pr.head.ref,
                    target_branch=gh_pr.base.ref,
                    status=gh_pr.state,
                    created_at=gh_pr.created_at,
                    updated_at=gh_pr.updated_at,
                    merged_at=gh_pr.merged_at,
                    closed_at=gh_pr.closed_at,
                )
            except GithubException as e:
                msg = f"Could not create pull request: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_pull_request(self, repo_name: str, pr_id: str) -> PullRequest:
            try:
                repo = self.client.get_repo(repo_name)
                pr = repo.get_pull(int(pr_id))
                return PullRequest(
                    id=str(pr.number),
                    title=pr.title,
                    description=pr.body or "",
                    source_branch=pr.head.ref,
                    target_branch=pr.base.ref,
                    status=pr.state,
                    created_at=pr.created_at,
                    updated_at=pr.updated_at,
                    merged_at=pr.merged_at,
                    closed_at=pr.closed_at,
                )
            except GithubException as e:
                msg = f"Could not get pull request: {e!s}"
                raise ResourceNotFoundError(msg)

        def merge_pull_request(self, repo_name: str, pr_id: str) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                pr = repo.get_pull(int(pr_id))
                return pr.merge().merged
            except GithubException:
                return False

        def get_pull_requests(self, repo_name: str, state: str = "open") -> list[PullRequest]:
            try:
                repo = self.client.get_repo(repo_name)
                return [
                    PullRequest(
                        id=str(pr.number),
                        title=pr.title,
                        description=pr.body or "",
                        source_branch=pr.head.ref,
                        target_branch=pr.base.ref,
                        status=pr.state,
                        created_at=pr.created_at,
                        updated_at=pr.updated_at,
                        merged_at=pr.merged_at,
                        closed_at=pr.closed_at,
                    )
                    for pr in repo.get_pulls(state=state)
                ]
            except GithubException as e:
                msg = f"Could not get pull requests: {e!s}"
                raise ResourceNotFoundError(msg)

        # Issue Operations
        def create_issue(self, repo_name: str, title: str, description: str = "") -> Issue:
            try:
                repo = self.client.get_repo(repo_name)
                gh_issue = repo.create_issue(title=title, body=description)
                return Issue(
                    id=str(gh_issue.number),
                    number=gh_issue.number,
                    title=gh_issue.title,
                    description=gh_issue.body or "",
                    state=gh_issue.state,
                    author=User(
                        username=gh_issue.user.login,
                        name=gh_issue.user.name,
                        email=gh_issue.user.email,
                        avatar_url=gh_issue.user.avatar_url,
                        created_at=gh_issue.user.created_at,
                    ),
                    assignee=None,  # TODO: Add assignee support
                    labels=[],  # TODO: Add labels support
                    created_at=gh_issue.created_at,
                    updated_at=gh_issue.updated_at,
                    closed_at=gh_issue.closed_at,
                )
            except GithubException as e:
                msg = f"Could not create issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_issue(self, repo_name: str, issue_id: str) -> Issue:
            try:
                repo = self.client.get_repo(repo_name)
                issue = repo.get_issue(int(issue_id))
                return Issue(
                    id=str(issue.number),
                    number=issue.number,
                    title=issue.title,
                    description=issue.body or "",
                    state=issue.state,
                    author=User(
                        username=issue.user.login,
                        name=issue.user.name,
                        email=issue.user.email,
                        avatar_url=issue.user.avatar_url,
                        created_at=issue.user.created_at,
                    ),
                    assignee=None,  # TODO: Add assignee support
                    labels=[],  # TODO: Add labels support
                    created_at=issue.created_at,
                    updated_at=issue.updated_at,
                    closed_at=issue.closed_at,
                )
            except GithubException as e:
                msg = f"Could not get issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def close_issue(self, repo_name: str, issue_id: str) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                issue = repo.get_issue(int(issue_id))
                issue.edit(state="closed")
                return True
            except GithubException:
                return False

        # Comment Operations
        def add_comment(
            self, repo_name: str, target_id: str, comment: str, target_type: str = "pr"
        ) -> Comment:
            try:
                repo = self.client.get_repo(repo_name)
                if target_type == "pr":
                    target = repo.get_pull(int(target_id))
                else:
                    target = repo.get_issue(int(target_id))

                gh_comment = target.create_comment(comment)
                return Comment(
                    id=str(gh_comment.id),
                    body=gh_comment.body,
                    author=User(
                        username=gh_comment.user.login,
                        name=gh_comment.user.name,
                        email=gh_comment.user.email,
                        avatar_url=gh_comment.user.avatar_url,
                        created_at=gh_comment.user.created_at,
                    ),
                    created_at=gh_comment.created_at,
                    updated_at=gh_comment.updated_at,
                )
            except GithubException as e:
                msg = f"Could not add comment: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflows(self, repo_name: str) -> list[Workflow]:
            try:
                repo = self.client.get_repo(repo_name)
                workflows = repo.get_workflows()
                return [
                    Workflow(
                        id=str(wf.id),
                        name=wf.name,
                        path=wf.path,
                        state=wf.state,
                        created_at=wf.created_at,
                        updated_at=wf.updated_at,
                    )
                    for wf in workflows
                ]
            except GithubException as e:
                msg = f"Could not get workflows: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow(self, repo_name: str, workflow_id: str) -> Workflow:
            try:
                repo = self.client.get_repo(repo_name)
                wf = repo.get_workflow(workflow_id)
                return Workflow(
                    id=str(wf.id),
                    name=wf.name,
                    path=wf.path,
                    state=wf.state,
                    created_at=wf.created_at,
                    updated_at=wf.updated_at,
                )
            except GithubException as e:
                msg = f"Could not get workflow: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow_runs(
            self, repo_name: str, workflow_id: str, branch: str = None
        ) -> list[WorkflowRun]:
            try:
                repo = self.client.get_repo(repo_name)
                workflow = repo.get_workflow(workflow_id)
                runs = workflow.get_runs(branch=branch) if branch else workflow.get_runs()

                return [
                    WorkflowRun(
                        id=str(run.id),
                        name=run.name,
                        workflow_id=str(workflow_id),
                        status=run.status,
                        conclusion=run.conclusion,
                        branch=run.head_branch,
                        commit_sha=run.head_sha,
                        url=run.html_url,
                        created_at=run.created_at,
                        updated_at=run.updated_at,
                        started_at=run.started_at,
                        completed_at=run.completed_at,
                    )
                    for run in runs
                ]
            except GithubException as e:
                msg = f"Could not get workflow runs: {e!s}"
                raise ResourceNotFoundError(msg)

        def trigger_workflow(
            self, repo_name: str, workflow_id: str, branch: str, inputs: dict = None
        ) -> WorkflowRun:
            try:
                repo = self.client.get_repo(repo_name)
                workflow = repo.get_workflow(workflow_id)
                run = workflow.create_dispatch(branch, inputs or {})

                return WorkflowRun(
                    id=str(run.id),
                    name=run.name,
                    workflow_id=str(workflow_id),
                    status=run.status,
                    conclusion=None,
                    branch=branch,
                    commit_sha=run.head_sha,
                    url=run.html_url,
                    created_at=run.created_at,
                    updated_at=run.updated_at,
                    started_at=None,
                    completed_at=None,
                )
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not trigger workflow: {e!s}")

        def cancel_workflow_run(self, repo_name: str, run_id: str) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                run = repo.get_workflow_run(run_id)
                run.cancel()
                return True
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not cancel workflow run: {e!s}")

        def get_workflow_run_logs(self, repo_name: str, run_id: str) -> str:
            try:
                repo = self.client.get_repo(repo_name)
                run = repo.get_workflow_run(run_id)
                return run.get_logs()
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not get workflow run logs: {e!s}")

        def get_user(self) -> User:
            gh_user = self.client.get_user()
            return User(
                username=gh_user.login,
                name=gh_user.name,
                email=gh_user.email,
                avatar_url=gh_user.avatar_url,
                created_at=gh_user.created_at,
            )

        def get_collaborators(self, repo_name: str) -> list[User]:
            try:
                repo = self.client.get_repo(repo_name)
                return [
                    User(
                        username=collab.login,
                        name=collab.name,
                        email=collab.email,
                        avatar_url=collab.avatar_url,
                        created_at=collab.created_at,
                    )
                    for collab in repo.get_collaborators()
                ]
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not get collaborators: {e!s}")

        def add_collaborator(
            self, repo_name: str, username: str, permission: str = "pull"
        ) -> bool:
            try:
                repo = self.client.get_repo(repo_name)
                repo.add_to_collaborators(username, permission=permission)
                return True
            except GithubException:
                return False

        def get_comments(
            self, repo_name: str, target_id: str, target_type: str = "pr"
        ) -> list[Comment]:
            try:
                repo = self.client.get_repo(repo_name)
                if target_type == "pr":
                    target = repo.get_pull(int(target_id))
                else:
                    target = repo.get_issue(int(target_id))

                return [
                    Comment(
                        id=str(comment.id),
                        body=comment.body,
                        author=User(
                            username=comment.user.login,
                            name=comment.user.name,
                            email=comment.user.email,
                            avatar_url=comment.user.avatar_url,
                            created_at=comment.user.created_at,
                        ),
                        created_at=comment.created_at,
                        updated_at=comment.updated_at,
                    )
                    for comment in target.get_comments()
                ]
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not get comments: {e!s}")

        def add_labels(
            self, repo_name: str, target_id: str, labels: list[str], target_type: str = "pr"
        ) -> list[Label]:
            try:
                repo = self.client.get_repo(repo_name)
                if target_type == "pr":
                    target = repo.get_pull(int(target_id))
                else:
                    target = repo.get_issue(int(target_id))

                added_labels = target.add_to_labels(*labels)
                return [
                    Label(
                        name=label.name,
                        color=label.color,
                        description=label.description or "",
                    )
                    for label in added_labels
                ]
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not add labels: {e!s}")

        def create_label(
            self, repo_name: str, name: str, color: str, description: str = ""
        ) -> Label:
            try:
                repo = self.client.get_repo(repo_name)
                gh_label = repo.create_label(name=name, color=color, description=description)
                return Label(
                    name=gh_label.name,
                    color=gh_label.color,
                    description=gh_label.description or "",
                )
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not create label: {e!s}")

        def get_commit(self, repo_name: str, commit_sha: str) -> Commit:
            try:
                repo = self.client.get_repo(repo_name)
                gh_commit = repo.get_commit(commit_sha)
                return Commit(
                    sha=gh_commit.sha,
                    message=gh_commit.commit.message,
                    author=User(
                        username=gh_commit.author.login if gh_commit.author else "unknown",
                        name=gh_commit.commit.author.name,
                        email=gh_commit.commit.author.email,
                        avatar_url=gh_commit.author.avatar_url if gh_commit.author else None,
                        created_at=gh_commit.author.created_at
                        if gh_commit.author
                        else datetime.now(),
                    ),
                    committer=User(
                        username=gh_commit.committer.login
                        if gh_commit.committer
                        else "unknown",
                        name=gh_commit.commit.committer.name,
                        email=gh_commit.commit.committer.email,
                        avatar_url=gh_commit.committer.avatar_url
                        if gh_commit.committer
                        else None,
                        created_at=gh_commit.committer.created_at
                        if gh_commit.committer
                        else datetime.now(),
                    ),
                    created_at=gh_commit.commit.author.date,
                    url=gh_commit.html_url,
                )
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not get commit: {e!s}")

        def get_commits(self, repo_name: str, branch: str | None = None) -> list[Commit]:
            try:
                repo = self.client.get_repo(repo_name)
                commits = repo.get_commits(sha=branch) if branch else repo.get_commits()
                return [
                    Commit(
                        sha=commit.sha,
                        message=commit.commit.message,
                        author=User(
                            username=commit.author.login if commit.author else "unknown",
                            name=commit.commit.author.name,
                            email=commit.commit.author.email,
                            avatar_url=commit.author.avatar_url if commit.author else None,
                            created_at=commit.author.created_at
                            if commit.author
                            else datetime.now(),
                        ),
                        committer=User(
                            username=commit.committer.login
                            if commit.committer
                            else "unknown",
                            name=commit.commit.committer.name,
                            email=commit.commit.committer.email,
                            avatar_url=commit.committer.avatar_url
                            if commit.committer
                            else None,
                            created_at=commit.committer.created_at
                            if commit.committer
                            else datetime.now(),
                        ),
                        created_at=commit.commit.author.date,
                        url=commit.html_url,
                    )
                    for commit in commits
                ]
            except GithubException as e:
                raise ResourceNotFoundError(f"Could not get commits: {e!s}")




def test_create_pull_request_success(github_provider, mock_pull_request):
    # Setup
    mock_gh_pr = Mock()
    mock_gh_pr.number = int(mock_pull_request.id)
    mock_gh_pr.title = mock_pull_request.title
    mock_gh_pr.body = mock_pull_request.description
    mock_gh_pr.head.ref = mock_pull_request.source_branch
    mock_gh_pr.base.ref = mock_pull_request.target_branch
    mock_gh_pr.state = mock_pull_request.status
    mock_gh_pr.created_at = mock_pull_request.created_at
    mock_gh_pr.updated_at = mock_pull_request.updated_at
    mock_gh_pr.merged_at = None
    mock_gh_pr.closed_at = None

    mock_repo = Mock()
    mock_repo.create_pull.return_value = mock_gh_pr
    github_provider.client.get_repo.return_value = mock_repo

    # Execute
    pr = github_provider.create_pull_request(
        "owner/test-repo",
        source_branch="feature-branch",
        target_branch="main",
        title="Test PR",
        description="Test description",
    )

    # Assert
    assert pr.id == mock_pull_request.id
    assert pr.title == mock_pull_request.title
    assert pr.source_branch == mock_pull_request.source_branch


def supports_url():
    assert GitHubRepository.supports_url("https://github.com/owner/repo")
    assert not GitHubRepository.supports_url("https://gitlab.com/owner/repo")


def test_get_branches(github_provider, mock_branch):
    # Setup
    mock_gh_branch = Mock()
    mock_gh_branch.name = mock_branch.name
    mock_gh_branch.commit.sha = mock_branch.sha
    mock_gh_branch.protected = mock_branch.protected

    mock_repo = Mock()
    mock_repo.default_branch = "main"
    mock_repo.get_branches.return_value = [mock_gh_branch]
    github_provider.client.get_repo.return_value = mock_repo

    # Execute
    branches = github_provider.get_branches("owner/repo")

    # Assert
    assert len(branches) == 1
    assert branches[0].name == mock_branch.name
    assert branches[0].sha == mock_branch.sha


def test_merge_pull_request(github_provider):
    # Setup
    mock_repo = Mock()
    mock_pr = Mock()
    mock_pr.merge.return_value = True

    mock_repo.get_pull.return_value = mock_pr
    github_provider.client.get_repo.return_value = mock_repo

    # Execute
    result = github_provider.merge_pull_request("owner/repo", "1")

    # Assert
    assert result is True
    mock_pr.merge.assert_called_once()
