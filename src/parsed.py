import ast

def parse_python_code(code: str):
    tree = ast.parse(code)
    parsed = []
    
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            parsed.append({
                'type': 'function',
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'docstring': ast.get_docstring(node),
                'lineno': node.lineno,
                'logic': extract_function_logic(node),
            })
        elif isinstance(node, ast.ClassDef):
            parsed.append({
                'type': 'class',
                'name': node.name,
                'docstring': ast.get_docstring(node),
                'methods': [
                    {
                        'name': method.name,
                        'args': [arg.arg for arg in method.args.args],
                        'docstring': ast.get_docstring(method),
                        'lineno': method.lineno,
                    }
                    for method in node.body if isinstance(method, ast.FunctionDef)
                ],
                'lineno': node.lineno,
            })

    return parsed

def extract_function_logic(func_node):
    logic = []
    
    for stm in ast.walk(func_node):
        if isinstance(stm, ast.Return):
            logic.append({
                'type': 'return',
                'value': ast.unparse(stm.value),
                'lineno': stm.lineno,
            })
        elif isinstance(stm, ast.Expr) and isinstance(stm.value, ast.Constant):
            logic.append({
                'type': 'comment',
                'value': stm.value,
                'lineno': stm.lineno,
            })
            
    return logic
    