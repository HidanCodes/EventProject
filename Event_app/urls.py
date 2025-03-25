from django.urls import path

from Event_app.views import EventListCreateView, EventDetailView

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),

]