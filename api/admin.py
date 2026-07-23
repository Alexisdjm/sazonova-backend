from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep, DistributorRequest, Product

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
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [IngredientInline, PreparationStepInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'meal_type', 'preparation_time', 'is_featured'),
        }),
        ('Imágenes', {
            'fields': ('card_image', 'detailed_image'),
        }),
    )


@admin.register(DistributorRequest)
class DistributorRequestAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'company', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('contact_name', 'company', 'email', 'phone')
    readonly_fields = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'quantity', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'quantity'),
        }),
        ('Ingredientes y detalles', {
            'fields': ('ingredients', 'product_details'),
            'description': 'En ingredientes puedes usar una línea por ítem o separarlos por comas.',
        }),
        ('Información nutricional', {
            'fields': ('nutritional_info',),
        }),
    )
