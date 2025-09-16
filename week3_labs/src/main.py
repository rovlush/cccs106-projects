import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # Page setup
    page.title = "User Login"
    page.window_width = 400
    page.window_height = 350
    page.window_frameless = True
    # page.window_center()  # works only in older Flet
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # --- UI Controls ---
    title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER
    )

    username = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    password = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.PASSWORD,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
    )

    # --- Login Logic ---
    def login_click(e):
        uname = username.value.strip()
        pword = password.value.strip()

        # Invalid input
        if not uname or not pword:
            dlg = ft.AlertDialog(
                title=ft.Text("Input Error"),
                content=ft.Text("Please enter username and password", text_align="center"),
                actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
                icon=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE),
            )
            page.open(dlg)
            return

        try:
            conn = connect_db()
            if conn is None:
                raise mysql.connector.Error("Connection failed")

            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (uname, pword)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                dlg = ft.AlertDialog(
                    title=ft.Text("Login Successful"),
                    content=ft.Text(f"Welcome, {uname}!", text_align="center"),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
                    icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                )
            else:
                dlg = ft.AlertDialog(
                    title=ft.Text("Login Failed"),
                    content=ft.Text("Invalid username or password", text_align="center"),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
                    icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                )

            page.open(dlg)

        except mysql.connector.Error:
            dlg = ft.AlertDialog(
                title=ft.Text("Database Error"),
                content=ft.Text("An error occurred while connecting to the database"),
                actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))],
                icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.ORANGE),
            )
            page.open(dlg)

    # --- Login Button ---
    login_btn = ft.ElevatedButton(
        text="Login",
        width=100,
        icon=ft.Icons.LOGIN,
        on_click=login_click
    )

    # --- Layout ---
    page.add(
        title,
        ft.Column([username, password], spacing=20),
        ft.Container(
            content=login_btn,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(0, 20, 40, 0)
        )
    )

# Run the app
ft.app(target=main)
