import os
import tempfile
import shutil
import subprocess
import unittest
from typing import List, Dict, Any

from src.orchestrator.engine import ReActEngine, ToolCall


class MockLLMClient:
    """
    A deterministic dummy client that replays a pre-defined sequence of tool calls.
    Used to simulate agent behavior without relying on external API calls.
    """
    def __init__(self, scheduled_actions: List[ToolCall]):
        self.scheduled_actions = scheduled_actions
        self.call_count = 0

    def generate_response(self, system_prompt: str, messages: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> ToolCall:
        if self.call_count >= len(self.scheduled_actions):
            raise RuntimeError("Mock LLM ran out of scheduled actions!")
        action = self.scheduled_actions[self.call_count]
        self.call_count += 1
        return action


class TestReActEngine(unittest.TestCase):
    def setUp(self):
        # 1. Create an isolated workspace
        self.test_dir = tempfile.mkdtemp()
        
        # 2. Initialize a pristine Git repository (Required by GitRollbackManager)
        subprocess.run(["git", "init"], cwd=self.test_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.test_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@antigravity.os"], cwd=self.test_dir, check=True)
        
        # 3. Create a clean initial file state
        self.file_path = os.path.join(self.test_dir, "app.py")
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("def run():\n    pass\n")
            
        subprocess.run(["git", "add", "app.py"], cwd=self.test_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial baseline"], cwd=self.test_dir, check=True)

    def tearDown(self):
        import stat
        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        # Clean up sandbox workspace
        shutil.rmtree(self.test_dir, onerror=remove_readonly)

    def test_3_strike_git_ripcord(self):
        """
        Simulates an agent breaking the code, failing to fix it 3 times, 
        getting forcefully rolled back, and then succeeding.
        """
        
        # Unified diff patches that match our strict editor tool requirements
        diff_bad = (
            "@@ -1,2 +1,2 @@\n"
            " def run():\n"
            "-    pass\n"
            "+    syntax error!!!"
        )
        
        diff_good = (
            "@@ -1,2 +1,2 @@\n"
            " def run():\n"
            "-    pass\n"
            "+    return True"
        )
        
        # Scheduled Actions: The "Rogue Agent" Sequence
        actions = [
            # Step 1: Agent writes a deliberate syntax error
            ToolCall("edit_file_unified_diff", {"filepath": self.file_path, "diff_string": diff_bad}),
            
            # Step 2: Agent attempts to run it, fails (Strike 1)
            ToolCall("run_bash_command", {"command": "python -c 'import app'"}),
            
            # Step 3: Agent tries to run it again, fails (Strike 2)
            ToolCall("run_bash_command", {"command": "python -c 'import app'"}),
            
            # Step 4: Agent tries a 3rd time, fails (Strike 3 -> Triggers Git Ripcord!)
            ToolCall("run_bash_command", {"command": "python -c 'import app'"}),
            
            # Step 5: (Post-Rollback) Agent writes correct code
            ToolCall("edit_file_unified_diff", {"filepath": self.file_path, "diff_string": diff_good}),
            
            # Step 6: Agent runs it successfully (Exit Code 0 resets the counter)
            ToolCall("run_bash_command", {"command": "python -c 'import app'"}),
            
            # Step 7: Agent declares victory
            ToolCall("task_complete", {"summary": "Fixed the bug."}),
        ]
        
        client = MockLLMClient(actions)
        engine = ReActEngine(workspace_dir=self.test_dir, llm_client=client)
        
        # Execute the loop
        final_result = engine.run_task("Write a working run function.")
        
        # --- VERIFICATIONS ---
        
        # 1. Verify Task Complete was reached
        self.assertEqual(final_result, "Task Complete: Fixed the bug.")
        
        # 2. Verify the System Override (Ripcord) message was injected into the LLM context
        override_triggered = any(
            "SYSTEM OVERRIDE" in msg.get("content", "") 
            for msg in engine.messages
        )
        self.assertTrue(override_triggered, "The 3-strike Git Ripcord failed to trigger.")
        
        # 3. Verify the final file state is the 'good' patch, meaning rollback happened 
        #    and the bad patch was successfully overwritten later.
        with open(self.file_path, "r", encoding="utf-8") as f:
            final_content = f.read()
            
        self.assertIn("return True", final_content)
        self.assertNotIn("syntax error!!!", final_content)


if __name__ == "__main__":
    unittest.main()
