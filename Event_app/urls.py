from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Event_app.views import EventListCreateView, EventDetailView, RegisterView, JoinEventView, LeaveEventView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/join/', JoinEventView.as_view(), name='event-join'),
    path('events/<int:pk>/leave/', LeaveEventView.as_view(), name='event-leave'),
    #path('events/myevents/', MyEventsView.as_view(), name='my-events'),


]