import json

import uvicorn
from fastapi import FastAPI
from Api.Models import CodeSnippet, CodeRequest, CodeTranslation,ProcessInputRequest,StyleCode
from Api.chains import explain_chain, generate_chain, translate_chain
from Api.agent import agent_executor

app = FastAPI()

#So i have 4 general endpoints like in the requirements and then one "King" endpoint which sends the input and (if present) language to agent for
#him to decide what operation needs to be performed and then triggering the needed function.I dont really need those 4 as an endpoints,i could have been fine with func
#but its in the requirements.

@app.post("/explain_code")
async def explain_code(snippet: CodeSnippet):
    explanation = explain_chain.invoke({"code": snippet.code})
    return {"explanation": explanation}

@app.post("/generate_code")
async def generate_code(request: CodeRequest):
    code = generate_chain.invoke({"request": request.request, "language": request.language})
    return {"code": code}

@app.post("/translate_code")
async def translate_code(translation: CodeTranslation):
    translated_code = translate_chain.invoke({"code": translation.code, "desired_language": translation.desired_language})
    return {"translated_code": translated_code}

STYLE_PREFERENCES_FILE = "style_preferences.json"

@app.post("/style_preferences")
async def set_style_preferences(preferences: StyleCode):

        preferences_dict = preferences.dict()


        with open(STYLE_PREFERENCES_FILE, "w") as f:
            json.dump(preferences_dict, f, indent=4)

        return {"message": "Style preferences saved successfully."}



@app.post("/process_input")
async def process_input(request: ProcessInputRequest):
    input_text = request.input
    language = request.language



    result = agent_executor(input_text,language)


    if result["action"] == "explain":
        response = await explain_code(CodeSnippet(code=input_text))
        return {"action": "explain", "result": response["explanation"]}
    elif result["action"] == "generate":
        response = await generate_code(
            CodeRequest(request=input_text, language=language))
        return {"action": "generate", "result": response["code"]}
    elif result["action"] == "translate":
        response = await translate_code(
            CodeTranslation(code=input_text, desired_language=language))
        return {"action": "translate", "result": response["translated_code"]}
    else:
        return {"action": "unknown", "result": "Unable to determine the action."}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)