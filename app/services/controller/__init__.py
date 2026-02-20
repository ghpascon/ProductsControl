from .main import Controller
from app.core import settings

controller = Controller(db_url=settings.DATABASE_URL)
