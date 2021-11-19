from django.apps import AppConfig


class F11CustomersConfig(AppConfig):
    name = 'f_1_1_customers'

    def ready(self):
        import f_1_1_customers.signals
