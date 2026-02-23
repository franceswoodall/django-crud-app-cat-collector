from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'), #path for home is an empty string
    #home is a kwarg - it's optional, it's just helpful for us to use to reference 
    path('about/', views.about, name='about'),
    path('cats/', views.CatList.as_view(), name='cat-index'),
    path('cats/<int:pk>/', views.CatDetail.as_view(), name='cat-detail'),
    path('cats/create/', views.CatCreate.as_view(), name='cat-create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat-update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat-delete'),
]
