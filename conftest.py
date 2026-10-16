import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

from pages.chat_page import ChatPage

PORT = 5055
URL = f"http://127.0.0.1:{PORT}"


@pytest.fixture(scope="session")
def base_url():
    """Start the demo app once for the whole test run and stop it afterwards."""
    env = {**os.environ, "PORT": str(PORT)}
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=Path(__file__).parent, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            urllib.request.urlopen(URL, timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        proc.terminate()
        raise RuntimeError("Demo app did not start")
    yield URL
    proc.terminate()


@pytest.fixture
def chat(page):
    chat_page = ChatPage(page)
    chat_page.open()
    return chat_page
