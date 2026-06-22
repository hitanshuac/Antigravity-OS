"""
Antigravity OS - Phase 3 & 4: The Agentic ReAct Loop
A deterministic state machine orchestrating Reason + Act iterations.
Enforces the 3-strike verification loop and Git rollback constraints.
"""

import json
from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass

from src.sandbox.bash import BashExecutionTool
from src.sandbox.git import GitRollbackManager
from src.sandbox.editor import FileEditorTool
from src.context.repomap import RepoMapGenerator


@dataclass
class ToolCall:
    """Standardized representation of an LLM's requested tool execution."""
    tool_name: str
    tool_args: Dict[str, Any]


class LLMClient(Protocol):
    """
    Abstract interface for LLM providers (OpenAI, Anthropic, vLLM).
    Keeps the orchestrator decoupled from proprietary SDKs.
    """
    def generate_response(self, system_prompt: str, messages: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> ToolCall:
        ...


class ReActEngine:
    """
    The core execution loop. Manages state transitions, tool dispatches,
    and the 3-strike verification rollback mechanism.
    """
    def __init__(
        self, 
        workspace_dir: str, 
        llm_client: LLMClient, 
        max_steps: int = 30,
        verification_command: str = "python -m pytest"
    ):
        self.workspace_dir = workspace_dir
        self.llm_client = llm_client
        self.max_steps = max_steps
        self.verification_command = verification_command
        
        # Initialize Sandboxed Tools
        self.bash = BashExecutionTool()
        self.git = GitRollbackManager(workspace_dir)
        self.repo_map_gen = RepoMapGenerator(workspace_dir)
        self.editor = FileEditorTool()
        
        # State Tracking
        self.messages: List[Dict[str, str]] = []
        self.consecutive_failures: int = 0
        self._checkpoint_hash: Optional[str] = None
        
        self.TOOL_SCHEMAS = self._build_tool_schemas()

    def _build_tool_schemas(self) -> List[Dict[str, Any]]:
        """Defines the deterministic action space for the LLM."""
        return [
            {
                "name": "read_file",
                "description": "Reads the complete contents of a local file.",
                "parameters": {
                    "type": "object",
                    "properties": {"filepath": {"type": "string"}},
                    "required": ["filepath"]
                }
            },
            {
                "name": "edit_file_unified_diff",
                "description": "Applies a unified diff patch to a file. Use this to modify code.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string"},
                        "diff_string": {"type": "string"}
                    },
                    "required": ["filepath", "diff_string"]
                }
            },
            {
                "name": "run_bash_command",
                "description": "Executes a shell command. Use this to run tests, linters, or scripts.",
                "parameters": {
                    "type": "object",
                    "properties": {"command": {"type": "string"}},
                    "required": ["command"]
                }
            },
            {
                "name": "task_complete",
                "description": "Signals that the goal has been achieved and verified.",
                "parameters": {
                    "type": "object",
                    "properties": {"summary": {"type": "string"}},
                    "required": ["summary"]
                }
            }
        ]

    def _generate_system_prompt(self) -> str:
        """Compiles the rule set and the current RepoMap into the System Prompt."""
        repo_map = self.repo_map_gen.generate_compact_map()
        return f"""You are Antigravity OS, an autonomous coding agent.
You operate in a strict Reason -> Act loop.

ENVIRONMENT:
- You have access to a sandboxed POSIX-compliant filesystem and terminal.
- Your goal is to write code, verify it via tests, and complete the user's objective.

CONSTRAINTS:
1. Always read files before attempting to edit them.
2. When making changes, use `edit_file_unified_diff`. 
3. After editing, use `run_bash_command` to run tests and verify your changes.
4. If your tests fail 3 times consecutively, the system will HARD RESET your code to the last known good state.

CURRENT REPOSITORY MAP:
{repo_map}
"""

    def _execute_tool(self, call: ToolCall) -> str:
        """Routes tool calls to the sandbox and handles Tier 0 security constraints."""
        name = call.tool_name
        args = call.tool_args

        if name == "read_file":
            try:
                with open(args["filepath"], "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"

        elif name == "edit_file_unified_diff":
            # [PILLAR 4: Git Rollback Constraint]
            # Ensure a pre-agent-edit checkpoint exists before any mutation occurs.
            if not self._checkpoint_hash:
                self._checkpoint_hash = self.git.create_checkpoint("pre-agent-edit")
            
            try:
                self.editor.apply_diff(args["filepath"], args["diff_string"])
                return f"Successfully applied diff to {args['filepath']}."
            except Exception as e:
                return f"Failed to apply diff: {e}"

        elif name == "run_bash_command":
            result = self.bash.execute(args["command"])
            
            # [PILLAR 3: REPL Verification Loop]
            if result.exit_code > 0:
                self.consecutive_failures += 1
                response = f"Command Failed (Exit Code {result.exit_code}).\nStdout: {result.stdout}\nStderr: {result.stderr}"
            else:
                self.consecutive_failures = 0  # Reset on success
                response = f"Command Succeeded.\nStdout: {result.stdout}"
                
            return response

        return f"Unknown tool: {name}"

    def run_task(self, task_objective: str) -> str:
        """
        Executes the continuous ReAct loop until the task is complete, 
        max steps are reached, or a fatal error occurs.
        """
        system_prompt = self._generate_system_prompt()
        self.messages.append({"role": "user", "content": task_objective})

        for step in range(self.max_steps):
            print(f"--- [Step {step + 1}/{self.max_steps}] ---")
            
            # 1. Reason / Act (Call LLM)
            action = self.llm_client.generate_response(system_prompt, self.messages, self.TOOL_SCHEMAS)
            
            if action.tool_name == "task_complete":
                return f"Task Complete: {action.tool_args.get('summary', '')}"

            # Log LLM's intent to the message history
            self.messages.append({
                "role": "assistant",
                "content": f"Calling Tool: {action.tool_name} with {json.dumps(action.tool_args)}"
            })

            # 2. Execute
            tool_output = self._execute_tool(action)
            
            # 3. Handle Rollback Circuit Breaker
            if self.consecutive_failures >= 3 and self._checkpoint_hash:
                print("\n[!] 3 Consecutive Failures Detected. Triggering Git Ripcord...")
                self.git.rollback_to_checkpoint(self._checkpoint_hash)
                
                rollback_msg = (
                    "SYSTEM OVERRIDE: You experienced 3 consecutive command failures. "
                    "Your recent edits have been rolled back to the pre-agent-edit state via Git. "
                    "Analyze the previous errors and try a completely different approach."
                )
                self.messages.append({"role": "system", "content": rollback_msg})
                
                # Reset circuit breaker state
                self.consecutive_failures = 0
                self._checkpoint_hash = None
            else:
                # Append standard tool output
                self.messages.append({"role": "system", "content": f"Tool Output:\n{tool_output}"})

        return "Task failed: Maximum iterations reached."
