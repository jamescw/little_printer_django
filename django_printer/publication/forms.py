import hashlib
from django import forms

from printer.fields import (
    BergCloudTextField,
    BergCloudSelectField
)
from printer.forms import (
    BergCloudPublicationForm
)


class HelloWorldPublicationForm(BergCloudPublicationForm):
    """
    The Hello World example encapsulated in a django form
    """
    meta = {
        "publication_api_version": "1.0",
        "name": "Hello World Example",
        "description": "Say Hello in a few languages",
        "delivered_on": "every Monday",
        "send_timezone_info": True,
        "send_delivery_count": False,
        "external_configuration": False,
    }
    greetings = {
        "english" : ["Good morning", "Hello", "Good evening"],
        "french" : ["Bonjour", "Bonjour", "Bonsoir"],
        "german" : ["Guten morgen", "Hallo", "Guten abend"],
        "spanish" : ["Buenos d&#237;as", "Hola", "Buenas noches"],
        "portuguese" : ["Bom dia", "Ol&#225;", "Boa noite"],
        "italian" : ["Buongiorno", "ciao", "Buonasera"],
        "swedish": ["God morgon", "Hall&#229;", "God kv&#228;ll"]
    }
    name = BergCloudTextField(
        label="Enter your name",
        error_messages={
            'required': 'Please enter your name'
        }
    )
    lang = BergCloudSelectField(
        label='Select your greeting language',
        choices=[
            ('english', 'English'),
            ('french', 'French'),
            ('german', 'German'),
            ('spanish', 'Spanish'),
            ('portuguese', 'Portuguese'),
            ('italian', 'Italian'),
            ('swedish', 'Swedish'),
        ],
        error_messages={
            'required': 'Please select a language from the select box.'
        }
    )

    def etag(self):
        """
        Generates an etag for this publication
        """
        name = self.cleaned_data.get('name')
        lang = self.cleaned_data.get('lang', 'english')
        date = self.cleaned_data.get('local_delivery_time')
        return hashlib.sha224(
            lang+name+date.strftime('%d%m%Y')
        ).hexdigest()

    def clean_lang(self):
        """
        Ensures the language choice is known to the form
        """
        lang = self.cleaned_data.get('lang', None)
        if not lang in self.greetings:
            raise forms.ValidationError(
                "We couldn't find the language you selected {}"
                " Please select another".format(lang)
            )
        return lang

    def get_render_context(self):
        """
        Returns a dictionary of context to be used during template rendering
        """
        lang = self.cleaned_data.get('lang', 'english')
        date = self.cleaned_data.get('local_delivery_time')

        # Pick a time of day appropriate greeting
        i = 0
        if date.hour >= 12 and date.hour <=17:
            i = 1
        if (date.hour > 17 and date.hour <=24) or (date.hour >= 0 and date.hour <= 3):
            i = 2

        return {
            'greeting': self.greetings[lang][i]
        }