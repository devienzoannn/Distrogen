from core.squash import build_squashfs
from core.iso import make_iso
from core.logger import log
import os,shutil
def build(p):os.makedirs('build/iso',exist_ok=True);shutil.copy(p['kernel'],'build/iso/kernel');build_squashfs(p['rootfs'],'build/iso/filesystem.squashfs');make_iso('build/iso',f"build/output/{p['output']}")
