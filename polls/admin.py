from django.contrib import admin

from polls.models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['question', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
    list_per_page = 42

    Poll.was_published_recently.admin_order_field = 'pub_date'
    Poll.was_published_recently.boolean = True
    Poll.was_published_recently.short_description = 'Published recently?'


admin.site.register(Poll, PollAdmin)