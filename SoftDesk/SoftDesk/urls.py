from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# from features.urls import router as features_router
# from accounts.urls import router as accounts_router
from api.urls import router as api_router


router = routers.DefaultRouter()
# router.registry.extend(features_router.registry)
# router.registry.extend(accounts_router.registry)
router.registry.extend(api_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # ACCOUNTS
    path('user/', include('dj_rest_auth.urls')),

    # FEATURES
]
