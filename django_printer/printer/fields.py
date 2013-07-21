from dateutil import parser
from django import forms


class BergCloudDateTimeField(forms.DateTimeField):

    def to_python(self, value):
        if value:
            value = parser.parse(value)
        return value


class BergCloudTextField(forms.CharField):

    type = 'text'

    def serialise(self, name):
        return {
            'name': name,
            'type': self.type,
            'label': self.label,
        }


class BergCloudCheckboxField(forms.BooleanField):

    type = 'checkbox'

    def serialise(self, name):
        return {
            'name': name,
            'type': self.type,
            'label': self.label,
        }


class BergCloudSelectField(forms.ChoiceField):

    type = 'select'

    def serialise(self, name):
        return {
            'name': name,
            'type': self.type,
            'label': self.label,
            'options': [
                [choice[1], choice[0]]
                for choice in self.choices
            ]
        }


class BergCloudRadioField(BergCloudSelectField):

    type = 'radio'


