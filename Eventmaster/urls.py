from rest_framework_nested import routers
from .views import EventViewSet, SubEventViewSet, ComponentViewSet
from .views import EventViewSet, SubEventViewSet, ComponentViewSet

# Set up the base router
router = routers.DefaultRouter()
router.register(r'events', EventViewSet)

# Set up nested router for sub-events under events
events_router = routers.NestedDefaultRouter(router, r'events', lookup='event')
events_router.register(r'sub-events', SubEventViewSet, basename='event-sub-events')

# Set up nested router for components under sub-events
sub_events_router = routers.NestedDefaultRouter(events_router, r'sub-events', lookup='sub_event')
sub_events_router.register(r'components', ComponentViewSet, basename='sub-event-components')

urlpatterns = [
    *router.urls,
    *events_router.urls,
    *sub_events_router.urls,
]
