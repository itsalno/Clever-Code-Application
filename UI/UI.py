import flet as ft
import requests

#My UI class nothing to complex.I have 2 dropdowns one for translating and one for generating.There is also input field and then
#send_input function which basically fires the /process_input with the users input and language if exists.Since i have 2 dropdowns,
#i decide which language to send based on the selected option.
def main(page: ft.Page):
    page.title = "Clever Code App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    user_input = ft.TextField(hint_text="Enter code or description", multiline=True)
    generating_language_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("", "None"),  # Empty option with a label
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
            ft.Text("Generating language",size=14),
            ft.Row([generating_language_dropdown],),
            ft.Text("Translating language", size=14),
            ft.Row([translating_language_dropdown]),
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