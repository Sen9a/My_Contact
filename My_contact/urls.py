from django.conf.urls import patterns, include, url
from hello.views import Info_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Info_view.as_view(), name='my_info'),
    url(r'^login$', 'hello.views.my_login_view', name='my_login'),
    url(r'^logout$', 'hello.views.my_logout_view', name='my_logout'),
    url(r'^to_form/(?P<my_info_id>\d+)/$', 'hello.views.my_edit_data', name='to_form'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
