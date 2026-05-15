from fastapi.templating import Jinja2Templates
from app.core.config import settings

templates = Jinja2Templates(directory="templates")

# Global variables available in all templates
templates.env.globals["settings"] = settings
