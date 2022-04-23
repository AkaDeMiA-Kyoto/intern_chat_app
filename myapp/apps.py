from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'

    # signals を参照してくれるよう設定を追加
    def ready(self):
        import myapp.signals
