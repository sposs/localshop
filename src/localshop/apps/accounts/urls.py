from django.urls import path, include, re_path

from localshop.apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('access-keys/', views.AccessKeyListView.as_view(), name='access_key_list'),
    path('access-keys/new', views.AccessKeyCreateView.as_view(), name='access_key_create'),
    re_path(r'^access-keys/(?P<pk>\d+)/', include([
        path('secret', views.AccessKeySecretView.as_view(), name='access_key_secret'),
        path('edit', views.AccessKeyUpdateView.as_view(), name='access_key_edit'),
        path('delete', views.AccessKeyDeleteView.as_view(), name='access_key_delete'),
    ])),

    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/create', views.TeamCreateView.as_view(), name='team_create'),
    re_path(r'^teams/(?P<pk>\d+)/', include([
        path('', views.TeamDetailView.as_view(), name='team_detail'),
        path('edit', views.TeamUpdateView.as_view(), name='team_edit'),
        path('delete', views.TeamDeleteView.as_view(), name='team_delete'),
        path('member-add', views.TeamMemberAddView.as_view(), name='team_member_add'),
        path('member-remove', views.TeamMemberRemoveView.as_view(), name='team_member_remove'),
    ]))
]
