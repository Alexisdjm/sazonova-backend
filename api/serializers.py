from rest_framework import serializers
from .models import Recipe, Ingredient, PreparationStep, DistributorRequest

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity']

class PreparationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationStep
        fields = ['id', 'fase_name', 'show_name', 'step_number', 'instruction']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = PreparationStepSerializer(many=True, read_only=True)
    recipe_image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug', 'meal_type', 'preparation_time', 'recipe_image', 'is_featured', 'created_at', 'updated_at', 'ingredients', 'steps']

    def get_recipe_image(self, obj):
        if not obj.recipe_image:
            return None
        image_url = obj.recipe_image.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(image_url)
        return image_url


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
