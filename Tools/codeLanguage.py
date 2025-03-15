from pygments.lexers import guess_lexer


#It works but i dont use it because the models are figuring out the language themselves.
#This library is an alternative to guesslang but i could have also used the easv api.
# Since my models are defining the language from code this tool is useless for my application

def detect_language(code: str) -> str:
    lexer = guess_lexer(code)
    return lexer.name