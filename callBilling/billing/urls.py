from django.urls import path
from billing import views


app_name = 'billing'
urlpatterns = [
    path('bill', views.source_billing, name='billing'),
]
