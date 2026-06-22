"""
Strict unified-diff parser and atomic file editor.
Features fallback semantic alignment to survive LLM formatting hallucinations.
"""

import os
import re
import tempfile
from typing import List, Dict, Any, Optional


class FileEditorTool:
    """
    Reads local files, parses unified diff strings, validates file context semantically,
    and performs atomic swaps to commit edits safely.
    """
    
    @staticmethod
    def _normalize_line(line: str) -> str:
        """Strips all whitespaces and line endings to compare semantic equivalence."""
        return "".join(line.split())

    @staticmethod
    def _parse_unified_diff(diff_content: str) -> List[Dict[str, Any]]:
        """Parses unified diff hunks into context and modification components."""
        hunks: List[Dict[str, Any]] = []
        current_hunk: Optional[Dict[str, Any]] = None
        
        hunk_re = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*')
        diff_lines = diff_content.splitlines(keepends=True)
        
        for line in diff_lines:
            match = hunk_re.match(line)
            if match:
                if current_hunk:
                    hunks.append(current_hunk)
                old_start = int(match.group(1))
                old_len = int(match.group(2)) if match.group(2) is not None else 1
                new_start = int(match.group(3))
                new_len = int(match.group(4)) if match.group(4) is not None else 1
                current_hunk = {
                    'old_start': old_start,
                    'old_len': old_len,
                    'new_start': new_start,
                    'new_len': new_len,
                    'lines': []
                }
            elif current_hunk is not None:
                if line.startswith(('+', '-', ' ', '\\')):
                    current_hunk['lines'].append(line)
                elif line in ('\n', '\r\n'):
                    current_hunk['lines'].append(' ' + line)
                else:
                    hunks.append(current_hunk)
                    current_hunk = None
                    
        if current_hunk:
            hunks.append(current_hunk)
            
        return hunks

    @classmethod
    def apply_patch_to_string(cls, original_code: str, diff_content: str, strict: bool = False) -> str:
        """
        Parses and applies patches to a string representation of file contents.
        Validates target segments line-by-line prior to editing.
        """
        original_lines = original_code.splitlines(keepends=True)
        hunks = cls._parse_unified_diff(diff_content)
        
        if not hunks:
            return original_code

        # Sort hunks in descending order by old_start to preserve index offsets
        hunks.sort(key=lambda h: h['old_start'], reverse=True)
        modified_lines = list(original_lines)
        
        for hunk in hunks:
            old_start = hunk['old_start']
            old_len = hunk['old_len']
            hunk_lines = hunk['lines']
            
            # Map 1-based index (diff convention) to 0-based array index
            start_idx = max(0, old_start - 1)
            
            if start_idx + old_len > len(modified_lines):
                raise ValueError(
                    f"Diff hunk bounds [{old_start}, {old_start + old_len}] are out of range. "
                    f"Target file has only {len(modified_lines)} lines."
                )
                
            expected_original: List[str] = []
            new_replacement: List[str] = []
            
            for idx, h_line in enumerate(hunk_lines):
                if h_line.startswith(' '):
                    expected_original.append(h_line[1:])
                    new_replacement.append(h_line[1:])
                elif h_line.startswith('-'):
                    expected_original.append(h_line[1:])
                elif h_line.startswith('+'):
                    new_replacement.append(h_line[1:])
                elif h_line.startswith('\\'):
                    # Strip newlines on preceding outputs when EOF warnings are encountered
                    if idx > 0:
                        prev = hunk_lines[idx - 1]
                        if prev.startswith('-') and expected_original:
                            expected_original[-1] = expected_original[-1].rstrip('\r\n')
                        elif prev.startswith('+') and new_replacement:
                            new_replacement[-1] = new_replacement[-1].rstrip('\r\n')
                        elif prev.startswith(' '):
                            if expected_original:
                                expected_original[-1] = expected_original[-1].rstrip('\r\n')
                            if new_replacement:
                                new_replacement[-1] = new_replacement[-1].rstrip('\r\n')

            # Extract target code block to compare
            actual_segment = modified_lines[start_idx : start_idx + old_len]
            actual_stripped = [line.rstrip('\r\n') for line in actual_segment]
            expected_stripped = [line.rstrip('\r\n') for line in expected_original]
            
            # Perform exact check first to maintain strict safety
            if actual_stripped != expected_stripped:
                if strict:
                    raise ValueError(
                        f"Line content mismatch at file line {old_start}.\n"
                        f"Expected structure:\n{''.join(expected_original)}\n"
                        f"Actual structure:\n{''.join(actual_segment)}"
                    )
                else:
                    # Semantic validation fallback to survive LLM indentation and formatting issues
                    actual_normalized = [cls._normalize_line(line) for line in actual_segment]
                    expected_normalized = [cls._normalize_line(line) for line in expected_original]
                    if actual_normalized != expected_normalized:
                        raise ValueError(
                            f"Semantic content mismatch at file line {old_start}.\n"
                            f"Expected structure:\n{''.join(expected_original)}\n"
                            f"Actual structure:\n{''.join(actual_segment)}"
                        )
            
            # Use matching line termination formats
            line_ending = '\n'
            if actual_segment and actual_segment[0].endswith('\r\n'):
                line_ending = '\r\n'
                
            final_replacement: List[str] = []
            for r_idx, r_line in enumerate(new_replacement):
                stripped = r_line.rstrip('\r\n')
                if r_idx == len(new_replacement) - 1:
                    if expected_original and not expected_original[-1].endswith('\n'):
                        final_replacement.append(stripped)
                    else:
                        final_replacement.append(stripped + line_ending)
                else:
                    final_replacement.append(stripped + line_ending)
                    
            modified_lines[start_idx : start_idx + old_len] = final_replacement
            
        return "".join(modified_lines)

    @classmethod
    def apply_diff(cls, filepath: str, diff_string: str, strict: bool = False) -> None:
        """
        Reads, applies patches, and writes to target files atomically.
        Refuses to modify target paths resolved as symbolic links to prevent security issues.
        """
        target_path = os.path.abspath(filepath)
        
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Target path does not exist: {target_path}")
        if os.path.islink(target_path):
            raise ValueError(f"Target path is a symbolic link. Operations terminated: {target_path}")
        if not os.path.isfile(target_path):
            raise ValueError(f"Target path is not a standard file: {target_path}")

        with open(target_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        new_content = cls.apply_patch_to_string(original_content, diff_string, strict=strict)

        # Write to temporary file in the same directory to allow atomic replacement
        dir_name = os.path.dirname(target_path) or "."
        fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix=".tmp_antigravity_", suffix=".py")
        
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as tmp_file:
                tmp_file.write(new_content)
            # Perform atomic swap operation
            os.replace(temp_path, target_path)
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise IOError(f"Failed to atomically write patch edits to {target_path}: {e}") from e
