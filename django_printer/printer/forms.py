"""
Base forms for creating forms that
validate requests from BERG Cloud
"""
from django import forms

from .fields import (
    BergCloudDateTimeField
)


class BergCloudPublicationForm(forms.Form):
    """
    A form that defines the common query params passed by
    BERG Cloud whilst requesting an edition
    """
    local_delivery_time = BergCloudDateTimeField(required=False)
    delivery_count = forms.IntegerField(required=False)

    def get_meta(self):
        """
        Gets meta data for the publication
        """
        if hasattr(self, 'meta'):
            return self.meta
        raise NotImplementedError(
            'Set meta attribute on your publication form'
        )

