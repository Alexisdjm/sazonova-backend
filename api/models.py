from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    MEAL_CHOICES = [
        ('DES', 'Desayuno'),
        ('ALM', 'Almuerzo'),
        ('CEN', 'Cena'),
        ('ROE', 'Refrigerios o Entradas'),
    ]

    card_image = models.ImageField(
        upload_to='recipes/cards/',
        null=True,
        blank=True,
        verbose_name='Imagen para la tarjeta',
    )
    detailed_image = models.ImageField(
        upload_to='recipes/details/',
        null=True,
        blank=True,
        verbose_name='Imagen para la página de detalle',
    )
    name = models.CharField(max_length=200, verbose_name='Nombre')
    calories = models.IntegerField(verbose_name='Calorías', default=300)
    portions = models.IntegerField(verbose_name='Porciones', default=1)
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    meal_type = models.CharField(max_length=3, choices=MEAL_CHOICES, verbose_name='Tipo de comida')
    preparation_time = models.CharField(
        max_length=100,
        verbose_name='Tiempo de preparación (ej: 30 minutos)',
        blank=True,
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacada',
        help_text='Marcar para que aparezca en recetas populares.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.get_meal_type_display()})'


class DistributorRequest(models.Model):
    company = models.CharField(max_length=200, blank=True)
    contact_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    company_address = models.TextField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.contact_name} — {self.company or self.email}'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL Slug')
    description = models.TextField(verbose_name='Descripción')
    quantity = models.CharField(
        max_length=100,
        verbose_name='Cantidad',
        help_text='Ej: 250 g, 1 unidad, 500 ml',
    )
    ingredients = models.TextField(
        verbose_name='Ingredientes',
        help_text='Un ingrediente por línea, o separados por coma.',
    )
    nutritional_info = models.ImageField(
        upload_to='products/nutrition/',
        null=True,
        blank=True,
        verbose_name='Información nutricional (imagen)',
    )
    product_details = models.TextField(
        blank=True,
        verbose_name='Detalles del producto',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).replace('-', '_')
        super().save(*args, **kwargs)

    def ingredient_list(self):
        """Parsea el textarea en una lista (líneas o comas)."""
        raw = (self.ingredients or '').replace('\r\n', '\n').replace('\r', '\n')
        items = []
        for line in raw.split('\n'):
            for part in line.split(','):
                item = part.strip()
                if item:
                    items.append(item)
        return items

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    MAX_IMAGES_PER_PRODUCT = 6

    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE,
        verbose_name='Producto',
    )
    image = models.ImageField(
        upload_to='products/gallery/',
        verbose_name='Imagen',
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Menor número = aparece primero. La primera es la principal.',
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Imagen del producto'
        verbose_name_plural = 'Imágenes del producto'

    def __str__(self):
        return f'{self.product.name} — imagen {self.order}'


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    text = models.CharField(
        max_length=300,
        verbose_name='Ingrediente (ej: 2 dientes de ajo picados)',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text


class PreparationStep(models.Model):
    fase_name = models.CharField(
        max_length=100,
        verbose_name='Fase (ej: Preparación, Cocción, Montaje)',
        blank=True,
    )
    show_name = models.BooleanField(
        default=False,
        verbose_name='Mostrar nombre de la fase en la receta?',
    )
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField(verbose_name='Número de paso')
    instruction = models.TextField(verbose_name='Instrucción')

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f'Paso {self.step_number}'
