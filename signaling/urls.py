from django.conf.urls import url
from signaling import views


app_name = 'signaling'
urlpatterns = [
    url('', views.signaling)
]
