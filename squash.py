from core.tools import tool
from core.logger import log
import subprocess
def build_squashfs(r,o):log('squashfs');subprocess.run([tool('mksquashfs'),r,o,'-noappend'],check=True)
