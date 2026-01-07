from core.tools import tool
from core.logger import log
import subprocess
def make_iso(i,o):log('iso');subprocess.run([tool('xorriso'),'-as','mkisofs','-o',o,i],check=True)
