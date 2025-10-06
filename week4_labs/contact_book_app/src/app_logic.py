import flet as ft
from database import (
    update_contact_db,
    delete_contact_db,
    add_contact_db,
    get_all_contacts_db,
)


def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView with optional search."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact

        # Avatar initials
        initials = "".join([part[0] for part in name.split()[:2]]).upper()

        contacts_list_view.controls.append(
            ft.Card(
                elevation=3,
                content=ft.Container(
                    padding=10,
                    content=ft.Row(
                        [
                            # Avatar with initials
                            ft.CircleAvatar(
                                content=ft.Text(initials),
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_400,
                            ),
                            ft.Column(
                                [
                                    ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                                    ft.Row(
                                        [ft.Icon(ft.Icons.PHONE, size=16), ft.Text(phone if phone else "N/A")]
                                    ),
                                    ft.Row(
                                        [ft.Icon(ft.Icons.EMAIL, size=16), ft.Text(email if email else "N/A")]
                                    ),
                                ],
                                expand=True,
                                spacing=3,
                            ),
                            ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, c=contact: open_edit_dialog(
                                            page, c, db_conn, contacts_list_view
                                        ),
                                    ),
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda _, cid=contact_id: delete_contact(
                                            page, cid, db_conn, contacts_list_view
                                        ),
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
            )
        )

    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn, search_field=None):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs

    # Validation
    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    else:
        name_input.error_text = None

    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    # Clear inputs
    for field in inputs:
        field.value = ""

    # Refresh contacts
    display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")

    # ✅ Updated SnackBar
    page.snack_bar = ft.SnackBar(ft.Text("Contact added!"))
    page.snack_bar.open = True
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view, search_field=None):
    """Shows confirmation before deleting a contact."""

    def confirm_delete(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")

        # ✅ Updated SnackBar
        page.snack_bar = ft.SnackBar(ft.Text("Contact deleted!"))
        page.snack_bar.open = True
        page.update()

    def cancel_delete(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_delete),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
    )

    page.dialog = dialog
    dialog.open = True
    page.update()


def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_field=None):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        if not edit_name.value.strip():
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return

        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")

        # ✅ Updated SnackBar
        page.snack_bar = ft.SnackBar(ft.Text("Contact updated!"))
        page.snack_bar.open = True
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, "open", False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )

    page.dialog = dialog
    dialog.open = True
    page.update()
