from django.conf.urls import patterns, url
from django.templatetags.static import static
from django.views.generic import TemplateView, RedirectView


from printer.views import EditionView, ValidateConfigView, MetaView
from .forms import HelloWorldPublicationForm



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
        EditionView.as_view(
            form_class = HelloWorldPublicationForm,
            template_name = 'publication/hello_world.html',
        )
    ),
    url(
        r'^validate_config/$',
        ValidateConfigView.as_view(
            form_class = HelloWorldPublicationForm,
        )
    ),
    
)