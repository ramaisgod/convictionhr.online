from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', cvrepo_home, name='cvrepo_home'),
    path('my_repository/', my_repository, name='my_repository'),
    path('search_cv/', search_cv, name='search_cv'),
    path('cv_download/<int:id>/', cv_download, name='cv_download'),
    path('upload_cv/', upload_cv, name='upload_cv'),
    path('auto_upload_cv/', auto_upload_cv, name='auto_upload_cv'),
    path('auto_upload_cv/<int:id>/', edit_auto_upload_cv, name='edit_auto_upload_cv'),
    path('edit_cv/<int:id>/', edit_cv, name='edit_cv'),
    path('view_cv/<int:id>/', view_cv, name='view_cv'),
]
