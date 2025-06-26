from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from portail import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'), namespace='core')),

    path('professeur/', include(('prof.urls', 'prof'), namespace='prof')),
    path('etudiant/', include(('etudiant.urls', 'etudiant'), namespace='etudiant')),
    path('administrateur/', include(('school_admin.urls', 'school_admin'), namespace='school_admin')),
    path('', views.login_view, name='login_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)