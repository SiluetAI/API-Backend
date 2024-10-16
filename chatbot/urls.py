# chatbot/urls.py
from django.urls import path
from .views import HomeTemplateView, ManychatWebhookView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),  # Root URL with HTML
    path('api/manychat_webhook/', ManychatWebhookView.as_view(), name='manychat_webhook'),
]
