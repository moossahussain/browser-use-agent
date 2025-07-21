import os
from dotenv import load_dotenv
import glob

load_dotenv()

BROWSER_EXECUTABLE = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
USER_PROFILE_DIR = '~/.config/browseruse/profiles/default'
DEFAULT_JSON_PATH = 'job_results/latest.json'  # symlink or latest file logic
RESUME_FILE = 'yourcv.pdf'
USER_NAME = 'user name'
USER_EMAIL = 'you@mail.com'
USER_PHONE = '000'




def get_latest_json(path: str = "job_results/*.json") -> str:
    files = sorted(glob.glob(path), key=os.path.getmtime, reverse=True)
    return files[0] if files else ""

DEFAULT_JSON_PATH = get_latest_json()
