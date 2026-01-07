import os
import shutil
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg):
    print(msg)
    sys.stdout.flush()

def run(cmd):
    log("[CMD] " + " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in proc.stdout:
        log("  " + line.rstrip())
    if proc.wait() != 0:
        raise RuntimeError("Comando falhou")

def generate_iso(
    iso_name="custom_linux.iso",
    volume_label="CUSTOM_LINUX"
):
    work = os.path.join(BASE_DIR, "iso_work")
    out = os.path.join(BASE_DIR, "output")

    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)

    # limpeza
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)

    log("[INFO] Criando estrutura ISO")

    os.makedirs(f"{work}/boot/grub", exist_ok=True)
    os.makedirs(f"{work}/EFI/BOOT", exist_ok=True)
    os.makedirs(f"{work}/live", exist_ok=True)

    # arquivos obrigatórios
    shutil.copy("filesystem.squashfs", f"{work}/live/filesystem.squashfs")
    shutil.copy("vmlinuz", f"{work}/boot/vmlinuz")
    shutil.copy("initrd.img", f"{work}/boot/initrd.img")

    # grub.cfg
    grub_cfg = f"""
set timeout=5
set default=0

menuentry "Boot Custom Linux" {{
    linux /boot/vmlinuz boot=live quiet
    initrd /boot/initrd.img
}}
"""
    with open(f"{work}/boot/grub/grub.cfg", "w") as f:
        f.write(grub_cfg.strip())

    log("[INFO] Gerando GRUB EFI")
    run([
        "grub-mkstandalone",
        "-O", "x86_64-efi",
        "-o", f"{work}/EFI/BOOT/BOOTX64.EFI",
        f"boot/grub/grub.cfg={work}/boot/grub/grub.cfg"
    ])

    log("[INFO] Gerando GRUB BIOS")
    run([
        "grub-mkstandalone",
        "-O", "i386-pc",
        "-o", f"{work}/boot/grub/core.img",
        f"boot/grub/grub.cfg={work}/boot/grub/grub.cfg"
    ])

    log("[INFO] Criando ISO híbrida BIOS/UEFI")

    iso_path = os.path.join(out, iso_name)

    run([
        "xorriso", "-as", "mkisofs",
        "-iso-level", "3",
        "-full-iso9660-filenames",
        "-volid", volume_label,
        "-eltorito-boot", "boot/grub/core.img",
        "-eltorito-catalog", "boot/grub/boot.cat",
        "-no-emul-boot",
        "-boot-load-size", "4",
        "-boot-info-table",
        "--eltorito-alt-boot",
        "-e", "EFI/BOOT/BOOTX64.EFI",
        "-no-emul-boot",
        "-isohybrid-gpt-basdat",
        "-output", iso_path,
        work
    ])

    log(f"[OK] ISO criada com sucesso: {iso_path}")

if __name__ == "__main__":
    generate_iso()
