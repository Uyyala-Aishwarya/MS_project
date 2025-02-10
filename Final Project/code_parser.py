import ast
import os

def parse_code(directory="cloned_repo"):
    """
    Parses the Python codebase in the specified directory to extract functions, classes, and their relationships.
    """
    parsed_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    parsed_data.append({"file": file, "tree": tree})
                    print(f"Parsed file: {file}")
    return parsed_data