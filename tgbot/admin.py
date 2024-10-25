from django.contrib import admin
from django.urls import reverse
from tgbot.models import User as BotUser, Text, Voice, TextPassed, VoiceCheck, BotAdmin, Feedback, Channel
from django.utils.html import format_html

import os
from tgbot.resources import TextResource, VoiceResource
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin


@admin.register(BotAdmin)
class BotAdminsAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'user', 'is_active', 'created_at', 'account')
    list_editable = ('is_active',)
    list_display_links = ('id', 'telegram_id')

    def telegram_id(self, obj):
        return str(obj.user.telegram_id)
    
    def account(self, obj):
        return format_html(f'<button><a class="button" href="https://t.me/{obj.user.username}">View Telegram</a></bitton>'  )
    account.short_description = 'Account'
    account.allow_tags = True


@admin.register(BotUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "full_name", 'location','sex', "username", 'created_at', 'is_active', 'academic_group'  )
    fields = ("full_name", "username", "telegram_id",'location','sex', 'academic_group')
    search_fields = ("full_name", "username", "telegram_id")
    list_display_links = ('id', 'telegram_id')
    list_filter = ('academic_group',)
    list_per_page = 50


@admin.register(Text)
class TextAdmin(ImportExportModelAdmin):
    resource_classes = [TextResource]
    list_display = ("id", "text_id", "text", )
    fields = ("text_id", "text", )
    search_fields = ("text_id", "text", )
    list_per_page = 50


@admin.register(Voice)
class VoiceAdmin(ExportActionModelAdmin):
    resource_classes = [VoiceResource]

    list_display = ("id", "user", "text", "audio_tag", 'Length', 'Size', 'like', 'dislike',)
    search_fields = ("user__username", "text__text",  )
    list_display_links = ('id', 'user')
    # list_filter = ('user__username', 'text__text')
    list_per_page = 50
    
    def audio_tag(self, obj):
        if obj.voice:
            return format_html('<audio controls src="{}"></audio>', obj.voice.url)
        else:
            return 'No audio file'
    audio_tag.short_description = 'Audio'
    
    def Length(self, obj):
        return f"{obj.length} sek." if obj.length else "0 sek."
    
    def Size(self, obj):
        return f"{round(obj.size / 1024 )} kb" if obj.size else "0 mb"

    def like(self, obj):
        return obj.checks.filter(is_correct=True).count()
    like.short_description = '👍'

    def dislike(self, obj):
        return obj.checks.filter(is_correct=False).count()
    dislike.short_description = '👎'


    def delete_queryset(self, request, queryset):
        for obj in queryset:
            # print(os.path.exists(obj.voice.path))
            os.remove(obj.voice.path)
        queryset.delete()

    def delete_model(self, request, obj):
        os.remove(obj.voice.path)
        obj.delete()


@admin.register(TextPassed)
class VoicePassedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text", )
    fields = ("user", "text", )
 
    search_fields = ("user__username", "text__text", )

    # list_filter = ('user__username', )
    list_per_page = 50
    
    
@admin.register(VoiceCheck)
class VoiceCheckAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "voice", 'is_correct')
    search_fields = ("user__username", "voice__text", )
    # list_filter = ('user__username', 'voice__text', 'is_correct')
    readonly_fields = ('audio_tag',)
    list_per_page = 50    
   
    def audio_tag(self, obj):
        if obj.voice:
            return format_html('<audio controls src="{}"></audio>', obj.voice.voice.url)
        else:
            return 'No audio file'
        
    audio_tag.short_description = 'Audio'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user', 'feedback1', 'created_at')
    list_display_links = ('id', 'username')

    def username(self, obj):
        return obj.user.username
    
    def feedback1(self, obj):
        return f"{obj.feedback}" if len(obj.feedback) < 80 else f"{str(obj.feedback)[:80]}..."



@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_id', 'name', 'username')
