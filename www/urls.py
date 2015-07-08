# coding: utf-8

from __future__ import unicode_literals

from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static

import views


admin.autodiscover()

urlpatterns = i18n_patterns(
    '',
    # This view allows private files within MEDIA_ROOT to be downloaded
    url(r'^private-media/(?P<path>.*)$', views.PrivateMediaView.as_view(),
        name='private-media'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Render statics/media locally
    # from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Do explicit setup of django debug toolbar
    import debug_toolbar

    urlpatterns += patterns(
        '', url(r'^__debug__/', include(debug_toolbar.urls)))