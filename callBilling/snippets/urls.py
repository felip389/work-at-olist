from django.conf.urls import url
from snippets import views


app_name = 'snippets'
urlpatterns = [
    url('', views.snippet_signaling)
]
