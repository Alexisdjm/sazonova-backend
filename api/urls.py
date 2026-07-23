from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, ProductViewSet, api_overview, distributor_request_create

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('distributors/', distributor_request_create, name='distributor-request-create'),
    path('', include(router.urls)),
]
