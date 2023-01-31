from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path(
        "jinja",
        TemplateView.as_view(template_name="index_jinja.html"),
        name="index_jinja",
    ),
]
