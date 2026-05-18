from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'meal_type', 'is_featured', 'created_at')
    list_filter = ('meal_type', 'is_featured')
    search_fields = ('name', 'ingredients')
    prepopulated_fields = {'slug': ('name',)}
