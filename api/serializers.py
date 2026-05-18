from rest_framework import serializers
from .models import Recipe, Ingredient, PreparationStep

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity']

class PreparationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationStep
        fields = ['id', 'step_number', 'instruction']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = PreparationStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug', 'meal_type', 'is_featured', 'created_at', 'updated_at', 'ingredients', 'steps']
