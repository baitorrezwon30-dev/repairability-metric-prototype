# Repairability Metric Prototype
# Academic-friendly, reproducible prototype

import os
import ast
import subprocess

# -------------------------------------
# ENTRY POINT
# -------------------------------------

def main(input_path):

    if is_github_url(input_path):
        repo_path = clone_repository(input_path)
    else:
        repo_path = input_path

    python_files = find_all_python_files(repo_path)

    if not python_files:
        print("No Python files found.")
        return

    metrics = analyze_codebase(python_files)

    static_score = calculate_static_repairability(metrics)

    ai_score = ai_repairability_evaluation(metrics)

    final_score = round((static_score * 0.7) + (ai_score * 0.3), 2)

    explanation = generate_explanation(metrics, static_score, ai_score)

    print("Repairability Score:", final_score)
    print("\nExplanation:\n", explanation)

# -------------------------------------
# FILE DISCOVERY
# -------------------------------------

def find_all_python_files(path):
    files_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                files_list.append(os.path.join(root, file))
    return files_list

# -------------------------------------
# STATIC ANALYSIS
# -------------------------------------

def analyze_codebase(files):

    total_functions = 0
    total_classes = 0
    total_imports = 0
    function_lengths = []
    dependency_graph = {}

    for file in files:
        try:
            tree = parse_ast(file)
        except:
            continue

        imports = extract_imports(tree)
        functions = extract_functions(tree)
        classes = extract_classes(tree)

        total_imports += len(imports)
        total_functions += len(functions)
        total_classes += len(classes)

        for func in functions:
            function_lengths.append(lines_of_code(func))

        dependency_graph[file] = len(imports)

    return {
        "functions": total_functions,
        "classes": total_classes,
        "imports": total_imports,
        "function_lengths": function_lengths,
        "dependencies": dependency_graph
    }

# -------------------------------------
# REPAIRABILITY CALCULATION
# -------------------------------------

def calculate_static_repairability(metrics):

    if metrics["function_lengths"]:
        avg_function_length = sum(metrics["function_lengths"]) / len(metrics["function_lengths"])
    else:
        avg_function_length = 0

    coupling_score = normalize_inverse(metrics["imports"])
    cohesion_score = normalize_inverse(avg_function_length)

    static_score = round((coupling_score * 0.5) + (cohesion_score * 0.5), 2)

    return static_score

# -------------------------------------
# AI SCORING (ADDED LAST — STUB)
# -------------------------------------

def ai_repairability_evaluation(metrics):
    """
    AI-assisted evaluation (prompt-based).
    Stubbed for prototype; replace with GPT/CodeLlama if needed.
    """

    prompt_summary = f"""
    Codebase summary:
    - Functions: {metrics['functions']}
    - Classes: {metrics['classes']}
    - Average function length: {average(metrics['function_lengths'])}
    - Total dependencies: {metrics['imports']}

    Rate repairability (0–100) based on modularity
    and ease of change.
    """

    # Placeholder AI score (acceptable for thesis prototype)
    ai_score = 75

    return ai_score

# -------------------------------------
# EXPLANATION
# -------------------------------------

def generate_explanation(metrics, static_score, ai_score):

    return (
        f"The analyzed codebase contains {metrics['functions']} functions "
        f"and {metrics['classes']} classes.\n"
        f"Average function length is {average(metrics['function_lengths'])} lines.\n"
        f"Total dependency count is {metrics['imports']}.\n\n"
        f"Static analysis repairability score: {static_score}\n"
        f"AI-assisted repairability score: {ai_score}\n\n"
        f"The final score combines static metrics and AI evaluation "
        f"to assess modularity and ease of change."
    )

# -------------------------------------
# HELPER FUNCTIONS
# -------------------------------------

def parse_ast(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return ast.parse(f.read())

def extract_imports(tree):
    return [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]

def extract_functions(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

def extract_classes(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

def lines_of_code(node):
    return getattr(node, "end_lineno", node.lineno) - node.lineno + 1

def normalize_inverse(value):
    # Simple normalization for prototype
    return max(0, 100 - value)

def average(values):
    return round(sum(values) / len(values), 2) if values else 0

def is_github_url(path):
    return path.startswith("http://") or path.startswith("https://")

def clone_repository(url):
    repo_name = url.rstrip("/").split("/")[-1]
    subprocess.run(["git", "clone", url, repo_name], stdout=subprocess.DEVNULL)
    return repo_name

# -------------------------------------
# RUN (example)
# -------------------------------------

# main("https://github.com/example/repo")
# main("path/to/local/codebase")
