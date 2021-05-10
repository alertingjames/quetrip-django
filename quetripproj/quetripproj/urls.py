from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from quetrip import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^quetrip/', include('quetrip.urls')),
    url(r'^imageagent/', include('imageagent.urls')),
    url(r'^rakubaru/', include('rakubaru.urls')),
    # url(r'^$', views.index, name='index'),

    url(r'^registerCustomer',views.registerCustomer,  name='registerCustomer'),
    url(r'^quetrip_verify',views.quetrip_verify,  name='quetrip_verify'),
    url(r'^login',views.login,  name='login'),
    url(r'^sociallogin',views.sociallogin,  name='sociallogin'),

    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^rstpwd', views.rstpwd, name='rstpwd'),

    url(r'^updateCustomer', views.updateCustomer, name='updateCustomer'),
    url(r'^getloc', views.getloc, name='getloc'),


    #################################### Jitsi Video Conference ###################################################################################

    url(r'^openJitsiVideo', views.openJitsiVideo, name='openJitsiVideo'),


    #################################### Admob Ads Test ###################################################################################

    url(r'^ads', views.ads, name='ads'),
]


urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


































