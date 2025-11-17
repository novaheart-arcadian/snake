import json
import os

DATA_FILE = "save_data.json"


# ========================
#   SISTEMA DE GUARDADO
# ========================

def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "coins": 0,
            "owned_skins": ["classic"],
            "equipped_skin": "classic"
        }
        save_data(data)
        return data

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ========================
#     SISTEMA DE SKINS
# ========================

SKINS = {
    "classic": {
        "price": 0,
        "color": (0, 255, 0)
    },
    "fire": {
        "price": 150,
        "color": (255, 80, 0)
    },
    "neon": {
        "price": 300,
        "color": (0, 255, 255)
    },
    "gold": {
        "price": 1000,
        "color": (255, 215, 0)
    }
}


def get_equipped_color(data):
    skin_name = data["equipped_skin"]
    return SKINS[skin_name]["color"]


def buy_skin(data, skin_name):
    if skin_name in data["owned_skins"]:
        return "Ya posees esta skin."

    price = SKINS[skin_name]["price"]
    if data["coins"] < price:
        return "No tienes suficientes monedas."

    data["coins"] -= price
    data["owned_skins"].append(skin_name)
    save_data(data)
    return f"Skin '{skin_name}' comprada."


def equip_skin(data, skin_name):
    if skin_name not in data["owned_skins"]:
        return "No tienes esta skin."

    data["equipped_skin"] = skin_name
    save_data(data)
    return f"Skin '{skin_name}' equipada."


# ========================
#         DLC
# ========================

def redeem_dlc_file(filepath, data):
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()

        if content == "COINS100":
            data["coins"] += 100
        elif content == "COINS300":
            data["coins"] += 300
        elif content == "COINS1000":
            data["coins"] += 1000
        else:
            return "Archivo DLC inválido."

        save_data(data)
        return "DLC canjeado con éxito."

    except:
        return "Error leyendo archivo."


# ========================
#       SISTEMA MONEDAS
# ========================

def add_coins(data, amount):
    data["coins"] += amount
    save_data(data)


def spend_coins(data, amount):
    if data["coins"] >= amount:
        data["coins"] -= amount
        save_data(data)
        return True
    else:
        return False
