import flet as ft
import requests

#My UI class nothing to complex.I have 2 dropdowns one for translating and one for generating.There is also input field and then
#send_input function which basically fires the /process_input with the users input and language if exists.Since i have 2 dropdowns,
#i decide which language to send based on the selected option.
def main(page: ft.Page):


    page.title = "Clever Code App"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    indentation_input = ft.TextField(hint_text="Indentation (e.g., 4 spaces, tabs)", width=300)
    naming_convention_input = ft.TextField(hint_text="Naming Convention (e.g., snake_case, camelCase)", width=300)

    user_input = ft.TextField(hint_text="Enter code or description", multiline=True)




    generating_language_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("", "None"),
            ft.dropdown.Option("python"),
            ft.dropdown.Option("java"),
            ft.dropdown.Option("javascript"),
            ft.dropdown.Option("c++"),
            ft.dropdown.Option("c#"),
            ft.dropdown.Option("typescript"),
            ft.dropdown.Option("php"),
            ft.dropdown.Option("Swift"),
            ft.dropdown.Option("Go"),
            ft.dropdown.Option("Rust"),
        ],
        value="",
        width=200,
    )
    translating_language_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("", "None"),
            ft.dropdown.Option("python"),
            ft.dropdown.Option("java"),
            ft.dropdown.Option("javascript"),
            ft.dropdown.Option("c++"),
            ft.dropdown.Option("c#"),
            ft.dropdown.Option("typescript"),
            ft.dropdown.Option("php"),
            ft.dropdown.Option("Swift"),
            ft.dropdown.Option("Go"),
            ft.dropdown.Option("Rust"),
        ],
        value="",
        width=200,
    )

    send_button = ft.ElevatedButton(text="Send")

    output = ft.Text()
    scrollable_output = ft.Column(
        [output],
        scroll=True,
        expand=True,
    )


    def save_preferences(e):
        try:
            # Get the user's input
            indentation = indentation_input.value
            naming_convention = naming_convention_input.value

            # Send the preferences to the API
            response = requests.post(
                "http://127.0.0.1:8000/style_preferences",
                json={
                    "indentation": indentation,
                    "naming_convention": naming_convention
                }
            )

            # Log the raw API response
            print(f"API response: {response.text}")

            # Parse the JSON response
            result = response.json()

            # Display the result
            output.value = result.get("message", "Preferences saved successfully.")

        except requests.exceptions.RequestException as e:
            output.value = f"Error: Failed to connect to the API\n{str(e)}"
        except ValueError as e:
            output.value = f"Error: Invalid JSON response\n{str(e)}"
        except Exception as e:
            output.value = f"Error: {str(e)}"

        # Update the UI
        page.update()

    save_button = ft.ElevatedButton(text="Save",on_click=save_preferences)



    def send_input(e):
        try:
            generating_language = generating_language_dropdown.value
            translating_language = translating_language_dropdown.value

            if generating_language and not translating_language:
                response = requests.post(
                    "http://127.0.0.1:8000/process_input",
                    json={
                        "input": user_input.value,
                        "language": generating_language,
                    }
                )
            elif translating_language and not generating_language:
                response = requests.post(
                    "http://127.0.0.1:8000/process_input",
                    json={
                        "input": user_input.value,
                        "language": translating_language,
                    }
                )
            elif not generating_language and not translating_language:
                response = requests.post(
                    "http://127.0.0.1:8000/process_input",
                    json={
                        "input": user_input.value,
                        "language": "",
                    }
                )
            else:
                output.value = "Error: Please select only one language (generating or translating)."
                return

            print(f"API response: {response.text}")

            result = response.json()

            if "action" in result and "result" in result:
                output.value = f"Action: {result['action']}\nResult: {result['result']}"
            else:
                output.value = f"Error: Invalid response from API\n{result}"
        except requests.exceptions.RequestException as e:
            output.value = f"Error: Failed to connect to the API\n{str(e)}"
        except ValueError as e:
            output.value = f"Error: Invalid JSON response\n{str(e)}"
        except Exception as e:
            output.value = f"Error: {str(e)}"

        page.update()

    send_button.on_click = send_input

    page.add(
        ft.Column([
            ft.Text("Clever Code App", size=20),
            ft.Row([
                ft.Column([ft.Text("Generating language", size=14), generating_language_dropdown]),
                ft.Column([ft.Text("Translating language", size=14), translating_language_dropdown]),
                ft.Column([indentation_input]),
                ft.Column([naming_convention_input,save_button])
            ]),
            user_input,
            send_button,
            ft.Container(
                content=scrollable_output,
                border=ft.border.all(1, ft.Colors.GREY_400),
                padding=10,
                expand=True,
            ),
        ],
        expand=True,
        )
    )

ft.app(target=main)