from django.conf.urls import patterns, include, url
from hello.views import Info_view
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Info_view.as_view(), name='my_info'),
)
