import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Optional


def generate_dependency_map(project_root: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Generate a dependency map for a project containing Python, JavaScript, TypeScript files.
    
    Args:
        project_root: Path to the project root directory
        
    Returns:
        Dictionary mapping file paths to their dependencies
    """
    project_path = Path(project_root)
    dependency_map = {}
    
    # Find all source files
    source_files = find_source_files(project_path)
    
    # Process each file to extract dependencies
    for file_path in source_files:
        relative_path = str(file_path.relative_to(project_path))
        dependencies = extract_dependencies(file_path, project_path)
        # Remove duplicates while preserving order
        unique_dependencies = []
        seen_paths = set()
        for dep in dependencies:
            if dep['path'] not in seen_paths:
                unique_dependencies.append(dep)
                seen_paths.add(dep['path'])
        dependency_map[relative_path] = unique_dependencies
    
    return dependency_map


def find_source_files(project_path: Path) -> List[Path]:
    """Find all Python, JavaScript, TypeScript source files in the project."""
    extensions = {'.py', '.js', '.jsx', '.ts', '.tsx'}
    source_files = []
    
    # Common directories to ignore
    ignore_dirs = {
        'node_modules', '__pycache__', '.git', '.venv', 'venv', 
        'env', 'dist', 'build', '.next', 'coverage', '.pytest_cache'
    }
    
    for file_path in project_path.rglob('*'):
        # Skip if in ignored directory
        if any(ignored in file_path.parts for ignored in ignore_dirs):
            continue
            
        if file_path.is_file() and file_path.suffix in extensions:
            source_files.append(file_path)
    
    return source_files


def extract_dependencies(file_path: Path, project_root: Path) -> List[Dict[str, str]]:
    """Extract dependencies from a source file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return []
    
    if file_path.suffix == '.py':
        return extract_python_dependencies(content, file_path, project_root)
    elif file_path.suffix in {'.js', '.jsx', '.ts', '.tsx'}:
        return extract_js_ts_dependencies(content, file_path, project_root)
    
    return []


def extract_python_dependencies(content: str, file_path: Path, project_root: Path) -> List[Dict[str, str]]:
    """Extract Python import dependencies."""
    dependencies = []
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Fallback to regex parsing if AST fails
        return extract_python_dependencies_regex(content, file_path, project_root)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dep_path = resolve_python_import(alias.name, file_path, project_root)
                if dep_path:
                    dependencies.append({
                        "name": Path(dep_path).name,
                        "path": dep_path
                    })
        
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                dep_path = resolve_python_import(node.module, file_path, project_root)
                if dep_path:
                    dependencies.append({
                        "name": Path(dep_path).name,
                        "path": dep_path
                    })
    
    return dependencies


def extract_python_dependencies_regex(content: str, file_path: Path, project_root: Path) -> List[Dict[str, str]]:
    """Fallback regex-based Python import extraction."""
    dependencies = []
    
    # Match import statements
    import_patterns = [
        r'^import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
        r'^from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import'
    ]
    
    for line in content.split('\n'):
        line = line.strip()
        for pattern in import_patterns:
            match = re.match(pattern, line)
            if match:
                module_name = match.group(1)
                dep_path = resolve_python_import(module_name, file_path, project_root)
                if dep_path:
                    dependencies.append({
                        "name": Path(dep_path).name,
                        "path": dep_path
                    })
    
    return dependencies


def extract_js_ts_dependencies(content: str, file_path: Path, project_root: Path) -> List[Dict[str, str]]:
    """Extract JavaScript/TypeScript import dependencies."""
    dependencies = []
    
    # Patterns for different import styles
    patterns = [
        # import ... from '...'
        r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
        # import '...'
        r"import\s+['\"]([^'\"]+)['\"]",
        # require('...')
        r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        # import('...')
        r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            dep_path = resolve_js_ts_import(match, file_path, project_root)
            if dep_path:
                dependencies.append({
                    "name": Path(dep_path).name,
                    "path": dep_path
                })
    
    return dependencies


def resolve_python_import(module_name: str, current_file: Path, project_root: Path) -> Optional[str]:
    """Resolve Python import to actual file path."""
    # Skip standard library and third-party imports
    if not module_name.startswith('.') and '.' not in module_name:
        return None
    
    # Handle relative imports
    if module_name.startswith('.'):
        current_dir = current_file.parent
        parts = module_name.split('.')
        
        # Count leading dots for relative level
        level = 0
        for part in parts:
            if part == '':
                level += 1
            else:
                break
        
        # Go up directories based on level
        target_dir = current_dir
        for _ in range(level - 1):
            target_dir = target_dir.parent
        
        # Add remaining module path
        remaining_parts = [p for p in parts if p]
        if remaining_parts:
            target_dir = target_dir / '/'.join(remaining_parts)
    else:
        # Handle absolute imports within project
        parts = module_name.split('.')
        target_dir = project_root
        for part in parts:
            target_dir = target_dir / part
    
    # Try different file extensions
    possible_files = [
        target_dir.with_suffix('.py'),
        target_dir / '__init__.py'
    ]
    
    for possible_file in possible_files:
        if possible_file.exists() and possible_file.is_relative_to(project_root):
            return str(possible_file.relative_to(project_root))
    
    return None


def resolve_js_ts_import(import_path: str, current_file: Path, project_root: Path) -> Optional[str]:
    """Resolve JavaScript/TypeScript import to actual file path."""
    # Skip node_modules and external packages
    if not import_path.startswith('.') and not import_path.startswith('/'):
        return None
    
    current_dir = current_file.parent
    
    if import_path.startswith('./') or import_path.startswith('../'):
        # Relative import
        target_path = (current_dir / import_path).resolve()
    elif import_path.startswith('/'):
        # Absolute import from project root
        target_path = project_root / import_path[1:]
    else:
        return None
    
    # Try different extensions
    extensions = ['.js', '.jsx', '.ts', '.tsx', '.json']
    
    # If path already has extension, try it first
    if target_path.suffix in extensions:
        if target_path.exists() and target_path.is_relative_to(project_root):
            return str(target_path.relative_to(project_root))
    
    # Try adding extensions
    for ext in extensions:
        test_path = target_path.with_suffix(ext)
        if test_path.exists() and test_path.is_relative_to(project_root):
            return str(test_path.relative_to(project_root))
    
    # Try index files in directory
    if target_path.is_dir():
        for ext in extensions:
            index_file = target_path / f'index{ext}'
            if index_file.exists() and index_file.is_relative_to(project_root):
                return str(index_file.relative_to(project_root))
    
    return None

# Hardcoded dependency map for reference
# dependency_map = {
#     "main_file.py": [
#         {"name": "auth.py", "path": "src/core/auth.py"},
#         {"name": "main_graph.py", "path": "src/utils/main_graph.py"},
#     ],
#     "src/core/auth.py": [],
#     "src/utils/main_graph.py": [{"name": "config.py", "path": "src/config.py"}],
#     "src/config.py": [],
# }
