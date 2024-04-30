from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator



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
    show_on_site = models.BooleanField("Show on site", default=True)
    bpm = models.IntegerField('BPM', default=90)
    key = models.CharField('Key', unique=False, null=False, max_length=16)
    mood = models.ForeignKey(Moods, on_delete=models.CASCADE)
    duration = models.CharField('Duration', max_length=16, null=False)
    type_beat = models.CharField('Type Beat', unique=False, max_length=32, default="Unique", null=False)
    tags = models.ManyToManyField(Tags, blank=True)
    description = models.CharField('Track description', max_length=256, blank=False, unique=False, default='Produced by @Cloudymotion4life. Only high quality beats for you💎')
    priority = models.IntegerField('Track priority', blank=False, unique=False, default=0)
    cool_cover = models.BooleanField('Cool cover in store', default=False)
    mp3 = models.FileField('Mp3 File', upload_to='uploads/')
    waw_link = models.URLField('Link to wav license files', blank=True)
    unl_and_exc_link = models.URLField('Link to unlimited and exclusive license files', blank=True)

    
    
    def __str__(self) -> str:
        return self.track_name
    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'


class Banners(models.Model):
    banner = models.ImageField("Banner", upload_to='uploads/')
    link = models.URLField('HREF', default='http://cloudymotion.com/store')
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class NoSignContracts(models.Model):
    wav_license = models.FileField('Wav license contract', upload_to='uploads/contracts/temp/')
    unlimited_license = models.FileField('Unlimited license contract', upload_to='uploads/contracts/temp/')
    exclusive_license = models.FileField('Exclusive license contract', upload_to='uploads/contracts/temp/')
    class Meta:
        verbose_name = 'No Sign Contract'
        verbose_name_plural = 'No Sign Contracts'

class SignContracts(models.Model):
    wav_license = models.FileField('Wav license contract', upload_to='uploads/contracts/temp/')
    unlimited_license = models.FileField('Unlimited license contract', upload_to='uploads/contracts/temp/')
    exclusive_license = models.FileField('Exclusive license contract', upload_to='uploads/contracts/temp/')
    class Meta:
        verbose_name = 'Sign Contract'
        verbose_name_plural = 'Sign Contracts'


User = get_user_model()
class PurchasedTrack(models.Model):
    LICENSE_CHOICES = [
        ('wav', 'Wav license'),
        ('unlimited', 'Unlimited license'),
        ('exclusive', 'Exclusive license'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_tracks')
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    track_license = models.CharField(max_length=20, choices=LICENSE_CHOICES, null=True, blank=True)
    contract = models.FileField(upload_to='uploads/contracts/', null=True, blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Purchased Track'
        verbose_name_plural = 'Purchased Tracks'

    def __str__(self):
        return f'{self.user.username} - {self.track.track_name}'
    

class ErrorReport(models.Model):
    email = models.EmailField('Email')
    subject = models.CharField('Subject', max_length=256)
    description = models.TextField('Description', max_length=4096)
    photo = models.ImageField(upload_to='uploads/errors/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class Promocode(models.Model):
    data_create = models.DateTimeField(auto_now_add=True)
    promo_name = models.CharField('Name', max_length=32, unique=True)
    promo_count = models.IntegerField('Amount of use', blank=True, null=True)
    promo_discount = models.IntegerField(
        'Percentage discount (%)',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    class Meta:
        verbose_name = 'Promocode'
        verbose_name_plural = 'Promocodes'

    def __str__(self):
        return self.promo_name
    

class AppliedPromocodes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE)
    data_create = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'APPLIEDPromocode'
        verbose_name_plural = 'APPLIEDPromocodes'

    def __str__(self):
        return f'{self.user} : {self.promocode}'