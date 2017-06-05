from django.views.generic.base import TemplateView
from .models import Contact
from .form import My_add_data_form
from django.shortcuts import render
from django.contrib import auth
import json
from django.http import HttpResponse


class Info_view(TemplateView):

    template_name = "my_info_template.html"

    def get_context_data(self, **kwargs):
        context = super(Info_view, self).get_context_data(**kwargs)
        context['info'] = Contact.objects.first()
        return context


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            new_user = {'username': user.username}
            return HttpResponse(json.dumps(new_user), content_type="application/json")
        else:
            my_errors = {'user_error': "Your username and password didn't match."}
            return HttpResponse(json.dumps(my_errors), content_type="application/json")


def my_logout_view(request):
    logout_content = {'bay': 'Bay bay %s' % (request.user.username)}
    auth.logout(request)
    return HttpResponse(json.dumps(logout_content), content_type="application/json")


def my_edit_data(request, my_info_id):
    if request.user.is_authenticated():
        my_instance = Contact.objects.get(id=my_info_id)
        if request.method == 'POST':
            delete_foto=request.POST.get('delete_foto','2')
            form = My_add_data_form(request.POST, request.FILES, instance=my_instance)
            if form.is_valid():
                if int(delete_foto) == 1:
                    my_instance.image = ''
                my_instance = form.save()
                return HttpResponse(json.dumps({'ok': 'Data has been edit'}), content_type="application/json")
            elif form.errors:
                return HttpResponse(json.dumps(form.errors), content_type="application/json")
        else:
            form = My_add_data_form(instance=my_instance)
        return render(request, 'add_data.html', {'form': form, 'id': my_info_id})
    else:
        return render(request, 'login_error.html')
