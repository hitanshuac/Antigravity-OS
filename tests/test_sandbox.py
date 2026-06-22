import pytest
import platform
from src.sandbox.bash import BashExecutionTool
from src.sandbox.git import GitRollbackManager
from src.sandbox.editor import FileEditorTool

def test_bash_execution_basic():
    tool = BashExecutionTool()
    # Simple echo command
    if platform.system() == "Windows":
        cmd = "echo Hello World"
    else:
        cmd = "echo 'Hello World'"
    
    result = tool.execute(cmd)
    assert result.exit_code == 0
    assert "Hello World" in result.stdout
    assert result.timed_out is False

def test_editor_normalize():
    assert FileEditorTool._normalize_line("  hello \n") == "hello"
    assert FileEditorTool._normalize_line("\tworld\r\n") == "world"

def test_git_init_validation(tmp_path):
    # This path is not a git repo, so GitRollbackManager should raise ValueError
    with pytest.raises(ValueError, match="not a valid Git repository"):
        GitRollbackManager(str(tmp_path))
