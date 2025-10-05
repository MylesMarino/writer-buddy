from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('share/<str:token>/', views.document_share_view, name='document_share'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/autosave/', views.document_autosave, name='document_autosave'),
    path('<int:pk>/export/', views.document_export, name='document_export'),
    path('<int:pk>/check-rules/', views.document_check_rules, name='document_check_rules'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('<int:pk>/generate-share/', views.document_generate_share, name='document_generate_share'),
]
