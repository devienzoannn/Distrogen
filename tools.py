import os,shutil
from core.logger import log
def tool(n):
 p=f"tools/{n}";return p if os.path.exists(p) else shutil.which(n)
