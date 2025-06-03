from django.contrib import admin
from django.urls import path, include

from portail import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'), namespace='core')),

    path('professeur/', include(('prof.urls', 'prof'), namespace='prof')),
    path('etudiant/', include(('etudiant.urls', 'etudiant'), namespace='etudiant')),
    path('', views.login_view, name='login_view'),
]
