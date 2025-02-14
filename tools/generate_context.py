#!/usr/bin/env python3
"""
generate_context.py

Scans all .py files under the src/ directory (ignoring __init__.py and similar files)
and outputs a summary of all top-level functions, classes, and class methods.
For each function/method, only the signature (parameter names and return type, if annotated)
is shown—not the actual code body.

Usage:
    python generate_context.py --src src --output project_context.txt
"""

import os
import ast
import argparse

def format_args(args: ast.arguments) -> str:
    """
    Format the function arguments into a string.
    
    Parameters:
        args (ast.arguments): The AST node containing function arguments.
    
    Returns:
        str: A comma-separated list of parameter names and (if available) annotations.
    """
    arg_strings = []
    
    # Positional and keyword arguments
    for arg in args.args:
        annotation = ""
        if arg.annotation:
            try:
                annotation = ast.unparse(arg.annotation)
            except AttributeError:
                # For Python versions without ast.unparse, skip annotation.
                annotation = ""
        if annotation:
            arg_strings.append(f"{arg.arg}: {annotation}")
        else:
            arg_strings.append(arg.arg)
    
    # *args
    if args.vararg:
        annotation = ""
        if args.vararg.annotation:
            try:
                annotation = ast.unparse(args.vararg.annotation)
            except AttributeError:
                annotation = ""
        if annotation:
            arg_strings.append(f"*{args.vararg.arg}: {annotation}")
        else:
            arg_strings.append(f"*{args.vararg.arg}")
    
    # Keyword-only arguments
    for arg in args.kwonlyargs:
        annotation = ""
        if arg.annotation:
            try:
                annotation = ast.unparse(arg.annotation)
            except AttributeError:
                annotation = ""
        if annotation:
            arg_strings.append(f"{arg.arg}: {annotation}")
        else:
            arg_strings.append(arg.arg)
    
    # **kwargs
    if args.kwarg:
        annotation = ""
        if args.kwarg.annotation:
            try:
                annotation = ast.unparse(args.kwarg.annotation)
            except AttributeError:
                annotation = ""
        if annotation:
            arg_strings.append(f"**{args.kwarg.arg}: {annotation}")
        else:
            arg_strings.append(f"**{args.kwarg.arg}")
    
    return ", ".join(arg_strings)

def format_function_def(func: ast.FunctionDef) -> str:
    """
    Format a function definition into a signature string.
    
    Parameters:
        func (ast.FunctionDef): The function definition node.
    
    Returns:
        str: A string showing the function's name, parameters, and return annotation (if any).
    """
    name = func.name
    params = format_args(func.args)
    ret = ""
    if func.returns:
        try:
            ret = ast.unparse(func.returns)
        except AttributeError:
            ret = ""
    ret_str = f" -> {ret}" if ret else ""
    return f"Function: {name}({params}){ret_str}"

def process_file(filepath: str) -> list:
    """
    Process a Python file to extract top-level functions and classes (with methods).
    
    Parameters:
        filepath (str): The path to the Python file.
    
    Returns:
        list: A list of strings summarizing the functions and classes.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
    except Exception as e:
        return [f"Error parsing {filepath}: {e}"]
    
    items = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # Top-level function
            items.append(format_function_def(node))
        elif isinstance(node, ast.ClassDef):
            class_header = f"Class: {node.name}"
            items.append(class_header)
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Indent methods by four spaces
                    items.append("    " + format_function_def(item))
    return items

# load a specified file with each line as an element in a list
def load_file(filepath: str):
    """
    Load a file and return its contents as a list of lines.
    
    Parameters:
        filepath (str): The path to the file to load.
    
    Returns:
        list: A list of strings, each representing a line from the file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()

def generate_context(src_dir: str) -> str:
    """
    Walk the src directory and generate a summary context for all Python files.
    
    Parameters:
        src_dir (str): The source directory to scan.
    
    Returns:
        str: A string containing the project context summary.
    """

    output_lines = []
    prepend_lines = []
    prepend_files = [
        "../design/01-requirements.md",
        "../design/02-tech-stack.md",
        "../design/03-application.md",
        "../design/04-frontend.md",
        "../design/05-backend.md"
    ]

    for file in prepend_files:
        prepend_lines.extend(load_file(file))
        prepend_lines.append("\n")

    output_lines.append("# Top-Level Functions and Classes")
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py") and file not in ("__init__.py",):
                filepath = os.path.join(root, file)
                output_lines.append(f"File: {filepath}")
                output_lines.append("-" * (len(filepath) + 6))
                items = process_file(filepath)
                if items:
                    output_lines.extend(items)
                else:
                    output_lines.append("    No classes or functions found.")
                output_lines.append("")  # Empty line between files
    return "".join(prepend_lines) + "\n".join(output_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a project context summary from the src/ directory."
    )
    parser.add_argument("--src", default="../app", help="Source directory to scan (default: src)")
    parser.add_argument("--output", default="../project-context.md",
                        help="Output file to write the context summary (default: project_context.txt)")
    args = parser.parse_args()
    
    context = generate_context(args.src)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(context)
    print(f"Project context summary written to {args.output}")

if __name__ == "__main__":
    main()
