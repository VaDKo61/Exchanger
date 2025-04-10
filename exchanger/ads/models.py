from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Ad(models.Model):
    condition_choose = [
        ('N', 'Новый'),
        ('U', 'Б/у')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image_url = models.URLField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=1, choices=condition_choose)
    created_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f'{self.id}'


class ExchangeProposal(models.Model):
    status_choose = [
        ('W', 'Ожидает'),
        ('A', 'Принята'),
        ('R', 'Отклонена'),
    ]
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, null=False, related_name='ad_send')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, null=False, related_name='ad_rec')
    comment = models.CharField(max_length=250)
    status = models.CharField(max_length=1, choices=status_choose, default='W')
    created_at = models.DateTimeField(auto_now_add=timezone.now)
