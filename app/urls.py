from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns =[
    path('',views.api_Overview,name='api_Overview'),
    path('all/',views.get_all,name='get_all'),
    path('create/',views.createItem,name="Create_Item"),
    path('update/<int:pk>',views.updateItem,name="Update_item"),
    path('pdf/',views.pdf_gen, name="pdfGen"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]