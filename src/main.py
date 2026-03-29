from dotenv import load_dotenv

from core import installer
import os

load_dotenv()

HOST = os.getenv("HOST")
KEY = os.getenv("KEY")
url = "https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-rustdesk86_64.erustdeske"

rustdesk = installer.RustDesk(url, HOST, KEY)

rustdesk.check_install()

if rustdesk.installed == False:
    rustdesk.download_installer()
    rustdesk.install()
    rustdesk.setup()
else:
    rustdesk.setup()
