from django.db import models


GENDER_CHOISES = (
    ('erkak', '🤵 Erkak'),
    ('ayol', '👩‍💼 Ayol')
)

REGION_CHOISES = (
    ('001', 'Toshkent shahri'),
    ('002', 'Andijon'),
    ('003', 'Farg`ona'),
    ('004', 'Namangan'),
    ('005', 'Toshkent'),
    ('006', 'Sirdaryo'),
    ('007', 'Jizzax'),
    ('008', 'Samarqand'),
    ('009', 'Qashqadaryo'),
    ('010', 'Surxondaryo'),
    ('011', 'Navoiy'),
    ('012', 'Buxoro'),
    ('013', 'Xorazm'),
    ('014', 'Qoraqalpog`iston'),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(BaseModel):
    telegram_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=10, choices=REGION_CHOISES, default='001')
    sex = models.CharField(max_length=10, choices=GENDER_CHOISES, default='erkak')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "telegram_users"


class BotAdmin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super(BotAdmin, self).save(*args, **kwargs)
        
    class Meta:
        db_table = "bot_admins"


class Text(BaseModel):
    text_id = models.CharField(max_length=255, unique=True)
    text = models.TextField()

    def __str__(self):
        return str(self.text)

    class Meta:
        db_table = "texts"


class Voice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="voices")
    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name="voices")
    voice = models.FileField(upload_to="voices/")
    voice_id = models.CharField(max_length=255, unique=True, null=True)
    length = models.IntegerField(null=True) # in seconds | 1 min = 60 sec
    size = models.IntegerField(null=True) # in bytes | 1 MB = 1024 KB = 1024 * 1024 bytes

    def __str__(self):
        return str(self.voice.url)
    
    @property
    def like(self):
        return self.checks.filter(is_correct=True).count()
    
    @property
    def dislike(self):
        return self.checks.filter(is_correct=False).count()

    class Meta:
        db_table = "voices"


class TextPassed(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passed")
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name="passed")

    def __str__(self):
        return str(self.text.text)

    class Meta:
        db_table = "text_passed"
        constraints = [
            models.UniqueConstraint(fields=['user', 'text'], name='unique_user_passed_text')
        ]

class VoiceCheck(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="checks")
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name="checks")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_correct)

    class Meta:
        db_table = "voice_checks"
        constraints = [
            models.UniqueConstraint(fields=['user', 'voice'], name='unique_user_check_voice')
        ]

    
class Feedback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback")
    feedback = models.TextField()

    def __str__(self):
        return f"{self.user.username}"
    

class Channel(BaseModel):
    channel_id = models.BigIntegerField()
    name = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.channel_id}"
    
    class Meta:
        db_table = "channels"
        