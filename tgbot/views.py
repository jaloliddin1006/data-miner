from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from tgbot.models import User, Text, Voice, VoiceCheck, Feedback, Channel
from django.db import models
from django.db.models import F, ExpressionWrapper, Value
from django.db.models.functions import Cast

def home(request: HttpRequest):
    group_1_students = (User.objects.filter(academic_group='1')
                       .annotate(
                            voice_count=models.Count('voices', distinct=True),
                            checks_count=models.Count('checks', distinct=True),
                            voice_duration=models.Sum('voices__length', distinct=True, default=0),
                            hours=ExpressionWrapper(F('voice_duration') / 3600, output_field=models.IntegerField()),
                            minutes=ExpressionWrapper((F('voice_duration') % 3600) / 60, output_field=models.IntegerField()
                                                      ),
                            )
                 
        )   
    group_1_results = group_1_students.aggregate(
                    students = models.Count('id', distinct=True),
                    voice_count = models.Count('voices', distinct=True),
                    checks_count = models.Count('checks', distinct=True),
                    voice_duration = models.Sum('voices__length', distinct=True)
                )
    
    group_1_results['formatted_voice_duration'] = f"{group_1_results['voice_duration'] // 3600:02}:{(group_1_results['voice_duration'] % 3600) // 60:02}"

    print(group_1_results)

    group_2_students = (User.objects.filter(academic_group='2')
                       .annotate(
                            voice_count=models.Count('voices', distinct=True),
                            checks_count=models.Count('checks', distinct=True),
                            voice_duration=models.Sum('voices__length', distinct=True),
                            hours=ExpressionWrapper(F('voice_duration') / 3600, output_field=models.IntegerField()),
                            minutes=ExpressionWrapper((F('voice_duration') % 3600) / 60, output_field=models.IntegerField()
                                                      ),
                            )
                
        )   
    group_2_results = group_2_students.aggregate(
                    students = models.Count('id', distinct=True),
                    voice_count = models.Count('voices', distinct=True),
                    checks_count = models.Count('checks', distinct=True),
                    voice_duration = models.Sum('voices__length', distinct=True)
                )
    
    # group_2_results['formatted_voice_duration'] = f"{group_2_results['voice_duration'] // 3600:02}:{(group_2_results['voice_duration'] % 3600) // 60:02}"

    context = {
        'group_1_students': group_1_students,
        'group_1_results': group_1_results,
        'group_2_students': group_2_students,
        'group_2_results': group_2_results,
    }
    return render(request, 'index.html', context)
