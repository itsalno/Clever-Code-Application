# Clever Code App

Here is how to get it running and small tips to check all the functionality.

## All things to do for app to work

```bash


# Navigate to project directory
cd CleverCodeApp

# Install all of the libraries
pip install -r requirements.txt

#In the command line you need to run 2 models
ollama run llama3.2

ollama run deepseek-r1:1.5b

#Run the Api
uvicorn Endpoints:app --reload

#Run the Flet
flet UI.py
```
## Tips
When everything is up and running you can test the different functions.
If you want ai to explain the code you can just put the code snippiet in input field and click send.

To generate a code in desired language just select the language in corresponding dropdown and then input natural language description in input field and click send.

To translate code,select target language from corresponding dropdown(MAKE SURE TO HAVE THE OTHER DROPDOWN EMPTY)then input translate this code:CODE SNIPPET.Click send.

## IMPORTANT NOTE
The ai is very slow so after pressing send button you should wait about 15-30 seconds for the result to show in UI

if you want to manually check just check the console it will be much faster.

