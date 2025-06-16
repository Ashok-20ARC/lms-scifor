from django.apps import AppConfig

<<<<<<< HEAD
=======

>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

<<<<<<< HEAD
    # 🔔 Automatically connect signals when app is ready
    def ready(self):
        import accounts.signals  # Signal for email verification, etc.
=======
    def ready(self):
        import accounts.signals
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
