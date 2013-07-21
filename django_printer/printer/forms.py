from django import forms

from .fields import (
    BergCloudDateTimeField
)


class BergCloudParametersForm(forms.Form):
    """
    A form that defines the common query params passed by
    BergCloud whilst requesting an edition
    """
    local_delivery_time = BergCloudDateTimeField(required=False)
    delivery_count = forms.IntegerField(required=False)


class BergCloudPublicationForm(BergCloudParametersForm):

    def get_meta(self):
        if hasattr(self, 'meta'):
            return self.meta
        raise NotImplementedError(
            'Set meta attribute on your publication form'
        )

    def etag(self):
        raise NotImplementedError(
            'You must provide an etag function for your publication'
        )

    def get_render_context(self):
        raise NotImplementedError(
            'Override this function to provide context data '
            'for your publication template'
        )
