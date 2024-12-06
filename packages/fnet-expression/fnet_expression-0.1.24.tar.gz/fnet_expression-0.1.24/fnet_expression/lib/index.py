import re

def parse_expression(expression, depth=5):
    """
    Recursively parses an expression into processor and statement components.

    Args:
        expression (str): The expression to parse.
        depth (int, optional): Current recursion depth. Defaults to 5.

    Returns:
        dict | None: Parsed components or None if no match or max depth reached.
    """
    if depth <= 0:
        return None

    # Pattern to match processor and statement
    pattern_base = r"^([a-z_-]+)::([^\s][\s\S]*)$"
    match = re.match(pattern_base, expression)
    if not match:
        return None

    processor, statement = match.groups()
    # Recursively parse nested statements
    next_parsed = parse_expression(statement, depth=depth - 1)

    result = {
        "processor": processor,
        "statement": statement,
        "expression": expression,
    }

    # Add nested parsed expression if exists
    if next_parsed:
        result["next"] = next_parsed

    return result

def extract_processors(parsed):
    """
    Extracts all processors from a parsed expression.

    Args:
        parsed (dict | None): The parsed expression.

    Returns:
        list[str]: List of processors.
    """
    if not parsed:
        return []

    # Recursively collect processors from nested expressions
    processors = extract_processors(parsed.get("next", None))
    processors.append(parsed["processor"])
    return processors

def default(expression):
    """
    Main function to parse an expression and return its components.

    Args:
        expression (str): The expression to parse.

    Returns:
        dict | None: Parsed components or None if no match.
    """
    parsed = parse_expression(expression)

    if not parsed:
        return None

    # Navigate to the deepest nested expression
    current = parsed
    while current.get("next"):
        current = current["next"]

    result = {
        "processor": parsed["processor"],
        "statement": parsed["statement"],
        "expression": parsed["expression"],
        "process": {
            "statement": current["statement"],
            "order": extract_processors(parsed),
        }
    }

    # Include nested expression if available
    if "next" in parsed:
        result["next"] = parsed["next"]

    return result