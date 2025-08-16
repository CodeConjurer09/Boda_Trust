from rest_framework.routers import DefaultRouter
from .views import SystemSettingViewSet, AdminLogViewSet

router = DefaultRouter()
router.register(r'system-settings', SystemSettingViewSet)
router.register(r'admin-logs', AdminLogViewSet)

urlpatterns = router.urls