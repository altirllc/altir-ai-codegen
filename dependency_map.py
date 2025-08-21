dependency_map = {
    "main_file.py": [
        {"name": "auth.py", "path": "src/core/auth.py"},
        {"name": "main_graph.py", "path": "src/utils/main_graph.py"},
    ],
    "src/core/auth.py": [],
    "src/utils/main_graph.py": [{"name": "config.py", "path": "src/config.py"}],
    "src/config.py": [],
}
