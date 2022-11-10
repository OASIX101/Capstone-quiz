from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
admin.site.site_header = 'Capstone Quiz'
admin.site.site_title = 'Capstone Quiz'
admin.site.index_title = 'Capstone Quiz'



schema_view = get_schema_view(
   openapi.Info(
      title="Quiz",
      default_version='v1',
      description="API for capstone quiz project",
      contact=openapi.Contact(email="anthonyolowuxx6@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Capstone_users.urls')),
    path('', include('Capstone_app.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns