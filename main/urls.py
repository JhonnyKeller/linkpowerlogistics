from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('',views.route, name='home'),
    path('map/',views.map, name='removals'),
    path('privacy/',views.privacy, name='privacy'),
    path('quotation_forniture/',views.quotation_forniture, name='quotation_forniture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
