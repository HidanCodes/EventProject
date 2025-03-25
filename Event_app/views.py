from django.shortcuts import get_object_or_404
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

    def post(self, request):
        """
        ایجاد رویداد جدید
        """
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    """
    نمایش، به‌روزرسانی و حذف یک رویداد خاص
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        دریافت جزئیات یک رویداد
        """
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        به‌روزرسانی کامل رویداد
        """
        event = get_object_or_404(Event, pk=pk)

        # تنها سازنده می‌تواند رویداد را ویرایش کند
        if event.creator != request.user:
            return Response(
                {'detail': 'فقط سازنده مجاز به ویرایش رویداد است.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        حذف رویداد
        """
        event = get_object_or_404(Event, pk=pk)

        # تنها سازنده می‌تواند رویداد را حذف کند
        if event.creator != request.user:
            return Response(
                {'detail': 'فقط سازنده مجاز به حذف رویداد است.'},
                status=status.HTTP_403_FORBIDDEN
            )

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)