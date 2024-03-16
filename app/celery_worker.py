from main import create_app

app = create_app()
app.app_context().push()

from app.initialize import celery