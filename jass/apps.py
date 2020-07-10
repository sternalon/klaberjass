from django.apps import AppConfig


class JassConfig(AppConfig):
    name = 'jass'

    # importing signals so they are available outside of the models
    def ready(self):
        from jass import signals