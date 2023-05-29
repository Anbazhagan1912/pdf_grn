from django.urls import path
from . import views

urlpatterns =[
    path('',views.api_Overview,name='api_Overview'),
    path('all/',views.get_all,name='get_all'),
    path('create/',views.createItem,name="Create_Item"),
    path('update/<int:pk>',views.updateItem,name="Update_item"),
    path('delet/<int:pk>',)
]