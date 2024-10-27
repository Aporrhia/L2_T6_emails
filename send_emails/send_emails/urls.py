from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from django.conf.urls import handler404
from django.conf.urls import handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.user_login, name='login'),
    path('logout/', accounts_views.user_logout, name='logout'),
    path('send_email/', accounts_views.send_email, name='send_email'),
    path('', accounts_views.user_login, name='root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.error_404'
handler500 = 'accounts.views.error_500'