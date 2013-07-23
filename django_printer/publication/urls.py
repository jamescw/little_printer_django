from django.conf.urls import patterns, url
from django.templatetags.static import static
from django.views.generic import TemplateView, RedirectView

from printer.views import ValidateConfigView, MetaView

from .forms import HelloWorldPublicationForm
from .views import HelloWorldView


urlpatterns = patterns('',

    url(
        r'^meta.json$',
        MetaView.as_view(
            form_class = HelloWorldPublicationForm,
        )
    ),
    url(
        r'^icon.png$',
        RedirectView.as_view(
            url=static('icon.png')
        )
    ),
    url(
        r'^sample/$',
        TemplateView.as_view(
            template_name = 'publication/sample.html',
        )
    ),
    url(
        r'^edition/$',
        HelloWorldView.as_view()
    ),
    url(
        r'^validate_config/$',
        ValidateConfigView.as_view(
            form_class = HelloWorldPublicationForm,
        )
    ),
    
)