from django.contrib import admin
from .models import Bug

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'project', 'description', 'query_type', 'created_at', 'status', 'date_fixed')
