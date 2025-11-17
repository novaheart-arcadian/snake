# generate_dlc_tokens.py
import secrets, os

OUT = "dlc_tokens"
os.makedirs(OUT, exist_ok=True)

packs = [("COINS100", 100, 100), ("COINS300", 300, 50), ("COINS1000", 1000, 10)]
# formato: (prefix, coins, quantity) -> genera 'quantity' archivos por pack

for prefix, coins, qty in packs:
    for i in range(qty):
        token = f"{prefix}-{secrets.token_hex(8).upper()}"
        fname = f"{OUT}/{token}.dlc"
        with open(fname, "w") as f:
            f.write(token)
        print("Creado:", fname, "->", coins)
