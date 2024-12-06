
    def create_pull_request(
            self,
            repo_name: str,
            source_branch: str,
            target_branch: str,
            title: str,
            description: str = "",
        ) -> PullRequest:
            try:
                workspace, repo_slug = repo_name.split("/")
                pr = self.client.create_pull_request(
                    workspace,
                    repo_slug,
                    title=title,
                    source_branch=source_branch,
                    destination_branch=target_branch,
                    description=description,
                )

                return PullRequest(
                    id=str(pr["id"]),
                    title=pr["title"],
                    description=pr.get("description", ""),
                    source_branch=pr["source"]["branch"]["name"],
                    target_branch=pr["destination"]["branch"]["name"],
                    status=pr["state"],
                    created_at=datetime.strptime(pr["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    updated_at=datetime.strptime(pr["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    merged_at=None,  # Need to check PR status separately
                    closed_at=None,
                )
            except ApiError as e:
                msg = f"Could not create pull request: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_branches(self, repo_name: str) -> list[Branch]:
            try:
                workspace, repo_slug = repo_name.split("/")
                branches_data = self.client.get_branches(workspace, repo_slug)
                repo = self.client.get_repository(workspace, repo_slug)
                default_branch = repo["mainbranch"]["name"]

                branches = []
                for branch in branches_data:
                    branches.append(
                        Branch(
                            name=branch["name"],
                            sha=branch["target"]["hash"],
                            protected=False,  # Need additional API call to check branch restrictions
                            default=(branch["name"] == default_branch),
                        )
                    )
                return branches
            except ApiError as e:
                msg = f"Could not get branches: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_pull_request(self, repo_name: str, pr_id: str) -> PullRequest:
            try:
                workspace, repo_slug = repo_name.split("/")
                pr = self.client.get_pull_request(workspace, repo_slug, pr_id)

                return PullRequest(
                    id=str(pr["id"]),
                    title=pr["title"],
                    description=pr.get("description", ""),
                    source_branch=pr["source"]["branch"]["name"],
                    target_branch=pr["destination"]["branch"]["name"],
                    status=pr["state"],
                    created_at=datetime.strptime(pr["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    updated_at=datetime.strptime(pr["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    merged_at=None,  # Need to check PR status separately
                    closed_at=None,
                )
            except ApiError as e:
                msg = f"Could not get pull request: {e!s}"
                raise ResourceNotFoundError(msg)

        def merge_pull_request(self, repo_name: str, pr_id: str) -> bool:
            try:
                workspace, repo_slug = repo_name.split("/")
                result = self.client.merge_pull_request(workspace, repo_slug, pr_id)
                return result["state"] == "MERGED"
            except ApiError as e:
                msg = f"Could not merge pull request: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow(self, repo_name: str, workflow_id: str) -> Workflow:
            try:
                workspace, repo_slug = repo_name.split("/")
                pl = self.client.get_pipeline(workspace, repo_slug, workflow_id)
                return Workflow(
                    id=str(pl["uuid"]),
                    name=pl.get("name", f"Pipeline {pl['uuid']}"),
                    path=pl["target"]["ref_name"],
                    state=pl["state"],
                    created_at=datetime.strptime(pl["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    updated_at=datetime.strptime(pl["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                )
            except Exception as e:
                msg = f"Could not get workflow: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_collaborators(self, repo_name: str) -> list[User]:
            try:
                workspace, repo_slug = repo_name.split("/")
                users = self.client.get_repository_users(workspace, repo_slug)
                return [
                    User(
                        username=user["nickname"],
                        name=user.get("display_name"),
                        email=None,  # Bitbucket API doesn't provide email
                        avatar_url=user.get("links", {}).get("avatar", {}).get("href"),
                        created_at=datetime.now(),  # Bitbucket API doesn't provide created_at
                    )
                    for user in users
                ]
            except Exception as e:
                msg = f"Could not get collaborators: {e!s}"
                raise ResourceNotFoundError(msg)

        def add_collaborator(
            self, repo_name: str, username: str, permission: str = "pull"
        ) -> bool:
            try:
                workspace, repo_slug = repo_name.split("/")
                permission_map = {"pull": "read", "push": "write", "admin": "admin"}
                self.client.update_repository_user(
                    workspace, repo_slug, username, permission_map.get(permission, "read")
                )
                return True
            except Exception:
                return False

        def get_comments(
            self, repo_name: str, target_id: str, target_type: str = "pr"
        ) -> list[Comment]:
            try:
                workspace, repo_slug = repo_name.split("/")
                if target_type == "pr":
                    comments = self.client.get_pullrequest_comments(
                        workspace, repo_slug, target_id
                    )
                else:
                    comments = self.client.get_issue_comments(workspace, repo_slug, target_id)

                return [
                    Comment(
                        id=str(comment["id"]),
                        body=comment["content"]["raw"],
                        author=User(
                            username=comment["user"]["nickname"],
                            name=comment["user"].get("display_name"),
                            email=None,
                            avatar_url=comment["user"]
                            .get("links", {})
                            .get("avatar", {})
                            .get("href"),
                            created_at=datetime.strptime(
                                comment["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                            ),
                        ),
                        created_at=datetime.strptime(
                            comment["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                        updated_at=datetime.strptime(
                            comment["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                    )
                    for comment in comments
                ]
            except Exception as e:
                msg = f"Could not get comments: {e!s}"
                raise ResourceNotFoundError(msg)

        def add_labels(
            self, repo_name: str, target_id: str, labels: list[str], target_type: str = "pr"
        ) -> list[Label]:
            # Bitbucket doesn't have a native labels feature like GitHub/GitLab
            # You might want to use custom fields or tags as an alternative
            return [Label(name=label, color="", description="") for label in labels]

        def create_repository(
            self, name: str, private: bool = False, description: str = "", **kwargs: Any
        ) -> Repository:
            """Create a new repository on Bitbucket.

            Args:
                name: Repository name (should be in format "workspace/name" or workspace provided in kwargs)
                private: Whether the repository should be private
                description: Repository description
                **kwargs: Additional arguments including workspace if not in name

            Returns:
                Repository object representing the created repository

            Raises:
                ResourceNotFoundError: If repository creation fails
                ValueError: If workspace is not provided
            """
            try:
                # Handle workspace/name format
                if "/" in name:
                    workspace, repo_slug = name.split("/")
                else:
                    workspace = kwargs.get("workspace")
                    repo_slug = name

                if not workspace:
                    msg = "Workspace must be provided either in name (workspace/name) or as kwargs"
                    raise ValueError(msg)

                repo = self.client.create_repository(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    is_private=private,
                    description=description,
                )

                return Repository(
                    name=repo["name"],
                    url=repo["links"]["html"]["href"],
                    description=repo.get("description", ""),
                    private=not repo["is_private"],
                    default_branch=repo["mainbranch"]["name"]
                    if "mainbranch" in repo
                    else "main",
                    created_at=datetime.strptime(
                        repo["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    updated_at=datetime.strptime(
                        repo["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                )
            except ApiError as e:
                msg = f"Could not create repository: {e!s}"
                raise ResourceNotFoundError(msg)

        def delete_repository(self, repo_name: str) -> bool:
            """Delete a repository from Bitbucket.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"

            Returns:
                True if deletion was successful, False otherwise

            Raises:
                ResourceNotFoundError: If repository deletion fails
            """
            try:
                workspace, repo_slug = repo_name.split("/")
                self.client.delete_repository(workspace=workspace, repository_slug=repo_slug)
                return True
            except ApiError as e:
                msg = f"Could not delete repository: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_branch(
            self, repo_name: str, branch_name: str, source_branch: str
        ) -> Branch:
            """Create a new branch from source branch.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"
                branch_name: Name of the new branch
                source_branch: Name of the source branch

            Returns:
                Branch object representing the created branch

            Raises:
                ResourceNotFoundError: If branch creation fails
            """
            try:
                workspace, repo_slug = repo_name.split("/")

                # Get the commit hash of the source branch to use as starting point
                branches = self.client.get_branches(workspace, repo_slug)
                source = next((b for b in branches if b["name"] == source_branch), None)
                if not source:
                    msg = f"Source branch '{source_branch}' not found"
                    raise ResourceNotFoundError(msg)

                # Create the new branch
                branch = self.client.create_branch(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    name=branch_name,
                    start_point=source["target"]["hash"],
                )

                return Branch(
                    name=branch["name"],
                    sha=branch["target"]["hash"],
                    protected=False,  # Bitbucket doesn't return protection status in create response
                    default=False,  # New branches are never default
                )
            except ApiError as e:
                msg = f"Could not create branch: {e!s}"
                raise ResourceNotFoundError(msg)

        def delete_branch(self, repo_name: str, branch_name: str) -> bool:
            """Delete a branch.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"
                branch_name: Name of the branch to delete

            Returns:
                True if deletion was successful

            Raises:
                ResourceNotFoundError: If branch deletion fails
            """
            try:
                workspace, repo_slug = repo_name.split("/")

                # Check if branch exists and is not default branch
                repo = self.client.get_repository(workspace, repo_slug)
                if repo["mainbranch"]["name"] == branch_name:
                    msg = "Cannot delete default branch"
                    raise ValueError(msg)

                self.client.delete_branch(
                    workspace=workspace, repository_slug=repo_slug, name=branch_name
                )
                return True
            except ApiError as e:
                msg = f"Could not delete branch: {e!s}"
                raise ResourceNotFoundError(msg)

        def protect_branch(self, repo_name: str, branch_name: str) -> bool:
            """Enable branch protection.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"
                branch_name: Name of the branch to protect

            Returns:
                True if protection was enabled successfully

            Raises:
                ResourceNotFoundError: If setting branch protection fails
            """
            try:
                workspace, repo_slug = repo_name.split("/")

                # Bitbucket uses branch restrictions instead of direct protection
                # We'll set up basic merge restrictions for the branch
                restriction = self.client.set_branch_restriction(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    kind="push",  # Prevents direct pushes
                    pattern=branch_name,  # Branch name to protect
                    value=None,  # No specific value needed for push restriction
                )

                # Add merge restriction as well
                merge_restriction = self.client.set_branch_restriction(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    kind="require_approvals_to_merge",
                    pattern=branch_name,
                    value=1,  # Require at least 1 approval
                )

                return bool(restriction and merge_restriction)
            except ApiError as e:
                msg = f"Could not protect branch: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_pull_requests(self, repo_name: str, state: str = "open") -> list[PullRequest]:
            """Get all pull requests in a repository.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"
                state: State of PRs to fetch ("open", "merged", "declined", "superseded")

            Returns:
                List of PullRequest objects

            Raises:
                ResourceNotFoundError: If fetching pull requests fails
            """
            try:
                workspace, repo_slug = repo_name.split("/")

                # Map standard states to Bitbucket states
                state_map = {
                    "open": "OPEN",
                    "closed": "DECLINED",
                    "merged": "MERGED",
                    "all": None,  # Will fetch all states
                }

                bitbucket_state = state_map.get(state.lower(), state.upper())

                # Get pull requests
                prs = self.client.get_pull_requests(
                    workspace=workspace, repository_slug=repo_slug, state=bitbucket_state
                )

                return [
                    PullRequest(
                        id=str(pr["id"]),
                        title=pr["title"],
                        description=pr.get("description", ""),
                        source_branch=pr["source"]["branch"]["name"],
                        target_branch=pr["destination"]["branch"]["name"],
                        status=pr["state"],
                        created_at=datetime.strptime(
                            pr["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                        updated_at=datetime.strptime(
                            pr["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                        merged_at=datetime.strptime(pr["closed_on"], "%Y-%m-%dT%H:%M:%S.%f%z")
                        if pr.get("closed_on") and pr["state"] == "MERGED"
                        else None,
                        closed_at=datetime.strptime(pr["closed_on"], "%Y-%m-%dT%H:%M:%S.%f%z")
                        if pr.get("closed_on")
                        else None,
                    )
                    for pr in prs
                ]
            except ApiError as e:
                msg = f"Could not get pull requests: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_issue(self, repo_name: str, title: str, description: str = "") -> Issue:
            try:
                workspace, repo_slug = repo_name.split("/")

                issue = self.client.create_issue(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    title=title,
                    description=description,
                    priority="normal",  # Default priority
                    kind="bug",  # Default type
                )

                # Get reporter info
                reporter = issue.get("reporter", {})
                reporter_user = User(
                    username=reporter.get("nickname", ""),
                    name=reporter.get("display_name", ""),
                    email=None,  # Bitbucket API doesn't provide email
                    avatar_url=reporter.get("links", {}).get("avatar", {}).get("href"),
                    created_at=None,  # Not provided by Bitbucket API
                )

                return Issue(
                    id=str(issue["id"]),
                    number=str(issue["id"]),  # Bitbucket uses same value for id and number
                    title=issue["title"],
                    description=issue.get("content", {}).get("raw", ""),
                    state=issue["state"],
                    created_at=datetime.strptime(
                        issue["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    updated_at=datetime.strptime(
                        issue["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    closed_at=None,  # Need to check if state is resolved/closed
                    author=reporter_user,
                    assignee=None,  # Would need to parse assignee if present
                    labels=[],  # Bitbucket doesn't have built-in labels
                    closed=issue["state"]
                    in ["resolved", "closed", "invalid", "duplicate", "wontfix"],
                )
            except ApiError as e:
                msg = f"Could not create issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_issue(self, repo_name: str, issue_id: str) -> Issue:
            """Get issue information.

            Args:
                repo_name: Repository name in format "workspace/repo-slug"
                issue_id: Issue identifier

            Returns:
                Issue object

            Raises:
                ResourceNotFoundError: If issue is not found
            """
            try:
                workspace, repo_slug = repo_name.split("/")

                issue = self.client.get_issue(
                    workspace=workspace, repository_slug=repo_slug, issue_id=issue_id
                )

                # Get reporter info
                reporter = issue.get("reporter", {})
                reporter_user = User(
                    username=reporter.get("nickname", ""),
                    name=reporter.get("display_name", ""),
                    email=None,
                    avatar_url=reporter.get("links", {}).get("avatar", {}).get("href"),
                    created_at=None,
                )

                # Get assignee info if present
                assignee = issue.get("assignee", {})
                assignee_user = None
                if assignee:
                    assignee_user = User(
                        username=assignee.get("nickname", ""),
                        name=assignee.get("display_name", ""),
                        email=None,
                        avatar_url=assignee.get("links", {}).get("avatar", {}).get("href"),
                        created_at=None,
                    )

                return Issue(
                    id=str(issue["id"]),
                    number=str(issue["id"]),
                    title=issue["title"],
                    description=issue.get("content", {}).get("raw", ""),
                    state=issue["state"],
                    created_at=datetime.strptime(
                        issue["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    updated_at=datetime.strptime(
                        issue["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    closed_at=None,  # Bitbucket doesn't provide explicit closed_at
                    author=reporter_user,
                    assignee=assignee_user,
                    labels=[],  # Bitbucket doesn't have built-in labels
                    closed=issue["state"]
                    in ["resolved", "closed", "invalid", "duplicate", "wontfix"],
                )
            except ApiError as e:
                msg = f"Could not get issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def close_issue(self, repo_name: str, issue_id: str) -> bool:
            try:
                workspace, repo_slug = repo_name.split("/")
                self.client.update_issue(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    issue_id=issue_id,
                    state="resolved",
                )
                return True
            except ApiError as e:
                msg = f"Could not close issue: {e!s}"
                raise ResourceNotFoundError(msg)

        def add_comment(
            self, repo_name: str, target_id: str, comment: str, target_type: str = "pr"
        ) -> Comment:
            try:
                workspace, repo_slug = repo_name.split("/")
                if target_type == "pr":
                    response = self.client.add_pull_request_comment(
                        workspace=workspace,
                        repository_slug=repo_slug,
                        pull_request_id=target_id,
                        content=comment,
                    )
                else:
                    response = self.client.add_issue_comment(
                        workspace=workspace,
                        repository_slug=repo_slug,
                        issue_id=target_id,
                        content=comment,
                    )

                return Comment(
                    id=str(response["id"]),
                    body=response["content"]["raw"],
                    author=User(
                        username=response["user"]["nickname"],
                        name=response["user"].get("display_name"),
                        email=None,
                        avatar_url=response["user"]
                        .get("links", {})
                        .get("avatar", {})
                        .get("href"),
                        created_at=datetime.strptime(
                            response["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                    ),
                    created_at=datetime.strptime(
                        response["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                    updated_at=datetime.strptime(
                        response["updated_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                )
            except ApiError as e:
                msg = f"Could not add comment: {e!s}"
                raise ResourceNotFoundError(msg)

        def create_label(
            self, repo_name: str, name: str, color: str, description: str = ""
        ) -> Label:
            # Bitbucket doesn't support labels natively
            return Label(name=name, color=color, description=description)

        def get_commits(self, repo_name: str, branch: str | None = None) -> list[Commit]:
            try:
                workspace, repo_slug = repo_name.split("/")
                commits = self.client.get_commits(
                    workspace=workspace, repository_slug=repo_slug, branch=branch
                )

                return [
                    Commit(
                        sha=commit["hash"],
                        message=commit["message"],
                        author=User(
                            username=commit["author"].get("user", {}).get("nickname", ""),
                            name=commit["author"].get("raw"),
                            email=None,
                            avatar_url=None,
                            created_at=None,
                        ),
                        created_at=datetime.strptime(commit["date"], "%Y-%m-%dT%H:%M:%S%z"),
                    )
                    for commit in commits
                ]
            except ApiError as e:
                msg = f"Could not get commits: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_commit(self, repo_name: str, commit_sha: str) -> Commit:
            try:
                workspace, repo_slug = repo_name.split("/")
                commit = self.client.get_commit(
                    workspace=workspace, repository_slug=repo_slug, revision=commit_sha
                )

                return Commit(
                    sha=commit["hash"],
                    message=commit["message"],
                    author=User(
                        username=commit["author"].get("user", {}).get("nickname", ""),
                        name=commit["author"].get("raw"),
                        email=None,
                        avatar_url=None,
                        created_at=None,
                    ),
                    created_at=datetime.strptime(commit["date"], "%Y-%m-%dT%H:%M:%S%z"),
                )
            except ApiError as e:
                msg = f"Could not get commit: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_user(self) -> User:
            try:
                user = list(self.client.get_users_info())[0]
                return User(
                    username=user["nickname"],
                    name=user.get("display_name"),
                    email=user.get("email"),
                    avatar_url=user.get("links", {}).get("avatar", {}).get("href"),
                    created_at=datetime.strptime(
                        user["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    ),
                )
            except ApiError as e:
                msg = f"Could not get user: {e!s}"
                raise ResourceNotFoundError(msg) from e

        def get_workflows(self, repo_name: str) -> list[Workflow]:
            try:
                workspace, repo_slug = repo_name.split("/")
                pipelines = self.client.get_pipelines(workspace, repo_slug)

                return [
                    Workflow(
                        id=str(pl["uuid"]),
                        name=pl.get("name", f"Pipeline {pl['uuid']}"),
                        path=pl["target"]["ref_name"],
                        state=pl["state"],
                        created_at=datetime.strptime(
                            pl["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                        updated_at=datetime.strptime(
                            pl["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                    )
                    for pl in pipelines
                ]
            except ApiError as e:
                msg = f"Could not get workflows: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow_runs(
            self, repo_name: str, workflow_id: str, branch: str | None = None
        ) -> list[WorkflowRun]:
            try:
                workspace, repo_slug = repo_name.split("/")
                runs = self.client.get_pipeline_steps(workspace, repo_slug, workflow_id)

                return [
                    WorkflowRun(
                        id=str(run["uuid"]),
                        workflow_id=workflow_id,
                        name=run.get("name", f"Run {run['uuid']}"),
                        status=run["state"],
                        conclusion=run["result"]["name"] if run.get("result") else None,
                        created_at=datetime.strptime(
                            run["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        ),
                        updated_at=datetime.strptime(
                            run["completed_on"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        )
                        if run.get("completed_on")
                        else None,
                    )
                    for run in runs
                ]
            except ApiError as e:
                msg = f"Could not get workflow runs: {e!s}"
                raise ResourceNotFoundError(msg)

        def trigger_workflow(
            self,
            repo_name: str,
            workflow_id: str,
            branch: str,
            inputs: dict[str, Any] | None = None,
        ) -> WorkflowRun:
            try:
                workspace, repo_slug = repo_name.split("/")
                run = self.client.trigger_pipeline(
                    workspace=workspace,
                    repository_slug=repo_slug,
                    branch=branch,
                    variables=inputs,
                )

                return WorkflowRun(
                    id=str(run["uuid"]),
                    workflow_id=workflow_id,
                    name=run.get("name", f"Run {run['uuid']}"),
                    status=run["state"],
                    conclusion=None,
                    created_at=datetime.strptime(run["created_on"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    updated_at=None,
                )
            except ApiError as e:
                msg = f"Could not trigger workflow: {e!s}"
                raise ResourceNotFoundError(msg)

        def cancel_workflow_run(self, repo_name: str, run_id: str) -> bool:
            try:
                workspace, repo_slug = repo_name.split("/")
                self.client.stop_pipeline(workspace, repo_slug, run_id)
                return True
            except ApiError as e:
                msg = f"Could not cancel workflow run: {e!s}"
                raise ResourceNotFoundError(msg)

        def get_workflow_run_logs(self, repo_name: str, run_id: str) -> str:
            try:
                workspace, repo_slug = repo_name.split("/")
                logs = self.client.get_pipeline_steps_log(workspace, repo_slug, run_id)
                return "\n".join(log["text"] for log in logs)
            except ApiError as e:
                msg = f"Could not get workflow run logs: {e!s}"
                raise ResourceNotFoundError(msg)
