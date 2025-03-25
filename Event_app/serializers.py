from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):

    creator = UserSimpleSerializer(read_only=True)
    participants = UserSimpleSerializer(many=True, read_only=True)
    current_participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'creator','participants', 'capacity',  'created_at', 'current_participants_count']
        read_only_fields = ['created_at', 'current_participants_count']

    def create(self, validated_data):
        """
        محدود کردن تعداد رویدادها در زمان ساخت
        """
        user = self.context['request'].user
        if Event.objects.filter(creator=user).count() >= 10:
            raise serializers.ValidationError('شما مجاز به ساخت بیش از 10 رویداد نیستید.')

        validated_data['creator'] = user
        return super().create(validated_data)

    def get_current_participants_count(self, obj):
        """
        محاسبه تعداد شرکت‌کنندگان فعلی رویداد
        """
        return obj.participants.count()


class JoinEventSerializer(serializers.Serializer):
    """
    سریالایزر برای عضویت در رویداد
    """

    def create(self, validated_data):
        """
        افزودن کاربر به شرکت‌کنندگان رویداد
        """
        user = self.context['request'].user
        event = self.context.get('event')

        event.add_participant(user)
        return event