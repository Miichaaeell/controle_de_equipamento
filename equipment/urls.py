from django.urls import path
from .views import CreateEquipmentView, CreateBrandView, CreateModelEquipmentView, CreateCategoryView, CreateStatusEquipmentView, ListEquipmentView, ListBrandView,  ListModelEquipmentView, ListCategoryView, ListStatusEquipmentView, UpdateBrandView, UpdateEquipmentView, UpdateModelEquipmentView, UpdateCategoryView, UpdateStatusEquipmentView


urlpatterns = [
    # Views Equipments
    path('create_equipment/', CreateEquipmentView.as_view(),
         name='create_equipment'),
    path('list_equipment/', ListEquipmentView.as_view(), name='list_equipment'),
    path('update_equipment/<pk>', UpdateEquipmentView.as_view(),
         name='update_equipment'),

    # Views Brand
    path('create_brand/', CreateBrandView.as_view(), name='create_brand'),
    path('list_brand/', ListBrandView.as_view(), name='list_brand'),
    path('update_brand/<pk>', UpdateBrandView.as_view(), name='update_brand'),

    # Views Model
    path('create_model_equipment/', CreateModelEquipmentView.as_view(),
         name='create_modelequipment'),
    path('list_model_equipment/', ListModelEquipmentView.as_view(),
         name='list_modelequipment'),
    path('update_model_equipment/<pk>', UpdateModelEquipmentView.as_view(),
         name='update_modelequipment'),

    # Views Category
    path('create_category/', CreateCategoryView.as_view(), name='create_category'),
    path('list_category/', ListCategoryView.as_view(), name='list_category'),
    path('update_category/<pk>', UpdateCategoryView.as_view(),
         name='update_category'),

    # Views Status
    path('create_status/', CreateStatusEquipmentView.as_view(),
         name='create_statusequipment'),
    path('list_status/', ListStatusEquipmentView.as_view(),
         name='list_statusequipment'),
    path('update_status/<pk>', UpdateStatusEquipmentView.as_view(),
         name='update_statusequipment'),
]
