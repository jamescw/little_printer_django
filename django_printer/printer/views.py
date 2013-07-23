"""
Base views for BERG Cloud publications.
Publications should subclass EditionView.
"""
import json

from django.http import HttpResponse
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.core.exceptions import ImproperlyConfigured

from .forms import BergCloudPublicationForm


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object
        """
        return json.dumps(context)


class MetaView(JSONResponseMixin, FormView):
    """
    Returns a meta file for this publication which
    is dynamically generated from the publication
    form_class

    Satisfies:
    http://remote.bergcloud.com/developers/reference/metajson
    """
    def __init__(self, **kwargs):
        """
        Overrides base to make sure a form_class is set
        """
        super(MetaView, self).__init__(**kwargs)
        if not getattr(self, 'form_class', None):
            raise ImproperlyConfigured(
                'You must set a form_class on {}'
                'in url config or subclasses'.format(self)
            )

    def get(self, request, *args, **kwargs):
        """
        Constructs meta JSON by taking meta header
        from the form_class and including its
        serialized fields except for those sent
        by BERG Cloud
        """
        form = self.get_form(self.get_form_class())
        berg_params = BergCloudPublicationForm()
        meta = form.get_meta()
        fields_meta = []
        for name, instance in form.fields.items():
            # ignore fields that are required by Berg
            if name not in berg_params.fields:
                # serialise field and add to fields list
                fields_meta.append(instance.serialise(name))
        if fields_meta:
            meta['config'] = {'fields': fields_meta}
        return self.render_to_json_response(meta)


class EditionView(FormView):
    """
    Parse the incoming request from BERG Cloud
    and respond with edition content

    Satisfies:
    http://remote.bergcloud.com/developers/reference/edition
    """
    def get(self, request, *args, **kwargs):
        """
        Forces form validation
        """
        self.post(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Wraps GET params into a dict that
        can be validated by the form class
        """
        return {'data': self.request.GET}

    def form_valid(self, form):
        """
        If the form is valid render publication
        """
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
        response['ETag'] = self.etag(context)
        return response

    def etag(self, context):
        """
        Returns an ETag for this edition
        based on the passed in context
        """
        raise NotImplementedError(
            'You must override the etag function '
            'to provide an ETag for your publication'
        )

    def get_context_data(self, **kwargs):
        """
        Returns content for the publication template
        """
        raise NotImplementedError(
            'You must override get_context to provide '
            'context data for your publication template'
        )


class ValidateConfigView(JSONResponseMixin, FormView):
    """
    Uses the native Django form validation to validate
    user choices sent from BERG Cloud

    Satisfies:
    http://remote.bergcloud.com/developers/reference/validate_config
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        """
        Override dispatch to make this view CSRF exempt
        """
        return super(ValidateConfigView, self).dispatch(
            *args,
            **kwargs
        )

    def get_form_kwargs(self):
        """
        Parse form parameters from config param
        """
        return {
            'data': json.loads(
                self.request.POST.get('config')
            )}

    def form_valid(self, form):
        """
        If the form is valid simply return true
        """
        return self.render_to_json_response(
            {'valid': True}
        )

    def form_invalid(self, form):
        """
        If the form is invalid, return a list of errors
        """
        return self.render_to_json_response({
            'valid': False,
            'errors': [error[0] for error in form.errors.values()]
        })
