"""URL Configuration."""

from django.apps import apps as django_apps
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from config.settings import INSTALLED_APPS

admin.site.site_header = "CoreBase"
admin.site.site_title = "CoreBase Admin"
admin.site.index_title = "Panel de administración"

def robots_txt(request):
    return HttpResponse("User-agent: *\nDisallow: /\n", content_type="text/plain")


urlpatterns = [
    path("robots.txt", robots_txt),
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/tenants/", include("apps.tenants.urls")),
    path("api/tokens/", include("apps.api_tokens.urls")),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/plans/", include("apps.plans.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/watchdog/", include("apps.watchdog.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
]

if "debug_toolbar" in INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

for _app_config in django_apps.get_app_configs():
    if getattr(_app_config, "vigilo_module", False):
        _prefix = getattr(_app_config, "api_prefix", _app_config.label)
        urlpatterns += [path(f"api/{_prefix}/", include(f"{_app_config.name}.urls"))]
