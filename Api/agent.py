from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
import re


def extract_language(input: str) -> str:
    """
    Extract the target language from the user's input.
    """

    match = re.search(r"(in|to|using)\s+(\w+)", input, re.IGNORECASE)
    if match:
        return match.group(2).lower()
    return None

#I chooes llama3.2 as a decider AI here because from the responses it generated i can tell its better at decision making then deepseek.
llm1 = OllamaLLM(model="llama3.2")

system_prompt = """
You are an AI assistant that helps users with code-related tasks. Based on the user's input, decide which action to take:
- If the input is a code snippet, explain it.
- If the input is a natural language description of code functionality, generate code.
- If the input is a code snippet and a target language, translate it.
- If the input is style preferences, save them.

Your response should be one of the following:
- "explain" if the input is a code snippet.
- "generate" if the input is a natural language description.
- "translate" if the input is a code snippet and a target language.
- "style" if the input is style preferences.
- "unknown" if the input doesn't fit any of the above categories.

**Do not include any reasoning or thought process in your response. Provide only the final output.**
"""


prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

agent_chain = RunnableSequence(
    prompt_template | llm1 | StrOutputParser()
)

#This function serves as a decider based on the input which action to perform.
# So llama3.2 takes the imput and decides what it should send the input next.
def agent_executor(input: str,language: str):
    print(f"Agent input: {input}, Language: {language}")



    result = agent_chain.invoke({"input": input})
    print(f"Agent result: {result}")

    if "explain" in result.lower():
        return {"action": "explain", "language": None}
    elif "generate" in result.lower():
        return {"action": "generate", "language": language}
    elif "translate" in result.lower():
        return {"action": "translate", "language": language }
    else:
        return {"action": "unknown", "language": None}