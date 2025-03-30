from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Event_app.views import EventListCreateView, EventDetailView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),


]