import flet as ft

def get_login_view(page, on_login_success):
    username = ft.TextField(label="Username", width=300, bgcolor="white")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, bgcolor="white")

    # Folosim Stack pentru a pune imaginea sub formular
    return ft.Stack([
        # Stratul 1: Imaginea de fundal
        ft.Image(
            #src="ia4_bck.jpg",
            #src="bck.png",
            src="bck3.jpg",
            fit=ft.ImageFit.COVER,
            width=page.width, # Preia lățimea ferestrei browserului
            height=page.height,
            #expand=True,
            #width=1920, # Forțăm dimensiuni mari pentru a acoperi ecranul
            #height=1080,
        ),
        # Stratul 2: Formularul de Login centrat
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("HealthyByte Login", size=32, weight="bold", color="green900"),
                        ft.Text("Your journey to a healthier life", color="grey700"),
                        ft.Divider(height=20, color="transparent"),
                        username,
                        password,
                        ft.Container(height=10),
                        ft.FilledButton(
                            "Login", 
                            on_click=lambda _: on_login_success(), 
                            width=300, 
                            height=50,
                            bgcolor=ft.colors.GREEN_600
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.with_opacity(0.9, "white"), 
                    padding=40,
                    width=400,
                    border_radius=20,
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )
    ], expand=True)