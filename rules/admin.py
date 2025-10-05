from django.contrib import admin
from .models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'rule_type', 'is_active', 'created_at']
    list_filter = ['rule_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
