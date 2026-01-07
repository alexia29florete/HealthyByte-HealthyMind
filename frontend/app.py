import flet as ft
from login import get_login_view

def main(page: ft.Page):

    def handle_login_success():
        login_container.visible = False    # Ascundem login-ul
        journal_view.visible = True        # Arătăm jurnalul
        page.navigation_bar.visible = True # Arătăm meniul de jos
        page.update()

    # Setări de bază
    page.title = "HealthyByte - HealthyMind"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO 
    page.bgcolor = "#F0F2F5" 

    # --- 1. REFERINȚE DATE ---
    breakfast1_ref = ft.Ref[ft.TextField](); lunch1_ref = ft.Ref[ft.TextField](); dinner1_ref = ft.Ref[ft.TextField]()
    breakfast1_q_ref = ft.Ref[ft.TextField](); lunch1_q_ref = ft.Ref[ft.TextField](); dinner1_q_ref = ft.Ref[ft.TextField]()

    breakfast2_ref = ft.Ref[ft.TextField](); lunch2_ref = ft.Ref[ft.TextField](); dinner2_ref = ft.Ref[ft.TextField]()
    breakfast2_q_ref = ft.Ref[ft.TextField](); lunch2_q_ref = ft.Ref[ft.TextField](); dinner2_q_ref = ft.Ref[ft.TextField]()
    
    breakfast3_ref = ft.Ref[ft.TextField](); lunch3_ref = ft.Ref[ft.TextField](); dinner3_ref = ft.Ref[ft.TextField]()
    breakfast3_q_ref = ft.Ref[ft.TextField](); lunch3_q_ref = ft.Ref[ft.TextField](); dinner3_q_ref = ft.Ref[ft.TextField]()
    
    snack1_ref = ft.Ref[ft.TextField](); snack2_ref = ft.Ref[ft.TextField](); snack3_ref = ft.Ref[ft.TextField]()
    snack1_qref = ft.Ref[ft.TextField](); snack2_qref = ft.Ref[ft.TextField](); snack3_qref = ft.Ref[ft.TextField]()

    mood_ref = ft.Ref[ft.Slider](); energy_ref = ft.Ref[ft.Slider](); mindset_ref = ft.Ref[ft.Slider]()
    sleep_h_ref = ft.Ref[ft.TextField](); sleep_i_ref = ft.Ref[ft.TextField]()

    ex_type1_ref = ft.Ref[ft.TextField](); ex_dur1_ref = ft.Ref[ft.TextField]()
    ex_type2_ref = ft.Ref[ft.TextField](); ex_dur2_ref = ft.Ref[ft.TextField]()
    ex_type3_ref = ft.Ref[ft.TextField](); ex_dur3_ref = ft.Ref[ft.TextField]()
    ex_type4_ref = ft.Ref[ft.TextField](); ex_dur4_ref = ft.Ref[ft.TextField]()
    ex_type5_ref = ft.Ref[ft.TextField](); ex_dur5_ref = ft.Ref[ft.TextField]()


    # --- 2. LOGICĂ SALVARE ---
    def save_clicked(e):
        user_data = {
            "meals": {
                "breakfast": [breakfast1_ref.current.value, breakfast1_q_ref.current.value,breakfast2_ref.current.value, breakfast2_q_ref.current.value,breakfast3_ref.current.value, breakfast3_q_ref.current.value],
                "lunch": [lunch1_ref.current.value, lunch1_q_ref.current.value,lunch2_ref.current.value, lunch2_q_ref.current.value,lunch3_ref.current.value, lunch3_q_ref.current.value],
                "dinner": [dinner1_ref.current.value, dinner1_q_ref.current.value,dinner2_ref.current.value, dinner2_q_ref.current.value,dinner3_ref.current.value, dinner3_q_ref.current.value]
            },
            "wellness": {"m": mood_ref.current.value, "e": energy_ref.current.value, "mind": mindset_ref.current.value}
        }
        print("Date capturate:", user_data)
        page.snack_bar = ft.SnackBar(ft.Text("Jurnal salvat!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    def navigate(e):
        index = e.control.selected_index
        journal_view.visible = (index == 0)
        stats_view.visible = (index == 1)
        page.update()

    # --- 3. UI ---
    journal_view = ft.Column([
        ft.Text("Daily Journal", size=40, color="blue900", weight="bold"),
        ft.Text("Please insert details of your day", color="grey700"),
        ft.Container(height=10),

        ft.ResponsiveRow([
            # CARD MESE (Corectat: pus în ft.Column pentru aliniere)
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.ListTile(title=ft.Text("Main Meals", weight="bold")),
                            ft.ListTile(title=ft.Text("Breakfast-First Meal", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=breakfast1_ref, label="Food1", border="underline", expand=True),
                                ft.TextField(ref=breakfast1_q_ref, label="Quantity1", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=breakfast2_ref, label="Food2", border="underline", expand=True),
                                ft.TextField(ref=breakfast2_q_ref, label="Quantity2", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=breakfast3_ref, label="Food3", border="underline", expand=True),
                                ft.TextField(ref=breakfast3_q_ref, label="Quantity3", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Lunch-Second Meal", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=lunch1_ref, label="Food1", border="underline", expand=True),
                                ft.TextField(ref=lunch1_q_ref, label="Quantity1", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=lunch2_ref, label="Food2", border="underline", expand=True),
                                ft.TextField(ref=lunch2_q_ref, label="Quantity2", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=lunch3_ref, label="Food3", border="underline", expand=True),
                                ft.TextField(ref=lunch3_q_ref, label="Quantity3", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Dinner-Third Meal", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=dinner1_ref, label="Food1", border="underline", expand=True),
                                ft.TextField(ref=dinner1_q_ref, label="Quantity1", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=dinner2_ref, label="Food2", border="underline", expand=True),
                                ft.TextField(ref=dinner2_q_ref, label="Quantity2", border="underline", expand=True),
                            ], spacing=10),
                            ft.Row([
                                ft.TextField(ref=dinner3_ref, label="Food3", border="underline", expand=True),
                                ft.TextField(ref=dinner3_q_ref, label="Quantity3", border="underline", expand=True),
                            ], spacing=10),
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),

            # CARD SNACK-URI
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.ListTile(title=ft.Text("Snacks", weight="bold")),
                            ft.ListTile(title=ft.Text("Snack1", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack1_ref, label="Food1", border="underline", expand=True),
                                ft.TextField(ref=snack1_qref, label="Quantity1", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Snack2", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack2_ref, label="Food2", border="underline", expand=True),
                                ft.TextField(ref=snack2_qref, label="Quantity2", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Snack3", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack3_ref, label="Food3", border="underline", expand=True),
                                ft.TextField(ref=snack3_qref, label="Quantity3", border="underline", expand=True),
                            ], spacing=10),
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),

            # CARD WELLNESS
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.ListTile(title=ft.Text("Wellness", weight="bold")),
                            ft.Text("Mood:"), ft.Slider(ref=mood_ref, min=1, max=10, divisions=9, label="{value}"),
                            ft.Text("Energy:"), ft.Slider(ref=energy_ref, min=1, max=10, divisions=9, label="{value}"),
                            ft.Text("Focus:"), ft.Slider(ref=mindset_ref, min=1, max=10, divisions=9, label="{value}"),
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),

            # CARD ACTIVITATE
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.ListTile(title=ft.Text("Rest & Activity", weight="bold")),
                            ft.Text("Sleeping Schedule", size=14, weight="w500"),
                            ft.TextField(ref=sleep_h_ref, label="Sleep Hours"),
                            ft.TextField(ref=sleep_i_ref, label="Sleep Interval"),
                            ft.Text("Fitness and Exercises", size=14, weight="w500"),
                             ft.Row([
                                ft.TextField(ref=ex_type1_ref, label="Activity1", border="underline", expand=True),
                                ft.TextField(ref=ex_dur1_ref, label="Duration1", border="underline", expand=True),
                            ], spacing=10),
                             ft.Row([
                                ft.TextField(ref=ex_type2_ref, label="Activity2", border="underline", expand=True),
                                ft.TextField(ref=ex_dur2_ref, label="Duration2", border="underline", expand=True),
                            ], spacing=10),
                             ft.Row([
                                ft.TextField(ref=ex_type3_ref, label="Activity3", border="underline", expand=True),
                                ft.TextField(ref=ex_dur3_ref, label="Duration3", border="underline", expand=True),
                            ], spacing=10),
                             ft.Row([
                                ft.TextField(ref=ex_type4_ref, label="Activity4", border="underline", expand=True),
                                ft.TextField(ref=ex_dur4_ref, label="Duration4", border="underline", expand=True),
                            ], spacing=10),
                             ft.Row([
                                ft.TextField(ref=ex_type5_ref, label="Activity5", border="underline", expand=True),
                                ft.TextField(ref=ex_dur5_ref, label="Duration5", border="underline", expand=True),
                            ], spacing=10),
                             
                           # ft.TextField(ref=ex_type_ref, label="Exercise Type"),
                           # ft.TextField(ref=ex_dur_ref, label="Exercise Interval"),
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),
        ], spacing=20),

        ft.Container(height=20),
        ft.Row([
            ft.FilledButton("Save My Day", icon="save", on_click=save_clicked, width=300, height=50),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=40),
    ], visible=True)

    #---------------------------------------------
   # --- 3. UI --- (Secțiunea de Statistici REPARATĂ)
   # --- 3. UI --- (Secțiunea de Statistici REPARATĂ)
    valori_grafic = [6, 6, 7, 8, 9, 3, 4] # ore somn
    data_points = [ft.LineChartDataPoint(i, val) for i, val in enumerate(valori_grafic)]

    valori_grafic1 = [2550, 2345, 2678, 2367, 2789, 2456, 2234]# calorii arse
    data_points1 = [ft.LineChartDataPoint(i, val) for i, val in enumerate(valori_grafic1)]

    valori_grafic2 = [2400, 2435, 2763, 3120, 2432, 2436, 2214] # calorii consumate 
    data_points2 = [ft.LineChartDataPoint(i, val) for i, val in enumerate(valori_grafic2)]

    stats_view = ft.Column(
    [
        ft.Text("Dashboard Statistici", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        ft.Text("Hours Slept in the last 7 Days", color=ft.Colors.GREY_700),

        ft.Container(
            content=ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=data_points,
                        stroke_width=4,
                        color=ft.Colors.BLUE,
                        curved=True,
                        below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                        point=True,
                    )
                ],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=0,
                max_y=10,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(0, 11, 2)],
                    labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                expand=True,
            ),
            height=350,
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_300),
        ),

        ft.Container(height=8),

        ft.Row(
            [
                ft.Container(ft.Text("Mo", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Tu", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("We", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Th", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Fr", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Sa", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Su", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
            ],
            spacing=0,
        ),
        #---------------------------------------------------
        ft.Text("Burnt Calories in the last 7 Days", color=ft.Colors.GREY_700),

        ft.Container(
            content=ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=data_points1,
                        stroke_width=4,
                        color=ft.Colors.BLUE,
                        curved=True,
                        below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                        point=True,
                    )
                ],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=1800,
                max_y=3000,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(1800, 3000, 100)],
                    labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                expand=True,
            ),
            height=350,
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_300),
        ),

        ft.Container(height=8),

        ft.Row(
            [
                ft.Container(ft.Text("Mo", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Tu", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("We", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Th", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Fr", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Sa", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Su", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
            ],
            spacing=0,
        ),
         #---------------------------------------------------
        ft.Text("Consumed Calories in the last 7 Days", color=ft.Colors.GREY_700),

        ft.Container(
            content=ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=data_points2,
                        stroke_width=4,
                        color=ft.Colors.BLUE,
                        curved=True,
                        below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                        point=True,
                    )
                ],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=2000,
                max_y=3500,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(2000, 3500, 100)],
                    labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.GREY_100),
                expand=True,
            ),
            height=350,
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_300),
        ),

        ft.Container(height=8),

        ft.Row(
            [
                ft.Container(ft.Text("Mo", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Tu", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("We", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Th", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Fr", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Sa", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
                ft.Container(ft.Text("Su", size=12, color=ft.Colors.GREY_700),
                             expand=True, alignment=ft.alignment.center),
            ],
            spacing=0,
        ),
    ],
    visible=False,
    expand=True,
    )


    # --- 3. UI --- (Secțiunea de Statistici REPARATĂ FĂRĂ ERORI)
   #---------------------------------------------------------------
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon="edit_note", label="Jurnal"),
            ft.NavigationBarDestination(icon="insert_chart", label="Statistici"),
        ],
        on_change=navigate
    )

    ###################################################################
    # În app.py, în interiorul funcției main:
    login_container = get_login_view(page, handle_login_success) # Adaugă 'page' ca prim argument

    # MODIFICĂ journal_view să fie invizibil la început
    journal_view.visible = False 
    
    # MODIFICĂ navigation_bar să fie invizibil la început
    page.navigation_bar.visible = False

    # Adaugă login_container în listă
    page.add(login_container, journal_view, stats_view)
    #---------------------------------------------------------------
   # page.add(journal_view, stats_view)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, assets_dir="assets")

    '''
                          ft.ChartAxisLabel(value=0, label=ft.Text("L")),
                          ft.ChartAxisLabel(value=1, label=ft.Text("M")),
                          ft.ChartAxisLabel(value=2, label=ft.Text("M")),
                          ft.ChartAxisLabel(value=3, label=ft.Text("J")),
                          ft.ChartAxisLabel(value=4, label=ft.Text("V")),
                          ft.ChartAxisLabel(value=5, label=ft.Text("S")),
                          ft.ChartAxisLabel(value=6, label=ft.Text("D")),
                          '''