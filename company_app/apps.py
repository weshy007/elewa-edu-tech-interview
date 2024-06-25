from django.apps import AppConfig


class CompanyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company_app'

    def ready(self):
        import company_app.signals