from django.views.generic.base import TemplateView
from .models import Contact


class Info_view(TemplateView):

    template_name = "my_info_template.html"

    def get_context_data(self, **kwargs):
        context = super(Info_view, self).get_context_data(**kwargs)
        context['info'] = Contact.objects.first()
        return context
