from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

from .models import Recipe
from .serializers import RecipeSerializer, DistributorRequestSerializer
from .services.brevo import BrevoEmailError, send_distributor_request_notification

logger = logging.getLogger(__name__)

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
        '8. Solicitud de distribuidor (POST)': '/api/distributors/',
    }
    return Response(api_urls)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def distributor_request_create(request):
    """
    Recibe el formulario de distribuidor desde el frontend y guarda la solicitud.
    """
    serializer = DistributorRequestSerializer(data=request.data)
    if serializer.is_valid():
        distributor_request = serializer.save()

        email_sent = False
        email_error = None
        try:
            send_distributor_request_notification(distributor_request)
            email_sent = True
        except BrevoEmailError as exc:
            email_error = str(exc)
            logger.error('No se pudo enviar el correo de distribuidor: %s', exc)

        response_data = serializer.data
        response_data['email_sent'] = email_sent
        if email_error:
            response_data['email_error'] = email_error

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
