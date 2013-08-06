import hashlib

from printer.views import EditionView

from .forms import HelloWorldPublicationForm


class HelloWorldView(EditionView):
    """
    Edition view for the Hello World example
    """
    form_class = HelloWorldPublicationForm
    template_name = 'publication/hello_world.html'

    def etag(self, context):
        """
        Gets passed the context and generates
        an etag for this publication
        """
        return hashlib.sha224(
            "".join([str(value) for value in context.values()])
        ).hexdigest()

    def get_context_data(self, **kwargs):
        """
        Gets passed the validated form and returns a dictionary
        of context to be used during template rendering
        """
        form = kwargs.get('form')
        name = form.cleaned_data.get('name')
        lang = form.cleaned_data.get('lang', 'english')
        date = form.cleaned_data.get('local_delivery_time')

        # Pick a time of day appropriate greeting
        i = 0
        if 12 < date.hour <= 17:
            i = 1
        if 17 < date.hour <= 24 or 0 < date.hour <= 3:
            i = 2

        return {
            'name': name,
            'lang': lang,
            'date': date,
            'greeting': form.greetings[lang][i] + " {}".format(name)
        }