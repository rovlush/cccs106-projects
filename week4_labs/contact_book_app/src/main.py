import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact


def main(page: ft.Page):
    page.title = "Contact Book"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 700

    db_conn = init_db()

    # Contact list view (scrollable only for saved contacts)
    contacts_list_view = ft.ListView(
        expand=True,        # fills remaining space and scrolls
        spacing=10,
        auto_scroll=True,   # auto scrolls when new contact is added
    )

    # Search bar
    search_field = ft.TextField(
        label="Search contacts...",
        prefix_icon=ft.Icons.SEARCH,
        width=380,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, e.control.value),
    )

    # Input fields
    name_input = ft.TextField(label="Full Name", prefix_icon=ft.Icons.PERSON, width=350)
    phone_input = ft.TextField(label="Phone", prefix_icon=ft.Icons.PHONE, width=350)
    email_input = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, width=350)
    inputs = (name_input, phone_input, email_input)

    # Add contact button
    add_button = ft.ElevatedButton(
        text="➕ Add Contact",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_field),
    )

    # Dark mode toggle
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        page.update()

    theme_switch = ft.Switch(label="🌙 Dark Mode", on_change=toggle_theme)

    # Layout
    page.add(
        ft.Column(
            [
                # Header bar
                ft.Container(
                    bgcolor=ft.Colors.BLUE_500,
                    padding=15,
                    content=ft.Row(
                        [
                            ft.Text("📒 Contact Book", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            theme_switch,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
                ft.Divider(),

                # Add contact section
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            [
                                ft.Text("➕ Add New Contact", size=18, weight=ft.FontWeight.BOLD),
                                name_input,
                                phone_input,
                                email_input,
                                add_button,
                            ],
                            spacing=10,
                        ),
                    ),
                ),

                # Search + saved contacts
                search_field,
                ft.Text("👥 Saved Contacts", size=18, weight=ft.FontWeight.BOLD),

                # 👇 Scrollable saved contacts area
                ft.Container(
                    contacts_list_view,
                    expand=True,   # fills bottom area and scrolls
                ),
            ],
            spacing=15,
            expand=True,  # makes the column fill the whole page height
        )
    )

    # Load saved contacts
    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)
