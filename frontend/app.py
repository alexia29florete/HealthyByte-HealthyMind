import flet as ft
# --- charts compat (Flet charts moved to extension package) ---
try:
    import flet_charts as ftc  # pip install flet-charts
except Exception:
    ftc = None

if ftc is not None and not hasattr(ft, "LineChartDataPoint"):
    # re-export commonly used chart classes into ft namespace
    for name in [
        "LineChart",
        "LineChartData",
        "LineChartDataPoint",
        "ChartAxis",
        "ChartAxisLabel",
        "ChartGridLines",
        "ChartPointShape",
        "ChartPointLine",
    ]:
        if hasattr(ftc, name) and not hasattr(ft, name):
            setattr(ft, name, getattr(ftc, name))
# -------------------------------------------------------------

from api_client import create_journal_entry, get_stats_summary, ApiError
from login import get_login_view

def main(page: ft.Page):

    def handle_login_success(token: str):
        auth['token'] = token
        login_container.visible = False   
        journal_view.visible = True       
        page.navigation_bar.visible = True 
        page.update()

   
    page.title = "HealthyByte - HealthyMind"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO 
    #page.bgcolor = "#F0F2F5"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#E8F5E9"

    auth = {'token': None}

    feedback_display = ft.Text("", selectable=True)
    stats_summary_text = ft.Text("", selectable=True)

    # --- DATA REF---
    breakfast1_ref = ft.Ref[ft.TextField](); lunch1_ref = ft.Ref[ft.TextField](); dinner1_ref = ft.Ref[ft.TextField]()
    breakfast1_q_ref = ft.Ref[ft.TextField](); lunch1_q_ref = ft.Ref[ft.TextField](); dinner1_q_ref = ft.Ref[ft.TextField]()

    breakfast2_ref = ft.Ref[ft.TextField](); lunch2_ref = ft.Ref[ft.TextField](); dinner2_ref = ft.Ref[ft.TextField]()
    breakfast2_q_ref = ft.Ref[ft.TextField](); lunch2_q_ref = ft.Ref[ft.TextField](); dinner2_q_ref = ft.Ref[ft.TextField]()
    
    breakfast3_ref = ft.Ref[ft.TextField](); lunch3_ref = ft.Ref[ft.TextField](); dinner3_ref = ft.Ref[ft.TextField]()
    breakfast3_q_ref = ft.Ref[ft.TextField](); lunch3_q_ref = ft.Ref[ft.TextField](); dinner3_q_ref = ft.Ref[ft.TextField]()
    
    snack1_ref = ft.Ref[ft.TextField](); snack2_ref = ft.Ref[ft.TextField](); snack3_ref = ft.Ref[ft.TextField](); snack4_ref = ft.Ref[ft.TextField](); snack5_ref = ft.Ref[ft.TextField](); snack6_ref = ft.Ref[ft.TextField]()
    snack1_qref = ft.Ref[ft.TextField](); snack2_qref = ft.Ref[ft.TextField](); snack3_qref = ft.Ref[ft.TextField](); snack4_qref = ft.Ref[ft.TextField](); snack5_qref = ft.Ref[ft.TextField](); snack6_qref = ft.Ref[ft.TextField]()

    mood_ref = ft.Ref[ft.Slider](); energy_ref = ft.Ref[ft.Slider](); mindset_ref = ft.Ref[ft.Slider]()
    sleep_h_ref = ft.Ref[ft.TextField](); sleep_i_ref = ft.Ref[ft.TextField]()
    entry_date_ref = ft.Ref[ft.TextField]()

    ex_type1_ref = ft.Ref[ft.TextField](); ex_dur1_ref = ft.Ref[ft.TextField]()
    ex_type2_ref = ft.Ref[ft.TextField](); ex_dur2_ref = ft.Ref[ft.TextField]()
    ex_type3_ref = ft.Ref[ft.TextField](); ex_dur3_ref = ft.Ref[ft.TextField]()
    ex_type4_ref = ft.Ref[ft.TextField](); ex_dur4_ref = ft.Ref[ft.TextField]()
    ex_type5_ref = ft.Ref[ft.TextField](); ex_dur5_ref = ft.Ref[ft.TextField]()


    # ---SAVE---
    def save_clicked(e):
        if not auth.get('token'):
            page.snack_bar = ft.SnackBar(ft.Text("Not logged in."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        def food_item(food_val, qty_val):
            food = (food_val or "").strip()
            if not food:
                return None
            try:
                q = int(float(qty_val)) if qty_val not in (None, "") else None
            except Exception:
                q = None
            return {"food": food, "quantity_g": q}

        breakfast = [food_item(breakfast1_ref.current.value, breakfast1_q_ref.current.value),
                     food_item(breakfast2_ref.current.value, breakfast2_q_ref.current.value),
                     food_item(breakfast3_ref.current.value, breakfast3_q_ref.current.value)]
        lunch = [food_item(lunch1_ref.current.value, lunch1_q_ref.current.value),
                 food_item(lunch2_ref.current.value, lunch2_q_ref.current.value),
                 food_item(lunch3_ref.current.value, lunch3_q_ref.current.value)]
        dinner = [food_item(dinner1_ref.current.value, dinner1_q_ref.current.value),
                  food_item(dinner2_ref.current.value, dinner2_q_ref.current.value),
                  food_item(dinner3_ref.current.value, dinner3_q_ref.current.value)]

        snack1 = [food_item(snack1_ref.current.value, snack1_qref.current.value)]
        snack2 = [food_item(snack2_ref.current.value, snack2_qref.current.value)]
        snack3 = [food_item(snack3_ref.current.value, snack3_qref.current.value)]
        snack4 = [food_item(snack4_ref.current.value, snack4_qref.current.value)]
        snack5 = [food_item(snack5_ref.current.value, snack5_qref.current.value)]
        snack6 = [food_item(snack6_ref.current.value, snack6_qref.current.value)]

        # remove None
        breakfast = [x for x in breakfast if x]
        lunch = [x for x in lunch if x]
        dinner = [x for x in dinner if x]
        snack1 = [x for x in snack1 if x]
        snack2 = [x for x in snack2 if x]
        snack3 = [x for x in snack3 if x]
        snack4 = [x for x in snack4 if x]
        snack5 = [x for x in snack5 if x]
        snack6 = [x for x in snack6 if x]

        # wellness sliders might be string
        def to_int(v):
            try:
                return int(float(v))
            except Exception:
                return None

        fitness = []
        def add_ex(t, d):
            name = (t or "").strip()
            if not name:
                return
            try:
                minutes = int(float(d)) if d not in (None, "") else None
            except Exception:
                minutes = None
            if minutes is None:
                return
            fitness.append({"exercise": name, "time_min": minutes})

        add_ex(ex_type1_ref.current.value, ex_dur1_ref.current.value)
        add_ex(ex_type2_ref.current.value, ex_dur2_ref.current.value)
        add_ex(ex_type3_ref.current.value, ex_dur3_ref.current.value)
        add_ex(ex_type4_ref.current.value, ex_dur4_ref.current.value)
        add_ex(ex_type5_ref.current.value, ex_dur5_ref.current.value)

        payload = {
            "entry_date": (entry_date_ref.current.value or "").strip() or None,
            "main_meals": {"breakfast": breakfast, "lunch": lunch, "dinner": dinner},
            "snacks": {"snack1": snack1, "snack2": snack2, "snack3": snack3, "snack4": snack4, "snack5": snack5, "snack6": snack6},
            "wellness": {"mood": to_int(mood_ref.current.value), "energy": to_int(energy_ref.current.value), "focus": to_int(mindset_ref.current.value)},
            "rest": {"sleep_hours": to_int(sleep_h_ref.current.value), "sleep_interval": (sleep_i_ref.current.value or "").strip()},
            "fitness": fitness,
        }

        try:
            result = create_journal_entry(auth['token'], payload)
            feedback_display.value = result.get("feedback", "")
            page.snack_bar = ft.SnackBar(ft.Text("Saved!"), bgcolor="green")
            page.snack_bar.open = True
        except ApiError as err:
            page.snack_bar = ft.SnackBar(ft.Text(str(err)), bgcolor="red")
            page.snack_bar.open = True

        page.update()


    def refresh_stats():
        if not auth.get('token'):
            stats_summary_text.value = "Not logged in."
            return
        try:
            s = get_stats_summary(auth['token'])
            macros = s.get("macros_totals", {})
            emo = s.get("emotions_frequency", {})
            cal = s.get("calories_trend", [])

            total_cal = 0
            if isinstance(cal, list):
                for x in cal:
                    try:
                        total_cal += float(x.get("calories", 0))
                    except Exception:
                        pass

            stats_summary_text.value = (
                f"Total calories (trend sum): {int(total_cal)}\n"
                f"Macros: P {macros.get('protein_g', 0)}g | C {macros.get('carbs_g', 0)}g | F {macros.get('fat_g', 0)}g | Fiber {macros.get('fiber_g', 0)}g\n"
                f"Emotions: " + (", ".join([f"{k}={v}" for k, v in emo.items()]) if emo else "-")
            )

            # Acceptă ambele formate: fie *_7d la root, fie charts.* (în funcție de backend)
            charts = s.get("charts", {}) or {}
            sleep = charts.get("sleep_hours", [0]*7)
            burned = charts.get("burned_calories", [0]*7)
            consumed = charts.get("consumed_calories", [0]*7)
            happy = charts.get("happiness", [0]*7)

            # forțează exact 7 valori (ca să nu crape chart-ul / să nu rămână cu vechi)
            def norm7(vals):
                vals = list(vals)[:7]
                while len(vals) < 7:
                    vals.append(0)
                return vals

            sleep = norm7(sleep)
            burned = norm7(burned)
            consumed = norm7(consumed)
            happy = norm7(happy)

            # UPDATE: acum folosești seriile tale (sleep_series, burned_series, etc.)
            sleep_series.data_points = [ft.LineChartDataPoint(i, float(v)) for i, v in enumerate(sleep)]
            burned_series.data_points = [ft.LineChartDataPoint(i, float(v)) for i, v in enumerate(burned)]
            consumed_series.data_points = [ft.LineChartDataPoint(i, float(v)) for i, v in enumerate(consumed)]
            happiness_series.data_points = [ft.LineChartDataPoint(i, float(v)) for i, v in enumerate(happy)]

            page.update()

        except ApiError as e:
            stats_summary_text.value = str(e)
            page.update()

    def navigate(e):
        index = e.control.selected_index
        journal_view.visible = (index == 0)
        stats_view.visible = (index == 1)
        if index == 1:
            refresh_stats()
        page.update()

    # --- ADDED LAST TIME ---
    image_card = ft.Card(
         margin=0,
        content=ft.Container(
             expand=True,          
             padding=0,  
            bgcolor="#F9FFFB",
            border=ft.border.all(1, "#D6E8D7"),
         shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
         ),
          border_radius=16,
          clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
          height=350,  
            content=ft.Image(
            src="bck7.jpg",  
            fit=ft.ImageFit.COVER,
            expand=True, 
            ),
        ),
        elevation=0,
    ) 

    image_card1 = ft.Card(
        margin=0,
        content=ft.Container(
            bgcolor="#F9FFFB",
            border=ft.border.all(1, "#D6E8D7"),
         shadow=ft.BoxShadow(
            blur_radius=14,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 6),
         ),
          border_radius=16,
          clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
          height=550,  
            content=ft.Image(
            src="bck4.jpg",  
            fit=ft.ImageFit.COVER,
            ),
        ),
        elevation=0,
    )

    # ---  UI ---
    journal_view = ft.Column([
        #ft.Text("Daily Journal", size=40, color="blue900", weight="bold"),
        ft.Text(
             "Daily Journal",
             size=40,
             weight="bold",
             color="#2E7D32",   
             text_align=ft.TextAlign.CENTER,
            ),
        ft.Text("Please insert details of your day", color="grey700"),
        ft.Container(height=10),

        ft.ResponsiveRow([
            # MEALS
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        #########-------------------------------------
                        bgcolor="#F9FFFB",
                        border=ft.border.all(1, "#D6E8D7"),
                        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 6)),
                        ##------------------------------
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

            # CARD SNACKS
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        #########-------------------------------------
                        bgcolor="#F9FFFB",
                        border=ft.border.all(1, "#D6E8D7"),
                        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 6)),
                        ##------------------------------
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
                            ft.ListTile(title=ft.Text("Snack4", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack4_ref, label="Food4", border="underline", expand=True),
                                ft.TextField(ref=snack4_qref, label="Quantity4", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Snack5", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack5_ref, label="Food5", border="underline", expand=True),
                                ft.TextField(ref=snack5_qref, label="Quantity5", border="underline", expand=True),
                            ], spacing=10),
                            ft.ListTile(title=ft.Text("Snack6", weight="bold")),
                            ft.Row([
                                ft.TextField(ref=snack6_ref, label="Food6", border="underline", expand=True),
                                ft.TextField(ref=snack6_qref, label="Quantity6", border="underline", expand=True),
                            ], spacing=10),
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),

            #  WELLNESS
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        #########-------------------------------------
                        bgcolor="#F9FFFB",
                        border=ft.border.all(1, "#D6E8D7"),
                        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 6)),
                        ##------------------------------
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

            ft.Column([image_card], col={"sm": 12, "md": 6},expand=True),
            #  ACTIVIY
            ft.Column([
                ft.Card(
                    content=ft.Container(
                        #########-------------------------------------
                        bgcolor="#F9FFFB",
                        border=ft.border.all(1, "#D6E8D7"),
                        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK), offset=ft.Offset(0, 6)),
                        ##------------------------------
                        padding=20,
                        content=ft.Column([
                            ft.ListTile(title=ft.Text("Rest & Activity", weight="bold")),
                            ft.TextField(ref=entry_date_ref, label="Entry date (YYYY-MM-DD)", hint_text="e.g. 2026-01-08 (leave empty = today)"),
                            ft.Text("Sleeping Schedule", size=14, weight="bold"),
                            ft.TextField(ref=sleep_h_ref, label="Sleep Hours"),
                            ft.TextField(ref=sleep_i_ref, label="Sleep Interval"),
                            ft.Text("Fitness and Exercises", size=14, weight="bold"),
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
                        ])
                    )
                )
            ], col={"sm": 12, "md": 6}),

            ft.Column(
                    [image_card1],
                    col={"sm": 12, "md": 6},
            ),
        ], spacing=20,
            alignment=ft.MainAxisAlignment.START,##################################################
        ),
      # ft.Column([image_card1], col={"sm": 12, "md": 6}),

        ft.Container(height=20),
        ft.Row([
            ft.FilledButton("Save My Day", icon="save", on_click=save_clicked, width=300, height=50),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=40),
    ], visible=True)

    #---------------------------------------------
    #STATISTICS
    #---------------------------------------------
    # STATISTICS (serii actualizabile din refresh_stats)
    sleep_series = ft.LineChartData(
        data_points=[],
        stroke_width=4,
        #color=ft.Colors.BLUE,
        #curved=True,
        #below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
        color="#43A047", 
        curved=True,
        below_line_bgcolor=ft.Colors.with_opacity(0.12, "#66BB6A"),
        point=True,
    )

    burned_series = ft.LineChartData(
        data_points=[],
        stroke_width=4,
        #color=ft.Colors.BLUE,
        #curved=True,
        #below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
        color="#43A047", 
        curved=True,
        below_line_bgcolor=ft.Colors.with_opacity(0.12, "#66BB6A"),
        point=True,
    )

    consumed_series = ft.LineChartData(
        data_points=[],
        stroke_width=4,
        #color=ft.Colors.BLUE,
        #curved=True,
        #below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
        color="#43A047", 
        curved=True,
        below_line_bgcolor=ft.Colors.with_opacity(0.12, "#66BB6A"),
        point=True,
    )

    happiness_series = ft.LineChartData(
        data_points=[],
        stroke_width=4,
        #color=ft.Colors.BLUE,
        #curved=True,
        #below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
        color="#43A047", 
        curved=True,
        below_line_bgcolor=ft.Colors.with_opacity(0.12, "#66BB6A"),
        point=True,
    )


    feedback_text_ref = ft.Ref[ft.Text]() ## pt caseta AI

    feedback_card = ft.Card(
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,##########################
            padding=20,
            content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME, color=ft.Colors.AMBER_700),
                ft.Text("AI Personalized Insights", size=20, weight="bold", color=ft.Colors.BLUE_900),
            ]),
            ft.Divider(),
            ft.Text(
                ref=feedback_text_ref,
                value="Please insert today's data and you'll receive some meniu ideas!",
                size=16,
                color=ft.Colors.GREY_800,
                italic=True,
            ),
            ft.Container(height=10),
            ft.Text("💡 Meniu Recommendations:", weight="bold", color=ft.Colors.GREEN_700),
            feedback_display,
            ])
        ),
        elevation=4,
    )

    stats_view = ft.Column(
    [
        #ft.Text("Statistics dashboard", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        ft.Text(
             "Statistics dashboard",
             size=40,
             weight="bold",
             color="#1B5E20",   
             text_align=ft.TextAlign.CENTER,
            ),
        stats_summary_text,
        ft.FilledButton("Refresh stats", on_click=lambda _: refresh_stats(), bgcolor=ft.Colors.GREEN_600),
        ft.Text("Hours Slept in the last 7 Days", color=ft.Colors.GREY_700),

        ft.Container(
            content=ft.LineChart(
                data_series=[sleep_series],
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
                data_series=[burned_series],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=0,
                max_y=1000,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(0, 3501, 500)],
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
                data_series=[consumed_series],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=0,
                max_y=3500,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(0, 3501, 500)],
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
        ft.Text("Happiness level in the last 7 Days", color=ft.Colors.GREY_700),

        ft.Container(
            content=ft.LineChart(
                data_series=[happiness_series],
                border=ft.border.all(1, ft.Colors.GREY_300),
                min_y=0,
                max_y=10,
                min_x=0,
                max_x=6,
                baseline_x=0,
                left_axis=ft.ChartAxis(
                    labels=[ft.ChartAxisLabel(value=i, label=ft.Text(str(i))) for i in range(0, 11, 1)],
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
          #------------THE FEEDBACK RESPONSE----------------------------------
       ft.Container(height=16),
       feedback_card,
    ],
    visible=False,
    expand=True,
    )


   #---------------------------------------------------------------
    page.navigation_bar = ft.NavigationBar(
        bgcolor="#A5D6A7",
        destinations=[
            ft.NavigationBarDestination(icon="edit_note", label="My Journal"),
            ft.NavigationBarDestination(icon="insert_chart", label="Statistics"),
        ],
        on_change=navigate
    )

    ###################################################################
    
    login_container = get_login_view(page, handle_login_success) 
    journal_view.visible = False 
    page.navigation_bar.visible = False
    page.add(login_container, journal_view, stats_view)
    #---------------------------------------------------------------
   

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, assets_dir="assets")
