from django.contrib import admin

# Register your models here.
from .models import Job


class JobAdmin(admin.ModelAdmin):
    # fields = ['finish_date', 'name']

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date Information', {'fields': ['finish_date']})
    ]

    list_display = ('name', 'finish_date', 'was_finished_recently')

    list_filter = ['finish_date']

    search_fields = ['name']


admin.site.register(Job, JobAdmin)
