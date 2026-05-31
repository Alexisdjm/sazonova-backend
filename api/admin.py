from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep, DistributorRequest

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


@admin.register(DistributorRequest)
class DistributorRequestAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'company', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('contact_name', 'company', 'email', 'phone')
    readonly_fields = ('created_at',)
