from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.views.static import serve
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from uttermost import settings
from uttermostcontent import views
from uttermostcontent.views import (
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,

)

# Custom error handlers
handler403 = 'uttermostcontent.views.custom_permission_denied_view'
handler404 = 'uttermostcontent.views.custom_404'
handler500 = 'uttermostcontent.views.error_500'

# Admin site customization
admin.site.site_header = 'Utter Most Admin'  # default: "Django Administration"
admin.site.index_title = 'Contents Area'  # default: "Site administration"
admin.site.site_title = 'Uttermost Site'  # default: "Django site admin"

urlpatterns = i18n_patterns(
    path('', include('uttermostcontent.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^rosetta/', include('rosetta.urls')),
    path('home/', TemplateView.as_view(template_name='users/dashboard/home.html'), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('', RedirectView.as_view(url='/admin/login/', permanent=False)),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', views.user_logout, name='logout'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
)

# Static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
