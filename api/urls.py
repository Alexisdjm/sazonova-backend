from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, api_overview

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('', include(router.urls)),
]
