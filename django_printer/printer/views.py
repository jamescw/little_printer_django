import json

from django.http import HttpResponse
from django.views.generic import FormView, View
from django.views.decorators.csrf import csrf_exempt

from .forms import BergCloudParametersForm


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


class MetaView(JSONResponseMixin, View):

    form_class = None

    def get(self, request):

        form = self.form_class()
        berg_params = BergCloudParametersForm()
        meta = form.meta
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
    Parse the incoming request from BergCloud
    and respond with edition content
    """
    def get_form_kwargs(self):
        return {'data': self.request.GET}

    def render_to_response(self, context, **response_kwargs):
        form = self.get_form(self.form_class)
        response = super(EditionView, self).render_to_response(
            form.get_render_context(),
            **response_kwargs
        )
        response['ETag'] = form.etag()
        return response


class ValidateConfigView(JSONResponseMixin, FormView):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ValidateConfigView, self).dispatch(
            *args,
            **kwargs
        )

    def get_form_kwargs(self):
        return {
            'data': json.loads(
                self.request.POST.get('config')
            )}

    def form_valid(self, form):
        return self.render_to_json_response(
            {'valid': True}
        )

    def form_invalid(self, form):
        return self.render_to_json_response({
            'valid': False,
            'errors': [error[0] for error in form.errors.values()]
        })
