
import requests, os, sys, shutil, stat
from pathlib import Path

REPO = "novaheart-arcadian/snake"  # cambia a "novaheart-arcadian/snake"
CURRENT = "v1.0.0"           # opcional, versión actual; también se puede leer de un archivo

API_RELEASES = f"https://api.github.com/repos/snake/releases/latest"
DOWNLOAD_DIR = Path.cwd() / "update_tmp"

def get_latest_release_info():
    r = requests.get(API_RELEASES)
    r.raise_for_status()
    return r.json()

def select_asset(release_json):
    # intenta encontrar el build para la plataforma actual
    import platform
    plat = platform.system().lower()
    for a in release_json.get("assets", []):
        name = a["name"].lower()
        if plat.startswith("windows") and name.endswith(".exe"):
            return a
        if plat.startswith("linux") and ("appimage" in name or name.endswith(".bin") or name.endswith(".run") or name.endswith(".x86_64")):
            return a
        if plat.startswith("darwin") and name.endswith(".dmg"):
            return a
    return None

def download_asset(asset):
    url = asset["browser_download_url"]
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    local = DOWNLOAD_DIR / asset["name"]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local

def replace_current_executable(new_path):
    # Implementación simple: mover nuevo ejecutable sobre el actual (plataforma específica)
    exe_path = Path(sys.argv[0]).resolve()
    backup = exe_path.with_suffix(".old")
    try:
        # renombrar actual a .old
        exe_path.replace(backup)
        new_path.replace(exe_path)
        # permitir ejecución en linux
        exe_path.chmod(exe_path.stat().st_mode | stat.S_IEXEC)
        print("Actualización aplicada. Reinicia la aplicación.")
    except Exception as e:
        print("Error aplicando actualización:", e)
        # revertir si falló
        if backup.exists():
            backup.replace(exe_path)

def run_update():
    info = get_latest_release_info()
    asset = select_asset(info)
    if not asset:
        print("No se encontró un artefacto compatible en la última release.")
        return
    print("Descargando:", asset["name"])
    local = download_asset(asset)
    replace_current_executable(local)

if __name__ == "__main__":
    try:
        run_update()
    except Exception as e:
        print("Error en updater:", e)
