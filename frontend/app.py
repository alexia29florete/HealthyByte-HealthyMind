import flet as ft

def main(page: ft.Page):
    page.title = "HealthyByte - HealthyMind"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def navigate(e):
        index = e.control.selected_index
        journal_container.visible = (index == 0)
        stats_container.visible = (index == 1)
        page.update()

    # --- ECRANUL 1: Jurnal Zilnic ---
    journal_container = ft.Column([
        ft.Text("Jurnal Zilnic", size=30, weight=ft.FontWeight.BOLD),
        ft.Text("Introdu detaliile mesei tale:"),
        ft.TextField(label="Ce ai mâncat?", multiline=True, min_lines=3),
        ft.Text("Cum te simți (1-10)?"),
        ft.Slider(min=1, max=10, divisions=9, label="{value}"),
        # Folosim ft.FilledButton în loc de ElevatedButton pentru a evita DeprecationWarning
        ft.FilledButton("Salvează Jurnal", icon="save")
    ], visible=True)

    # --- ECRANUL 2: Statistici și Feedback ---
    stats_container = ft.Column([
        ft.Text("Dashboard Statistici", size=30, weight=ft.FontWeight.BOLD),
        ft.Text("Vizualizarea progresului tău va apărea aici."),
    ], visible=False)

    # Bara de navigare - Corectată conform versiunii noi de Flet
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            # Aici era eroarea: numele corect este NavigationBarDestination
            ft.NavigationBarDestination(icon="edit_note", label="Jurnal"),
            ft.NavigationBarDestination(icon="insert_chart", label="Statistici"),
        ],
        on_change=navigate
    )

    page.add(journal_container, stats_container)

if __name__ == "__main__":
    # Folosim ft.app în continuare, dar am corectat componentele din interior
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)