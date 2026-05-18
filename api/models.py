from django.db import models
from django.utils.text import slugify

class Recipe(models.Model):
    MEAL_CHOICES = [
        ('DES', 'Desayuno'),
        ('ALM', 'Almuerzo'),
        ('CEN', 'Cena'),
        ('ROE', 'Refrigerios o Entradas'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL Slug")
    ingredients = models.TextField(verbose_name="Ingredientes", help_text="Ej: 2 tomates, 1 cebolla...")
    preparation = models.TextField(verbose_name="Preparación", help_text="Pasos a seguir para cocinar.")
    meal_type = models.CharField(max_length=3, choices=MEAL_CHOICES, verbose_name="Tipo de comida")
    is_featured = models.BooleanField(default=False, verbose_name="Destacada", help_text="Marcar para que aparezca en recetas populares.")
    
    # Optional but recommended fields:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # slugify convierte a lowercase y cambia caracteres raros. Replace asegura que sean guiones bajos como pediste
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_meal_type_display()})"
