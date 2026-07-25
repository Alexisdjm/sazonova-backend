from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Recipe, Ingredient, PreparationStep, DistributorRequest, Product, ProductImage


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class PreparationStepInline(admin.TabularInline):
    model = PreparationStep
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = ProductImage.MAX_IMAGES_PER_PRODUCT
    ordering = ('order', 'id')
    fields = ('image', 'order')


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
    list_display = ('name', 'slug', 'quantity', 'image_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
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

    @admin.display(description='Imágenes')
    def image_count(self, obj):
        return obj.images.count()

    def save_formset(self, request, form, formset, change):
        if formset.model is ProductImage:
            total = 0
            for form_item in formset.forms:
                if not hasattr(form_item, 'cleaned_data') or not form_item.cleaned_data:
                    continue
                if form_item.cleaned_data.get('DELETE'):
                    continue
                if form_item.cleaned_data.get('image') or form_item.instance.pk:
                    total += 1
            if total > ProductImage.MAX_IMAGES_PER_PRODUCT:
                raise ValidationError(
                    f'Solo se permiten hasta {ProductImage.MAX_IMAGES_PER_PRODUCT} imágenes por producto.'
                )
        super().save_formset(request, form, formset, change)
