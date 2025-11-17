# shop_dlc.py
# Tienda de skins + canjeo de packs de monedas por archivo DLC (itch.io)
#
# Requisitos: Python 3.x (tkinter viene con la mayoría de instalaciones de Python)
# Integración: importa las funciones y llama a show_shop() o a redeem_dlc_file()

import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

SAVE_FILE = "save_game.json"

# --- Datos de tienda y packs (prepara y sube archivos con estos tokens a itch.io) ---
SHOP_SKINS = {
    "skin_classic": {"display": "Clásico", "price": 0},
    "skin_neon":    {"display": "Neón",    "price": 150},
    "skin_retro":   {"display": "Retro",   "price": 250},
}

# Tokens para los packs DLC (los archivos que subirás a itch.io tendrán SOLO este token como contenido).
# Ejemplo: archivo 'coins100.dlc' cuyo contenido de texto es "COINS100"
DLC_TOKEN_TO_COINS = {
    "COINS100": 100,
    "COINS300": 300,
    "COINS1000": 1000,
}

# --- Helpers de guardado ---
def default_save():
    return {
        "coins": 0,
        "unlocked_skins": ["skin_classic"],
        "current_skin": "skin_classic",
        "used_tokens": []  # tokens ya canjeados (para evitar doble canje)
    }

def load_save():
    if not os.path.exists(SAVE_FILE):
        s = default_save()
        save_game(s)
        return s
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        s = default_save()
        save_game(s)
        return s

def save_game(save_data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=2)

# --- Funciones de tienda lógica ---
def add_coins(amount, save=None):
    s = save or load_save()
    s["coins"] += amount
    save_game(s)
    return s["coins"]

def buy_skin(skin_key, save=None):
    s = save or load_save()
    if skin_key not in SHOP_SKINS:
        return False, "Skin no existe"
    price = SHOP_SKINS[skin_key]["price"]
    if skin_key in s["unlocked_skins"]:
        return False, "Skin ya desbloqueada"
    if s["coins"] < price:
        return False, f"No tienes monedas suficientes ({s['coins']} < {price})"
    s["coins"] -= price
    s["unlocked_skins"].append(skin_key)
    s["current_skin"] = skin_key
    save_game(s)
    return True, "Skin comprada"

def equip_skin(skin_key, save=None):
    s = save or load_save()
    if skin_key not in s["unlocked_skins"]:
        return False, "Skin no desbloqueada"
    s["current_skin"] = skin_key
    save_game(s)
    return True, "Skin equipada"

# --- Canjear archivo DLC (lector de archivo descargado de itch.io) ---
def redeem_dlc_file(filepath, save=None):
    """
    filepath: ruta al archivo que el usuario ha descargado de itch.io.
    El archivo debería contener SOLO el token (p.ej. "COINS100") en texto plano.
    """
    if not os.path.exists(filepath):
        return False, "Archivo no encontrado"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            token = f.read().strip()
    except Exception as e:
        return False, f"Error leyendo archivo: {e}"

    if token not in DLC_TOKEN_TO_COINS:
        return False, "Token inválido"

    s = save or load_save()
    if token in s.get("used_tokens", []):
        return False, "Este pack ya fue canjeado anteriormente en esta instalación."

    coins = DLC_TOKEN_TO_COINS[token]
    s["coins"] = s.get("coins", 0) + coins
    s.setdefault("used_tokens", []).append(token)
    save_game(s)
    return True, f"Canje OK: +{coins} monedas"

# --- Interfaz simple de canje con diálogo de archivo (usa tkinter) ---
def redeem_dlc_dialog():
    root = tk.Tk()
    root.withdraw()  # no mostrar ventana principal
    filepath = filedialog.askopenfilename(title="Selecciona el archivo DLC comprado")
    if not filepath:
        return False, "Cancelado"
    ok, msg = redeem_dlc_file(filepath)
    messagebox.showinfo("Resultado canje", msg if ok else f"Error: {msg}")
    return ok, msg

# --- Interfaz textual/console simple para la tienda (útil para testing) ---
def show_shop_console():
    s = load_save()
    print("=== TIENDA ===")
    print(f"Monedas: {s['coins']}")
    for k,v in SHOP_SKINS.items():
        status = "DESBLOQUEADA" if k in s["unlocked_skins"] else f"Precio: {v['price']}"
        print(f"{k} - {v['display']} - {status}")
    print("\nComandos: buy <skin_key>, equip <skin_key>, redeemfile <path>, exit")
    while True:
        cmd = input("> ").strip().split()
        if not cmd: continue
        if cmd[0] == "exit": break
        if cmd[0] == "buy" and len(cmd) > 1:
            ok,msg = buy_skin(cmd[1])
            print(msg)
        elif cmd[0] == "equip" and len(cmd) > 1:
            ok,msg = equip_skin(cmd[1])
            print(msg)
        elif cmd[0] == "redeemfile" and len(cmd) > 1:
            ok,msg = redeem_dlc_file(cmd[1])
            print(msg)
        elif cmd[0] == "redeem":
            redeem_dlc_dialog()
        else:
            print("Comando no reconocido")

if __name__ == "__main__":
    # modo prueba por consola
    show_shop_console()
