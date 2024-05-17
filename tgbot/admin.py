from django.contrib import admin
from tgbot.models import User as TelegramUser, Text, Voice, TextPassed, VoiceCheck
from django.utils.html import format_html
import os

@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "telegram_id", )
    fields = ("full_name", "username", "telegram_id", )
    search_fields = ("full_name", "username", "telegram_id", )


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "text_id", "text", )
    fields = ("text_id", "text", )
    search_fields = ("text_id", "text", )


@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text", "audio_tag",  )
    fields = ("user", "text",  )
    search_fields = ("user", "text",  )
    list_display_links = ('id', 'user')
    
    def audio_tag(self, obj):
        if obj.voice:
            return format_html('<audio controls src="{}"></audio>', obj.voice.url)
        else:
            return 'No audio file'
    audio_tag.short_description = 'Audio'

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            print(os.path.exists(obj.voice.path))
            os.remove(obj.voice.path)
        queryset.delete()

    def delete_model(self, request, obj):
        os.remove(obj.voice.path)
        obj.delete()


@admin.register(TextPassed)
class VoicePassedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text", )
    fields = ("user", "text", )
    search_fields = ("user", "text", )


@admin.register(VoiceCheck)
class VoiceCheckAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "voice", 'is_correct')
    fields = ("user", "voice", )
    search_fields = ("user", "voice", )