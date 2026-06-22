import datetime
import json
import os
import subprocess
import sys

ERROR_LOG_PATH = "data/error_logs.json"


def log_error(command, stderr):
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)

    error_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "error_type": "Git CLI Error",
        "component": command,
        "stack_trace_summary": stderr.strip() if stderr else "Unknown error",
        "status": "UNRESOLVED",
        "resolution_strategy": "",
    }

    try:
        if os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH) as f:
                content = f.read().strip()
                if content.startswith("[") and content.endswith("]"):
                    logs = json.loads(content)
                else:
                    # Fix mixed JSON arrays and JSON lines format
                    logs = []
                    for line in content.splitlines():
                        line = line.strip()
                        if line.startswith("{") and line.endswith("}"):
                            logs.append(json.loads(line))
        else:
            logs = []
    except Exception:
        logs = []

    logs.append(error_entry)

    with open(ERROR_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)


def run_git(args):
    print(f"Running: git {' '.join(args)}")
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr
        print(f"Git command failed:\n{stderr}")
        log_error(f"git {' '.join(args)}", stderr)
        return False, stderr
    return True, result.stdout


def handle_checkpoint(message):
    print("Staging files...")
    success, _ = run_git(["add", "."])
    if not success:
        return False

    print("Committing files...")
    success, stdout = run_git(["commit", "-m", f"[Safe Checkpoint] {message}"])
    if not success and "nothing to commit" not in stdout.lower():
        # A commit might fail if there's nothing to commit, which isn't necessarily an error
        print("Commit failed or nothing to commit.")

    print("Pushing to remote...")
    success, stderr = run_git(["push", "origin", "main"])
    if not success:
        # Check if it's a divergence error
        if "fetch first" in stderr or "git pull" in stderr or "non-fast-forward" in stderr or "rejected" in stderr:
            print("Divergent branches detected. Auto-recovering with 'git pull --rebase'...")
            success, _ = run_git(["pull", "--rebase", "origin", "main"])
            if success:
                print("Rebase successful. Retrying push...")
                success, _ = run_git(["push", "origin", "main"])
                if success:
                    print("Push successful after auto-recovery.")
                    return True
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/capabilities/git_manager.py [checkpoint <message> | <git_command>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "checkpoint":
        message = sys.argv[2] if len(sys.argv) > 2 else "auto checkpoint"
        if handle_checkpoint(message):
            print("Checkpoint secured successfully.")
            sys.exit(0)
        else:
            print("Checkpoint failed. Errors have been logged to data/error_logs.json.")
            sys.exit(1)
    else:
        # Passthrough other git commands
        success, _ = run_git(sys.argv[1:])
        sys.exit(0 if success else 1)
