from pydantic import BaseModel



class ProcessInputRequest(BaseModel):
    input: str
    language: str

class CodeSnippet(BaseModel):
    code: str

class CodeRequest(BaseModel):
    request: str
    language: str

class CodeTranslation(BaseModel):
    code: str
    desired_language: str

class StyleCode(BaseModel):
    indentation: str
    naming_convention: str