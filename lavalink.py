import os
import logging
import subprocess
from datetime import datetime

baselogger = logging.getLogger(__name__)
logging.basicConfig(format=f"[{datetime.utcnow()} %(name)s %(levelname)s] %(message)s", level=logging.INFO)
lavalink_directory = f"{os.getcwd()}/lavalink" # change this

request = f"cd {lavalink_directory} & java -jar Lavalink.jar"

baselogger.info(subprocess.run(request, shell=True))
