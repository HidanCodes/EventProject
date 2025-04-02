from django.urls import path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Event_app.views import EventListCreateView, EventDetailView, RegisterView, JoinEventView, LeaveEventView, \
    MyEventsView


schema_view = get_schema_view(
   openapi.Info(
      title="API مستندات",
      default_version='v1',
      description="توضیحات API شما",
      terms_of_service="https://www.yourapp.com/terms/",
      contact=openapi.Contact(email="contact@yourapp.com"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/join/', JoinEventView.as_view(), name='event-join'),
    path('events/<int:pk>/leave/', LeaveEventView.as_view(), name='event-leave'),
    path('events/myevents/', MyEventsView.as_view(), name='my-events'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]