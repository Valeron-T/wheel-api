from celery import Celery
from app import celeryconfig


def make_celery():
    app = Celery("wheel-api")
    app.config_from_object(celeryconfig.Config)

    return app


celery = make_celery()
