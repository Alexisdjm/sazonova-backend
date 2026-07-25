from rest_framework import serializers

from .models import Recipe, Ingredient, PreparationStep, DistributorRequest, Product, ProductImage


def _absolute_image_url(obj, field_name, serializer):
    image_field = getattr(obj, field_name, None)
    if not image_field:
        return None
    image_url = image_field.url
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(image_url)
    return image_url


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'text']


class PreparationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationStep
        fields = ['id', 'fase_name', 'show_name', 'step_number', 'instruction']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = PreparationStepSerializer(many=True, read_only=True)
    card_image = serializers.SerializerMethodField()
    detailed_image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'meal_type',
            'preparation_time',
            'card_image',
            'detailed_image',
            'is_featured',
            'created_at',
            'updated_at',
            'ingredients',
            'steps',
        ]

    def get_card_image(self, obj):
        return _absolute_image_url(obj, 'card_image', self)

    def get_detailed_image(self, obj):
        return _absolute_image_url(obj, 'detailed_image', self)


class DistributorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributorRequest
        fields = [
            'id',
            'company',
            'contact_name',
            'email',
            'phone',
            'company_address',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'order']

    def get_url(self, obj):
        return _absolute_image_url(obj, 'image', self)


class ProductSerializer(serializers.ModelSerializer):
    nutritional_info = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'quantity',
            'ingredients',
            'nutritional_info',
            'product_details',
            'images',
            'primary_image',
            'created_at',
            'updated_at',
        ]

    def get_nutritional_info(self, obj):
        return _absolute_image_url(obj, 'nutritional_info', self)

    def get_ingredients(self, obj):
        return obj.ingredient_list()

    def get_primary_image(self, obj):
        images = list(obj.images.all())
        if not images or not images[0].image:
            return None
        return _absolute_image_url(images[0], 'image', self)
