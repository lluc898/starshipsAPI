from django.urls import path, include
from rest_framework import routers
from api.views import StarshipView, StarshipSearchView, StarshipViewSet

router = routers.DefaultRouter()
router.register(r'naves', StarshipViewSet)

urlpatterns = [
    path('starships/', StarshipView.as_view(), name='starships'),
    path('starships/<int:pk>/', StarshipView.as_view(), name='starships'),
    path('starships/search/<str:name>/', StarshipSearchView.as_view(), name='starships-search'),
    path('', include(router.urls)),
]

