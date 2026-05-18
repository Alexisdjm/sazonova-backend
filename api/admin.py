from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class PreparationStepInline(admin.TabularInline):
    model = PreparationStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'meal_type', 'is_featured', 'created_at')
    list_filter = ('meal_type', 'is_featured')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [IngredientInline, PreparationStepInline]
