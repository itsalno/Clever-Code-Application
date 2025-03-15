from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser


llm1 = OllamaLLM(model="llama3.2")
llm2 = OllamaLLM(model="deepseek-r1:1.5b")


explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly skilled AI assistant specialized in explaining code."),
    ("human", "Explain the following code:\n\n{code}")
])
explain_chain = RunnableSequence(
    explain_prompt | llm1 | StrOutputParser()
)


generate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code generation AI."),
    ("human", "Generate {language} code for:\n\n{request}")
])
generate_chain = RunnableSequence(
    generate_prompt | llm2 | StrOutputParser()
)


translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code translation AI."),
    ("human", "Translate the following code to {desired_language}:\n\n{code}")
])
translate_chain = RunnableSequence(
    translate_prompt | llm1 | StrOutputParser()
)