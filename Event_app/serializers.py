from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        # چک کردن تطابق رمزهای عبور
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "رمزهای عبور مطابقت ندارند"})
        return attrs

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_members'):
            representation.pop('participants', None)
        return representation


