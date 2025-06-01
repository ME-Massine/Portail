from django.contrib import admin
from django.urls import path, include

from portail import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('professeur/', include(('prof.urls', 'prof'), namespace='prof')),
    path('', views.login_view, name='login_view'),
]
