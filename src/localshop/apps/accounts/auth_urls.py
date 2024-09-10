from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordChangeDoneView, \
    PasswordChangeView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.urls import reverse_lazy, path, re_path
from django.views.generic.base import RedirectView

from localshop.apps.accounts.views import login as login_view

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.OAUTH2_PROVIDER:
    urlpatterns.append(
        path('login/', RedirectView.as_view(
            url=reverse_lazy('social:begin', kwargs={
                'backend': settings.OAUTH2_PROVIDER
            }),
        ), name='login')
    )
else:
    urlpatterns.append(path('login/', login_view, name='login'))
