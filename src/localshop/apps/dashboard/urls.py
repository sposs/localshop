from django.urls import path, include, re_path

from localshop.apps.dashboard import views

app_name = 'dashboard'

repository_urls = [
    # Package urls
    path('packages/add/',
        views.PackageAddView.as_view(),
        name='package_add'),
    re_path(r'^packages/(?P<name>[-._\w]+)/', include([
        path('',
            views.PackageDetailView.as_view(),
            name='package_detail'),
        path('refresh-from-upstream/',
            views.PackageRefreshView.as_view(),
            name='package_refresh'),
        path('release-mirror-file/',
            views.PackageMirrorFileView.as_view(),
            name='package_mirror_file'),
    ])),

    # CIDR
    path('settings/cidr/',
        views.CidrListView.as_view(), name='cidr_index'),
    path('settings/cidr/create',
        views.CidrCreateView.as_view(), name='cidr_create'),
    re_path(r'^settings/cidr/(?P<pk>\d+)/edit',
        views.CidrUpdateView.as_view(), name='cidr_edit'),
    re_path(r'^settings/cidr/(?P<pk>\d+)/delete',
        views.CidrDeleteView.as_view(), name='cidr_delete'),

    # Credentials
    path('settings/credentials/',
        views.CredentialListView.as_view(),
        name='credential_index'),
    path('settings/credentials/create',
        views.CredentialCreateView.as_view(),
        name='credential_create'),
    re_path(r'^settings/credentials/(?P<access_key>[-a-f0-9]+)/secret',
        views.CredentialSecretKeyView.as_view(),
        name='credential_secret'),
    re_path(r'^settings/credentials/(?P<access_key>[-a-f0-9]+)/edit',
        views.CredentialUpdateView.as_view(),
        name='credential_edit'),
    re_path(r'^settings/credentials/(?P<access_key>[-a-f0-9]+)/delete',
        views.CredentialDeleteView.as_view(),
        name='credential_delete'),

    path('settings/teams/', views.TeamAccessView.as_view(), name='team_access'),
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('repositories/create', views.RepositoryCreateView.as_view(), name='repository_create'),

    re_path(r'^repositories/(?P<slug>[^/]+)/', include([
        path('', views.RepositoryDetailView.as_view(), name='repository_detail'),
        path('edit', views.RepositoryUpdateView.as_view(), name='repository_edit'),
        path('delete', views.RepositoryDeleteView.as_view(), name='repository_delete'),
        path('refresh', views.RepositoryRefreshView.as_view(), name='repository_refresh'),
    ])),

    re_path(r'^repositories/(?P<repo>[^/]+)/', include(repository_urls))

]
