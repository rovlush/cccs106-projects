import flet as ft
from weather_service import get_weather




def main(page: ft.Page):
    page.title = "Weather App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.bgcolor = "#F5F7FE"


    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------
    def fmt(value, suffix=""):
        try:
            if value is None:
                return "N/A"
            return f"{round(float(value), 1)}{suffix}"
        except:
            return str(value)


    def choose_icon(desc: str):
        d = desc.lower()
        if "clear" in d: return "☀️"
        if "cloud" in d: return "☁️"
        if "rain" in d: return "🌧"
        if "thunder" in d: return "⛈"
        if "snow" in d: return "❄️"
        if "mist" in d or "fog" in d: return "🌫"
        return "🌥"


    # -------------------------------------------------------------------
    # Title bar (left) + Dark Mode button (right)
    # -------------------------------------------------------------------
    title_row = ft.Row(
        [
            ft.Row(
                [
                    ft.Icon(ft.Icons.CLOUD, size=32, color="#4EA1FF"),
                    ft.Text("Weather App", size=28, weight=ft.FontWeight.BOLD, color="#1E90FF"),
                ],
                spacing=10,
            ),
            ft.IconButton(
                icon=ft.Icons.DARK_MODE,
                icon_color="#4EA1FF",
                on_click=lambda e: toggle_theme(),
            ),
        ],
        alignment="spaceBetween",
        width=850,
    )


    # -------------------------------------------------------------------
    # Theme toggle
    # -------------------------------------------------------------------
    def toggle_theme():
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()


    # -------------------------------------------------------------------
    # Search input row
    # -------------------------------------------------------------------
    city_input = ft.TextField(
        prefix_icon=ft.Icons.LOCATION_CITY,
        hint_text="Enter city name",
        width=650,
        height=52,
        border_radius=14,
    )


    search_btn = ft.FilledButton(
        "Search",
        icon=ft.Icons.SEARCH,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=lambda e: search(),
    )


    search_row = ft.Row(
        [city_input, search_btn],
        alignment="start",
        spacing=15,
        width=850,
    )


    loader = ft.ProgressRing(visible=False)


    # -------------------------------------------------------------------
    # Metric card factory
    # -------------------------------------------------------------------
    def metric_card(emoji, label, value):
        return ft.Container(
            width=170,
            padding=15,
            bgcolor="white",
            border_radius=14,
            shadow=ft.BoxShadow(blur_radius=8, offset=ft.Offset(0, 3)),
            content=ft.Column(
                [
                    ft.Text(emoji, size=26),
                    ft.Text(label, size=14, color="grey"),
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment="center",
                spacing=4,
            ),
        )


    # -------------------------------------------------------------------
    # Main weather card (light blue box)
    # -------------------------------------------------------------------
    weather_card = ft.Container(
        width=850,
        border_radius=25,
        padding=30,
        bgcolor="#E7F1FF",
        content=ft.Column(
            [
                ft.Text("Enter a city and click Search", color="grey")
            ],
            horizontal_alignment="center",
        ),
    )


    # Snackbar for errors
    page.snack_bar = ft.SnackBar(ft.Text(""), bgcolor="#FFCDD2")


    # -------------------------------------------------------------------
    # Main Weather Loader Function
    # -------------------------------------------------------------------
    async def load_weather(city):
        loader.visible = True
        page.update()


        try:
            raw = await get_weather(city)


            city_name = raw["city"]
            country = raw["country"]
            desc = raw["description"]
            icon = choose_icon(desc)


            temp = raw["temperature"]
            feels = raw["feels_like"]
            tmax = raw["temp_max"]
            tmin = raw["temp_min"]
            hum = raw["humidity"]
            wind = raw["wind_speed"]
            pres = raw["pressure"]
            cloud = raw["cloudiness"]


            # Fill the weather card EXACTLY like Image #1
            weather_card.content = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCATION_ON, color="#1E90FF"),
                            ft.Text(
                                f"{city_name}, {country}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color="#08306B",
                            ),
                        ],
                        alignment="center",
                    ),


                    ft.Container(height=8),


                    ft.Text(icon, size=70),
                    ft.Text(desc, size=16, color="grey"),


                    ft.Text(f"{fmt(temp, '°C')}", size=58, weight=ft.FontWeight.BOLD, color="#1E3A8A"),


                    ft.Text(f"Feels like {fmt(feels, '°C')}", size=15, color="grey"),


                    ft.Row(
                        [
                            ft.Text(f"↑ {fmt(tmax, '°C')}", size=14),
                            ft.Text(f"↓ {fmt(tmin, '°C')}", size=14),
                        ],
                        alignment="center",
                        spacing=15,
                    ),


                    ft.Container(height=25),
                    ft.Container(bgcolor="#DDEEF9", height=1, width=750),
                    ft.Container(height=25),


                    ft.Row(
                        [
                            metric_card("💧", "Humidity", f"{fmt(hum, '%')}"),
                            metric_card("🌬️", "Wind Speed", f"{fmt(wind, ' m/s')}"),
                            metric_card("🔻", "Pressure", f"{fmt(pres, ' hPa')}"),
                            metric_card("☁️", "Cloudiness", f"{fmt(cloud, '%')}"),
                        ],
                        alignment="center",
                        spacing=20,
                    ),
                ],
                horizontal_alignment="center",
                spacing=8,
            )


        except Exception as e:
            page.snack_bar.content = ft.Text(str(e))
            page.snack_bar.open = True


        loader.visible = False
        page.update()


    # -------------------------------------------------------------------
    # Search handler
    # -------------------------------------------------------------------
    def search():
        city = city_input.value.strip()
        if not city:
            page.snack_bar.content = ft.Text("Please enter a city name")
            page.snack_bar.open = True
            page.update()
            return
        page.run_task(load_weather, city)


    city_input.on_submit = lambda e: search()


    # -------------------------------------------------------------------
    # Add UI to page
    # -------------------------------------------------------------------
    page.add(
        title_row,
        ft.Container(height=20),
        search_row,
        ft.Container(height=10),
        loader,
        ft.Container(height=10),
        weather_card,
    )




if __name__ == "_main_":
    ft.app(target=main)