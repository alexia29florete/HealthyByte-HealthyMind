import flet as ft
from api_client import login_or_signup, ApiError


def get_login_view(page, on_login_success):
    email = ft.TextField(label="Email", width=300, bgcolor="white")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, bgcolor="white")

    status_text = ft.Text("", color="red")

    def do_login(_):
        try:
            token = login_or_signup(email.value.strip(), password.value)
            status_text.value = ""
            on_login_success(token)
        except ApiError as e:
            status_text.value = str(e)
        page.update()

    return ft.Stack([
        ft.Image(
            #src="ia4_bck.jpg",
            #src="bck.png",
            src="bck8.jpg",
            fit=ft.ImageFit.COVER,
            width=page.width, 
            height=page.height,
            #expand=True,
            #width=1920, 
            #height=1080,
        ),
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("HealthyByte Login", size=32, weight="bold", color="green900"),
                        ft.Text("Your journey to a healthier life", color="grey700"),
                        ft.Divider(height=20, color="transparent"),
                        email,
                        password,
                        ft.Container(height=10),
                        ft.FilledButton(
                            "Login / Auto-signup",
                            on_click=do_login,
                            width=300,
                            height=50,
                            bgcolor=ft.colors.GREEN_600
                        ),
                        ft.Container(height=10),
                        status_text,
                        ft.Text(
                            "Tip: dacă nu ai cont, se creează automat la primul login.",
                            size=12,
                            color="grey700",
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.with_opacity(0.9, "white"),
                    padding=40,
                    width=420,
                    border_radius=20,
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )
    ], expand=True)
