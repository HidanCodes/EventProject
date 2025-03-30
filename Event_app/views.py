from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from Event_app.models import Event
from Event_app.serializers import EventSerializer, UserSimpleSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSimpleSerializer(data=request.data)

        if serializer.is_valid():
            # حذف فیلد تایید رمز عبور قبل از ذخیره سازی
            validated_data = serializer.validated_data
            validated_data.pop('password2')

            # هش کردن رمز عبور
            validated_data['password'] = make_password(validated_data['password'])

            # ایجاد کاربر جدید
            user = User.objects.create(**validated_data)

            # تولید توکن برای کاربر جدید
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'کاربر با موفقیت ثبت نام شد',
                'username': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListCreateView(APIView):
    """
    نمایش لیست رویدادها و ایجاد رویداد جدید
    """
    permission_classes = [IsAuthenticated]

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
            event = serializer.save()
            event.participants.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    """
    نمایش، به‌روزرسانی و حذف یک رویداد خاص
    """
    permission_classes = [IsAuthenticated]

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
        if event.participants.count() != 1:
            return Response(
                {'detail': 'شما نمیتوانید رویداد را حذف کنید، چون رویداد دارای شرکت کننده میباشد.'},
                status=status.HTTP_403_FORBIDDEN
            )



        event.delete()
        return Response({'detail': 'رویداد با موفقیت حذف شد.'},
                        status=status.HTTP_204_NO_CONTENT)


class JoinEventView(APIView):
    """
    عضویت در رویداد
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        اضافه کردن کاربر به شرکت‌کنندگان رویداد
        """
        event = get_object_or_404(Event, pk=pk)
        if request.user in event.participants.all():
            return Response(
                {'detail': 'شما در این رویداد عضو هستید.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        event.participants.add(request.user)
        serializer = EventSerializer(event)
        return Response(serializer.data)



class LeaveEventView(APIView):
    """
    خروج از رویداد
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        حذف کاربر از شرکت‌کنندگان رویداد
        """
        event = get_object_or_404(Event, pk=pk)

        if request.user == event.creator:
            return Response(
                {'detail': 'شما سازنده این رویداد هستید، نمیتوانید رویداد را ترک کنید، در صورت نیاز میتوانید رویداد را حذف کنید.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # بررسی آیا کاربر در رویداد حضور دارد
        if request.user not in event.participants.all():
            return Response(
                {'detail': 'شما در این رویداد عضو نیستید.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # حذف کاربر از شرکت‌کنندگان
        event.participants.remove(request.user)

        # بازگرداندن اطلاعات رویداد به‌روزرسانی شده
        serializer = EventSerializer(event)
        return Response(serializer.data)


class MyEventsView(APIView):
    """
    نمایش رویدادهای ساخته شده و رویدادهای عضو شده توسط کاربر
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        دریافت رویدادهای ساخته شده و عضو شده
        """

        joined_events = Event.objects.filter(participants=request.user)

        return Response({
            'joined_events': EventSerializer(joined_events, many=True).data
        })


