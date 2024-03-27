from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    artist_name = models.CharField('Artist name', max_length=64, blank=False, default="")


class Prices(models.Model):
    wav_license = models.IntegerField('Wav License $', default=30)
    unlimited_license = models.IntegerField('Unlimited License $', default=100)
    exclusive_license = models.IntegerField('Exclusive License $', default=300)
    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'


class Moods(models.Model):
    mood = models.CharField('New mood', unique=True, max_length=32, null=False)
    def __str__(self) -> str:
        return self.mood
    class Meta:
        verbose_name = 'Mood'
        verbose_name_plural = 'Moods'


class Tags(models.Model):
    tag = models.CharField('Tag', unique=True, max_length=32)
    def __str__(self):
        return self.tag
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Tracks(models.Model):
    track_name = models.CharField('Track Name', unique=True, null=False, max_length=64)
    cover_art = models.ImageField("Cover Art", upload_to='uploads/')
    bpm = models.IntegerField('BPM', default=90)
    key = models.CharField('Key', unique=False, null=False, max_length=16)
    mood = models.ForeignKey(Moods, on_delete=models.CASCADE)
    duration = models.CharField('Duration', max_length=16, null=False)
    type_beat = models.CharField('Type Beat', unique=False, max_length=32, default="Unique", null=False)
    mp3 = models.FileField('Mp3 File', upload_to='uploads/')
    tags = models.ManyToManyField(Tags, blank=True)
    priority = models.IntegerField('Track priority', blank=False, unique=False, default=0)
    def __str__(self) -> str:
        return self.track_name
    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'


class Banners(models.Model):
    banner = models.ImageField("Banner", upload_to='uploads/')
    link = models.URLField('HREF', default='http://127.0.0.1:8000/store')
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
