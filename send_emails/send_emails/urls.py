from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.user_login, name='login'),
    path('send_email/', accounts_views.send_email, name='send_email'),
    path('', accounts_views.user_login, name='root'),
]