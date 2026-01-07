import os
import shutil
import subprocess

def log(msg):
    print(msg)  # depois liga na GUI

def detect_squashfs():
    base = os.path.dirname(os.path.abspath(__file__))

    local_mk = os.path.join(base, "mksquashfs")
    local_un = os.path.join(base, "unsquashfs")

    if (
        os.path.isfile(local_mk)
        and os.access(local_mk, os.X_OK)
        and os.path.isfile(local_un)
    ):
        log(f"[OK] SquashFS LOCAL detectado: {local_mk}")
        return local_mk

    system = shutil.which("mksquashfs")
    if system:
        log("[WARN] Usando mksquashfs do sistema")
        return system

    raise RuntimeError(
        "mksquashfs não encontrado (local ou sistema)"
    )
from gui.app import App
App().mainloop()
