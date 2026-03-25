from django.urls import path

from . import views

app_name = 'markdownfield'

urlpatterns = [
    path('preview/', views.markdown_preview, name='preview'),
]
