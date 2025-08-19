from django.urls import path
from .views import CreateEquipmentView, CreateBrandView, CreateModelEquipmentView, CreateCategoryView, CreateStatusView


urlpatterns = [
    # Views Equipments
    path('create_equipment/', CreateEquipmentView.as_view(),
         name='create_equipment'),
    # Views Brand
    path('create_brand/', CreateBrandView.as_view(), name='create_brand'),
    # Views Model
    path('create_model_equipment/', CreateModelEquipmentView.as_view(),
         name='create_model_equipment'),
    # Views Category
    path('create_category/', CreateCategoryView.as_view(), name='create_category'),
    # Views Status
    path('create_status/', CreateStatusView.as_view(), name='create_status')
]
