from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, SubEventViewSet,ComponentViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'sub-events', SubEventViewSet)  # Registering SubEvent
router.register(r'components', ComponentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
