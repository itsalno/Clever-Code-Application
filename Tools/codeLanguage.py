from pygments.lexers import guess_lexer


#It works but i dont use it because the models are figuring out the language themselves.
def detect_language(code: str) -> str:
    lexer = guess_lexer(code)
    return lexer.name