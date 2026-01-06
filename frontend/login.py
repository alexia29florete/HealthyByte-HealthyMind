import flet as ft

def get_login_view(on_login_success):
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    return ft.Container(
        content=ft.Column([
            ft.Text("HealthyByte Login", size=30, weight="bold", color="blue900"),
            username,
            password,
            ft.FilledButton("Login", on_click=lambda _: on_login_success(), width=300),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        
        # Am schimbat metoda de aliniere pentru a evita eroarea de modul
        alignment=ft.Alignment(0, 0), # (0,0) înseamnă centrul perfect
        
        expand=True
    )