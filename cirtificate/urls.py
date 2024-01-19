# project/urls.py
from django.contrib import admin
from django.urls import path
from cirapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/form/', UserProfileListCreateView.as_view(), name='user-profile-list-create'),
    path('api/user_profiles/<int:user_id>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('form/',form, name='form'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    path('all/', all_users, name='all'),
    path('update_form/<int:user_id>/', update_form, name='update'),
    path('user_id/<int:user_id>/', user_id, name='user_id'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
