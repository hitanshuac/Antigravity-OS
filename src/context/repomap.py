"""
Antigravity OS - Phase 2: The Repo Map (Context Engine)
Parses the repository AST structure, filters ignored paths, and builds
a compressed map of classes, functions, and signatures.
"""

import ast
import fnmatch
import os
from typing import Dict, List, Any


class GitIgnoreFilter:
    """
    Parses `.gitignore` directives and applies exclusion logic 
    to prevent indexing virtual environments, caches, and configuration directories.
    """
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[str]:
        # Baseline exclusions to guarantee performance safety
        patterns = [
            ".git/", 
            "__pycache__/", 
            "*.pyc", 
            "*.pyo", 
            "*.pyd",
            ".venv/", 
            "venv/", 
            "env/", 
            ".pytest_cache/", 
            ".ruff_cache/",
            ".tmp_antigravity_*"
        ]
        
        gitignore_path = os.path.join(self.root_path, ".gitignore")
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            patterns.append(line)
            except Exception:
                # Fallback to defaults if gitignore is unreadable
                pass
        return patterns

    def is_ignored(self, filepath: str) -> bool:
        """Determines if a given file path matches any exclusion patterns."""
        abs_path = os.path.abspath(filepath)
        rel_path = os.path.relpath(abs_path, self.root_path)
        
        # Standardize slashes for cross-platform matching
        normalized_rel_path = rel_path.replace(os.sep, "/")
        filename = os.path.basename(normalized_rel_path)

        for pattern in self.patterns:
            # Handle directory-level patterns
            if pattern.endswith("/"):
                clean_pattern = pattern.rstrip("/")
                if normalized_rel_path.startswith(clean_pattern + "/") or normalized_rel_path == clean_pattern:
                    return True
            
            # Check relative file paths and direct file names
            if fnmatch.fnmatch(normalized_rel_path, pattern) or fnmatch.fnmatch(filename, pattern):
                return True
                
        return False


class PythonASTParser:
    """
    Analyzes Python source files using abstract syntax trees to locate class 
    definitions, method signatures, functions, and associated line offsets.
    """
    
    @staticmethod
    def extract_symbols(source_code: str) -> Dict[str, Any]:
        """
        Parses source code into an AST and extracts structured definitions.
        Safely returns empty structures if syntax errors are encountered.
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            # Skip unparseable files gracefully
            return {"classes": [], "functions": []}

        symbols: Dict[str, Any] = {
            "classes": [],
            "functions": []
        }

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [],
                    "lineno": node.lineno
                }
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        # Extract the method arguments signature
                        try:
                            args_sig = ast.unparse(subnode.args)
                            returns_sig = f" -> {ast.unparse(subnode.returns)}" if getattr(subnode, 'returns', None) else ""
                        except Exception:
                            args_sig = ""
                            returns_sig = ""
                        
                        class_info["methods"].append({
                            "name": subnode.name,
                            "args": args_sig,
                            "returns": returns_sig,
                            "lineno": subnode.lineno
                        })
                symbols["classes"].append(class_info)
                
            elif isinstance(node, ast.FunctionDef):
                try:
                    args_sig = ast.unparse(node.args)
                    returns_sig = f" -> {ast.unparse(node.returns)}" if getattr(node, 'returns', None) else ""
                except Exception:
                    args_sig = ""
                    returns_sig = ""
                    
                symbols["functions"].append({
                    "name": node.name,
                    "args": args_sig,
                    "returns": returns_sig,
                    "lineno": node.lineno
                })
                
        return symbols


class RepoMapGenerator:
    """
    Scans the repository, applies filters, and compiles a highly
    compressed structural layout of files and internal symbols.
    """
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        self.filter = GitIgnoreFilter(self.root_path)

    def scan_repository(self) -> Dict[str, Dict[str, Any]]:
        """Walks the file system and processes unignored Python files."""
        repo_map: Dict[str, Dict[str, Any]] = {}
        
        for dirpath, _, filenames in os.walk(self.root_path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                
                # Exclude based on gitignore policies
                if self.filter.is_ignored(full_path):
                    continue
                
                # Only process Python source files for AST parsing
                if filename.endswith(".py"):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        symbols = PythonASTParser.extract_symbols(content)
                        
                        # Use a clean relative path representation
                        rel_path = os.path.relpath(full_path, self.root_path)
                        repo_map[rel_path] = symbols
                    except Exception:
                        # Fail-safe against unreadable files
                        pass
                        
        return repo_map

    def generate_compact_map(self) -> str:
        """
        Compiles the scanned structural representation into a compact outline
        suitable for feeding directly into LLM contexts.
        """
        raw_map = self.scan_repository()
        lines: List[str] = []
        
        for file_path, data in sorted(raw_map.items()):
            # Only represent files that contain definable signatures
            if not data["classes"] and not data["functions"]:
                continue
                
            lines.append(f"{file_path}:")
            
            # Map out classes and class methods
            for cls in data["classes"]:
                lines.append(f"  class {cls['name']}:")
                for method in cls["methods"]:
                    lines.append(f"    def {method['name']}({method['args']}){method.get('returns', '')}")
            
            # Map out free-standing module functions
            for func in data["functions"]:
                lines.append(f"  def {func['name']}({func['args']}){func.get('returns', '')}")
                
            lines.append("")  # Spacing delimiter between file outlines
            
        return "\n".join(lines).strip()
