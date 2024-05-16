from django.db import models


class User(models.Model):
    telegram_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "telegram_users"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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

    def __str__(self):
        return str(self.text.text)

    class Meta:
        db_table = "voices"


class TextPassed(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="passed")
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
        return self.is_correct

    class Meta:
        db_table = "voice_checks"
        constraints = [
            models.UniqueConstraint(fields=['user', 'voice'], name='unique_user_check_voice')
        ]

    
