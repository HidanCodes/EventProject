from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Event_app.models import Event
from Event_app.serializers import EventSerializer


class EventListCreateView(APIView):
    """
    نمایش لیست رویدادها و ایجاد رویداد جدید
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        دریافت لیست تمام رویدادها
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)