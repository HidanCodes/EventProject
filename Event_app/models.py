from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    participants = models.ManyToManyField(User, related_name='participants',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        محدود کردن تعداد رویدادهای ساخته شده توسط کاربر
        """
        if Event.objects.filter(creator=self.creator).count() >= 10:
            raise ValidationError('شما مجاز به ساخت بیش از 10 رویداد نیستید.')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name