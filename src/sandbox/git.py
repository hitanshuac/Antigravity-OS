"""
Git-based state manager providing atomic checkpoints and absolute rollbacks.
"""

import os
import subprocess
from typing import List


class GitRollbackManager:
    """
    Tracks workspace changes, commits checkpoints, and resets state.
    Asserts that the initial repository state is pristine.
    """
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        self._validate_repository()
        
        # Hard-fail check: Protects unsaved user files from destructive reset commands
        if self.is_dirty():
            raise RuntimeError(
                "Safety Constraint Failed: The repository contains uncommitted changes. "
                "To prevent accidental loss of unsaved work, the agent cannot execute "
                "until modifications are committed or stashed."
            )

    def _validate_repository(self) -> None:
        """Ensures Git is accessible and repo_path is a valid repository."""
        if not os.path.isdir(self.repo_path):
            raise ValueError(f"Directory path does not exist: {self.repo_path}")
        
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError("Git CLI is not installed or not found in system PATH.") from e

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip() != "true":
                raise ValueError(f"Target directory is not inside a git work tree: {self.repo_path}")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Target directory is not a valid Git repository: {self.repo_path}") from e

    def _run_git_command(self, args: List[str]) -> str:
        """Helper to run git commands with structured error propagation."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            stderr_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Git command failed: git {' '.join(args)}. Error: {stderr_msg}") from e

    def is_dirty(self) -> bool:
        """Returns True if there are untracked or modified files in the repository."""
        status = self._run_git_command(["status", "--porcelain"])
        return len(status) > 0

    def create_checkpoint(self, message: str = "pre-agent-edit") -> str:
        """
        Stages all local files (untracked and tracked) and commits them.
        Injects a generic Git author config locally to handle empty environmental variables.
        """
        self._run_git_command(["add", "-A"])
        
        commit_args = [
            "-c", "user.name=Antigravity OS Agent",
            "-c", "user.email=agent@antigravity.os",
            "commit",
            "-m", message,
            "--allow-empty"
        ]
        self._run_git_command(commit_args)
        return self._run_git_command(["rev-parse", "HEAD"])

    def rollback_to_checkpoint(self, commit_hash: str) -> None:
        """
        Performs a hard reset to the specific checkpoint, and runs a forceful clean
        to delete any new or untracked directory assets created by the agent.
        """
        self._run_git_command(["reset", "--hard", commit_hash])
        self._run_git_command(["clean", "-fd"])
