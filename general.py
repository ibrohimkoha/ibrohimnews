from database import SessionLocal

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

async def get_session():
    get_session = SessionLocal()
    try:
        yield get_session
    finally:
        get_session.close()