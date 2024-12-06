
    @abstractmethod
        def create_repository(
            self,
            name: str,
            private: bool = False,
            description: str = "",
            **kwargs,
        ) -> Repository:
            """Create a new repository."""

        @abstractmethod
        def delete_repository(self, repo_name: str) -> bool:
            """Delete a repository."""

        # Branch Operations
        @abstractmethod
        def get_branches(self, repo_name: str) -> list[Branch]:
            """Get all branches in the repository."""

        @abstractmethod
        def create_branch(
            self, repo_name: str, branch_name: str, source_branch: str
        ) -> Branch:
            """Create a new branch from source branch."""

        @abstractmethod
        def delete_branch(self, repo_name: str, branch_name: str) -> bool:
            """Delete a branch."""

        @abstractmethod
        def protect_branch(self, repo_name: str, branch_name: str) -> bool:
            """Enable branch protection."""

        # Pull Request Operations
        @abstractmethod
        def create_pull_request(
            self,
            repo_name: str,
            source_branch: str,
            target_branch: str,
            title: str,
            description: str = "",
        ) -> PullRequest:
            """Create a new pull request."""

        @abstractmethod
        def get_pull_request(self, repo_name: str, pr_id: str) -> PullRequest:
            """Get pull request information."""

        @abstractmethod
        def merge_pull_request(self, repo_name: str, pr_id: str) -> bool:
            """Merge a pull request."""

        @abstractmethod
        def get_pull_requests(self, repo_name: str, state: str = "open") -> list[PullRequest]:
            """Get all pull requests in a repository."""

        # Issue Operations
        @abstractmethod
        def create_issue(self, repo_name: str, title: str, description: str = "") -> Issue:
            """Create a new issue."""

        @abstractmethod
        def get_issue(self, repo_name: str, issue_id: str) -> Issue:
            """Get issue information."""

        @abstractmethod
        def close_issue(self, repo_name: str, issue_id: str) -> bool:
            """Close an issue."""

        # Comment Operations
        @abstractmethod
        def add_comment(
            self, repo_name: str, target_id: str, comment: str, target_type: str = "pr"
        ) -> Comment:
            """Add a comment to a PR or issue."""

        @abstractmethod
        def get_comments(
            self, repo_name: str, target_id: str, target_type: str = "pr"
        ) -> list[Comment]:
            """Get comments from a PR or issue."""

        # Label Operations
        @abstractmethod
        def create_label(
            self, repo_name: str, name: str, color: str, description: str = ""
        ) -> Label:
            """Create a new label."""

        @abstractmethod
        def add_labels(
            self, repo_name: str, target_id: str, labels: list[str], target_type: str = "pr"
        ) -> list[Label]:
            """Add labels to a PR or issue."""

        # Commit Operations
        @abstractmethod
        def get_commits(self, repo_name: str, branch: str | None = None) -> list[Commit]:
            """Get commit history."""

        @abstractmethod
        def get_commit(self, repo_name: str, commit_sha: str) -> Commit:
            """Get specific commit information."""

        # User Operations
        @abstractmethod
        def get_user(self) -> User:
            """Get authenticated user information."""

        @abstractmethod
        def get_collaborators(self, repo_name: str) -> list[User]:
            """Get repository collaborators."""

        @abstractmethod
        def add_collaborator(
            self, repo_name: str, username: str, permission: str = "pull"
        ) -> bool:
            """Add a collaborator to repository."""

        # Workflow Operations
        @abstractmethod
        def get_workflows(self, repo_name: str) -> list[Workflow]:
            """Get all workflows in a repository."""

        @abstractmethod
        def get_workflow(self, repo_name: str, workflow_id: str) -> Workflow:
            """Get specific workflow information."""

        @abstractmethod
        def get_workflow_runs(
            self, repo_name: str, workflow_id: str, branch: str | None = None
        ) -> list[WorkflowRun]:
            """Get workflow runs."""

        @abstractmethod
        def trigger_workflow(
            self,
            repo_name: str,
            workflow_id: str,
            branch: str,
            inputs: dict[str, Any] | None = None,
        ) -> WorkflowRun:
            """Trigger a workflow run."""

        @abstractmethod
        def cancel_workflow_run(self, repo_name: str, run_id: str) -> bool:
            """Cancel a workflow run."""

        @abstractmethod
        def get_workflow_run_logs(self, repo_name: str, run_id: str) -> str:
            """Get logs from a workflow run."""
