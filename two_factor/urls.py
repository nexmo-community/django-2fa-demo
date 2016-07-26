from django.conf.urls import url

from . import views

app_name = 'two_factor'
urlpatterns = [
    url(r'^$', views.NewView.as_view(), name='new'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^verify/$', views.VerifyView.as_view(), name='verify'),
    url(r'^confirm/$', views.ConfirmView.as_view(), name='confirm'),
]
