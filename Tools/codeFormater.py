import black

def format_code(code: str) -> str:
    formatted_code = black.format_str(code, mode=black.FileMode())
    return formatted_code