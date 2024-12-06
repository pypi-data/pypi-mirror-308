import os
import ast
from pathlib import Path
from typing import Dict, List, Any
import sys
# @hint: stdlib-list (channel=pypi)
from stdlib_list import stdlib_list
# @hint: pyyaml (channel=pypi)
import yaml
import json
import re  # For parsing metadata comments


class PythonDependencyAnalyzer:
    def __init__(
        self,
        extensions: List[str] = ["py"],
        recursive: bool = False,
        python_version: str = None,
    ):
        """
        Initialize the dependency analyzer.

        :param extensions: List of file extensions to consider as Python files.
        :param recursive: Whether to analyze directories recursively.
        :param python_version: Python version to use for standard library detection.
                               If None, defaults to the current runtime version.
        """
        self.extensions = extensions
        self.recursive = recursive
        self.modules = []
        self.parsed_files = set()
        self.used_identifiers = set()  # Track all used identifiers in the code

        # Collect built-in and standard library modules dynamically
        self.builtin_modules = set(sys.builtin_module_names)
        # Use the provided Python version or default to the current version
        self.python_version = (
            python_version or f"{sys.version_info.major}.{sys.version_info.minor}"
        )
        self.standard_modules = set(stdlib_list(self.python_version))

        # Log PYTHONPATH for debugging purposes
        self.python_path_dirs = os.getenv("PYTHONPATH", "").split(os.pathsep)
        print(f"PYTHONPATH: {self.python_path_dirs}")

    def resolve_file_path(self, base_dir: str, file_path: str) -> str:
        """
        Resolve the file path for a Python module, considering PYTHONPATH.
        """
        candidate = Path(base_dir) / file_path
        if candidate.is_file():
            return str(candidate.resolve())
        for ext in self.extensions:
            candidate_with_ext = f"{candidate}.{ext}"
            if Path(candidate_with_ext).is_file():
                return str(Path(candidate_with_ext).resolve())
        # Check PYTHONPATH for module resolution
        for path in self.python_path_dirs:
            candidate = Path(path) / (file_path.replace(".", os.sep) + ".py")
            if candidate.is_file():
                return str(candidate.resolve())
        return None

    def is_local_module(self, import_path: str) -> bool:
        """
        Determine if the import is a local module based on PYTHONPATH.
        """
        for path in self.python_path_dirs:
            candidate = Path(path) / (import_path.replace(".", os.sep) + ".py")
            if candidate.is_file():
                return True
        return import_path.startswith(".")

    def mark_used_identifiers(self, tree: ast.AST):
        """
        Traverse the AST and collect all identifiers that are used in the code.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                self.used_identifiers.add(node.id)
            elif isinstance(node, ast.Attribute):
                self.used_identifiers.add(node.attr)

    def deduplicate_modules(self):
        """
        Remove duplicate entries from the modules list.
        """
        unique_modules = []
        seen_paths = set()
        for mod in self.modules:
            if mod["path"] not in seen_paths:
                unique_modules.append(mod)
                seen_paths.add(mod["path"])
        self.modules = unique_modules

    def extract_comment_metadata(self, line: str) -> Dict[str, str]:
        """
        Extract metadata from comments using a regex.

        Example comment:
        # @hint: pyyaml (channel=pypi, version=^5.4.1)

        :param line: A single line of code or comment.
        :return: A dictionary of parsed metadata or None.
        """
        match = re.match(r"#\s*@hint:\s*([\w-]+)\s*\((.*?)\)", line)
        if match:
            package = match.group(1)
            attributes = dict(
                attr.split("=") for attr in match.group(2).split(",") if "=" in attr
            )
            attributes["package"] = package

            # # Add debug for version if it exists
            # if "version" in attributes:
            #     print(f"DEBUG: Found version -> {attributes['version']} for package {package}")

            return attributes
        return None

    def extract_imports(self, file_path: str):
        """
        Analyze the file and extract imports with metadata hints.
        """
        if file_path in self.parsed_files:
            # Detect circular dependency
            if file_path in [mod["path"] for mod in self.modules if mod["type"] == "local"]:
                print(f"Warning: Circular dependency detected for {file_path}")
            return
        self.parsed_files.add(file_path)

        base_dir = os.path.dirname(file_path)
        self.modules.append(
            {
                "type": "local",
                "path": file_path,
                "imported_by": [],
                "uses_dynamic_imports": False,
            }
        )

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            tree = ast.parse(content)
            self.mark_used_identifiers(tree)
        except SyntaxError as e:
            print(f"Syntax error in file {file_path}: {e}")
            return

        lines = content.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                # Check for a comment directly above the import statement
                metadata = None
                if node.lineno > 1:  # Ensure there are lines above
                    comment_line = lines[node.lineno - 2].strip()
                    metadata = self.extract_comment_metadata(comment_line)

                imported_name = None
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_name = alias.asname or alias.name
                        self.modules.append(
                            {
                                "type": "package",
                                "path": alias.name,
                                "imported_by": [
                                    {
                                        "path": file_path,
                                        "used": imported_name in self.used_identifiers,
                                        "line": node.lineno,
                                    }
                                ],
                                "alias": alias.asname,
                                "metadata": metadata,
                            }
                        )
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module
                    if module_name:
                        for alias in node.names:
                            imported_name = alias.asname or alias.name
                            resolved_path = self.resolve_file_path(base_dir, module_name.replace(".", os.sep))
                            module_type = "local" if resolved_path else "package"
                            module_path = resolved_path if resolved_path else module_name
                            self.modules.append(
                                {
                                    "type": module_type,
                                    "path": module_path,
                                    "imported_by": [
                                        {
                                            "path": file_path,
                                            "used": imported_name in self.used_identifiers,
                                            "line": node.lineno,
                                        }
                                    ],
                                    "alias": alias.asname,
                                    "metadata": metadata,
                                }
                            )


    def group_required_modules(
        self, required_modules: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group required modules by their type for better readability.
        """
        grouped = {"builtin": [], "third-party": [], "local": []}
        for mod in required_modules:
            if mod["type"] == "local":
                grouped["local"].append(mod)
            elif mod["type"] == "package":
                if (
                    mod["path"] in self.builtin_modules
                    or mod["path"] in self.standard_modules
                ):
                    grouped["builtin"].append(mod)
                else:
                    grouped["third-party"].append(mod)
            elif mod["type"] == "dynamic":
                grouped["third-party"].append(mod)
        return grouped

    def analyze(self, entry_file: str) -> Dict[str, Any]:
        """
        Analyze dependencies starting from the entry file.
        """
        resolved_entry = self.resolve_file_path("", entry_file)
        if not resolved_entry:
            return {
                "error": f"File {entry_file} does not exist.",
                "all": [],
                "unreferenced": [],
                "unnecessary": [],
                "required": [],
            }

        self.extract_imports(resolved_entry)
        self.deduplicate_modules()

        all_modules = self.modules
        unreferenced_modules = [
            mod
            for mod in all_modules
            if mod["path"] != resolved_entry
            and all(not imp["used"] for imp in mod["imported_by"])
        ]
        required_modules = [
            mod for mod in all_modules if mod not in unreferenced_modules
        ]
        grouped_required = self.group_required_modules(required_modules)

        return {
            "all": all_modules,
            "unreferenced": unreferenced_modules,
            "unnecessary": unreferenced_modules,
            "required": grouped_required,
        }


def default(**kwargs):
    """
    Default entry point for the dependency analyzer.

    :param kwargs: Arguments for the analysis.
    - entry_file: Path to the entry file for analysis.
    - recursive: Whether to analyze dependencies recursively.
    - python_version: Python version for standard library detection.
    - output_format: Output format for the results ("json" or "yaml").

    :return: Formatted analysis result.
    """
    entry_file = kwargs.get("entry_file")
    if not entry_file:
        raise ValueError("The 'entry_file' parameter is required.")
    
    recursive = kwargs.pop("recursive", True)
    python_version = kwargs.pop("python_version", None)
    output_format = kwargs.pop("output_format", "json").lower()

    analyzer = PythonDependencyAnalyzer(
        recursive=recursive, python_version=python_version
    )
    result = analyzer.analyze(entry_file)

    # Format the result based on the output format
    if output_format == "json":
        return json.dumps(result, indent=2)
    elif output_format == "yaml":
        return yaml.dump(result, default_flow_style=False, allow_unicode=True)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")