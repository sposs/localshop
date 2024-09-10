import re

from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import RedirectView

import localshop.apps.dashboard.urls
import localshop.apps.packages.urls
from localshop import views
from localshop.apps.packages.views import SimpleIndex
from localshop.apps.packages.xmlrpc import handle_request

admin.autodiscover()

static_prefix = re.escape(settings.STATIC_URL.lstrip('/'))


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', include(localshop.apps.dashboard.urls)),

    # Default path for xmlrpc calls
    path('RPC2', handle_request),
    path('pypi', handle_request),

    path('repo/', include(localshop.apps.packages.urls)),

    # Backwards compatible url (except for POST requests)
    path('simple/', SimpleIndex.as_view(), {'repo': 'default'}),
    re_path(r'^simple/(?P<path>.*)',
        RedirectView.as_view(url='/repo/default/%(path)s')),

    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('localshop.apps.accounts.auth_urls')),
    path('accounts/', include('localshop.apps.accounts.urls')),
    path('admin/', admin.site.urls),
]
