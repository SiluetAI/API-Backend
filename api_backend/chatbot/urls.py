# chatbot/urls.py
from django.urls import path
from .views import HomeView, ManychatWebhookView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Root URL
    path('api/manychat_webhook/', ManychatWebhookView.as_view(), name='manychat_webhook'),
]
