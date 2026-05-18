from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET'])
def api_overview(request):
    """
    Esta es una guía de todas las URLs disponibles en la API de Recetas.
    """
    api_urls = {
        'Guía de la API (esta página)': '/api/',
        '1. Todas las recetas': '/api/recipes/all/',
        '2. Recetas individuales (por su nombre)': '/api/recipes/<slug>/',
        '3. Recetas Populares/Destacadas': '/api/recipes/featured/',
        '4. Solo Desayunos': '/api/recipes/desayunos/',
        '5. Solo Almuerzos': '/api/recipes/almuerzos/',
        '6. Solo Cenas': '/api/recipes/cenas/',
        '7. Solo Entradas o Refrigerios': '/api/recipes/entradas/',
    }
    return Response(api_urls)

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('-created_at')
        meal_type = self.request.query_params.get('meal_type', None)
        if meal_type is not None:
            queryset = queryset.filter(meal_type=meal_type.upper())
        return queryset

    @action(detail=False, methods=['get'])
    def all(self, request):
        recipes = self.get_queryset()
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_recipes = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_recipes, many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        
        # Diccionario para mapear las URLs que pediste con los códigos de base de datos
        categories = {
            'desayunos': 'DES',
            'almuerzos': 'ALM',
            'cenas': 'CEN',
            'entradas': 'ROE'
        }
        
        # Si el slug que consultan coincide con uno de nuestros tipos de comida, filtramos y devolvemos la lista
        if slug in categories:
            recipes = Recipe.objects.filter(meal_type=categories[slug]).order_by('-created_at')
            serializer = self.get_serializer(recipes, many=True)
            return Response(serializer.data)
            
        # Si no es ninguna de esas palabras, asumimos que es una receta individual y dejamos que DRF haga lo suyo
        return super().retrieve(request, *args, **kwargs)
