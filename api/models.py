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

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Ingrediente (ej: Tomates)")
    quantity = models.CharField(max_length=100, verbose_name="Cantidad (ej: 2 piezas o 500g)")

    def __str__(self):
        return f"{self.quantity} de {self.name}"

class PreparationStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField(verbose_name="Número de paso")
    instruction = models.TextField(verbose_name="Instrucción")

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Paso {self.step_number}"
