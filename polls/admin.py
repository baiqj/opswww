from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'votes', 'poll')

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'pub_date')
    inlines = [ChoiceInline]
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
