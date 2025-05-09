import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io

def get_uuid():
    username = name_entry.get().strip()

    if not username:
        messagebox.showwarning("Hinweis", "Bitte gib einen Minecraft-Namen ein.")
        return

    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            uuid = data['id']
            result_label.config(
                text=f"Spielername: {data['name']}\nUUID: {uuid}",
                foreground="green"
            )
            uuid_copy_button.config(state="normal")
            uuid_copy_button.uuid = uuid 
            load_avatar(uuid)
        elif response.status_code == 204:
            result_label.config(text="Spieler nicht gefunden.", foreground="red")
            avatar_label.config(image="")
            uuid_copy_button.config(state="disabled")
        else:
            result_label.config(
                text=f"Fehler beim Abrufen (Code {response.status_code})",
                foreground="red"
            )
            avatar_label.config(image="")
            uuid_copy_button.config(state="disabled")
    except Exception as e:
        result_label.config(text=f"Ein Fehler ist aufgetreten: {e}", foreground="red")
        avatar_label.config(image="")
        uuid_copy_button.config(state="disabled")

def load_avatar(uuid):
    avatar_url = f"https://crafatar.com/avatars/{uuid}?size=100&overlay"
    try:
        response = requests.get(avatar_url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((64, 64), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            avatar_label.image = image
            avatar_label.config(image=image)
        else:
            avatar_label.config(text="Avatar konnte nicht geladen werden.")
    except Exception as e:
        avatar_label.config(text=f"Fehler beim Avatar: {e}")

def copy_uuid():
    if hasattr(uuid_copy_button, 'uuid'):
        root.clipboard_clear()
        root.clipboard_append(uuid_copy_button.uuid)
        messagebox.showinfo("Kopiert", "UUID wurde in die Zwischenablage kopiert.")

root = tk.Tk()
root.title("Minecraft UUID Checker")
root.geometry("360x320")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))

ttk.Label(root, text="Minecraft-Name eingeben:").pack(pady=(15, 5))
name_entry = ttk.Entry(root, width=30)
name_entry.pack()

ttk.Button(root, text="UUID abrufen", command=get_uuid).pack(pady=10)

avatar_label = tk.Label(root)
avatar_label.pack(pady=5)

result_label = ttk.Label(root, text="", wraplength=330, justify="center")
result_label.pack(pady=(10, 5))

uuid_copy_button = ttk.Button(root, text="UUID kopieren", command=copy_uuid, state="disabled")
uuid_copy_button.pack(pady=(5, 10))

root.mainloop()
