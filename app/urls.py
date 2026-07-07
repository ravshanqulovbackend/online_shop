from django.urls import path, include
from app.views import home ,product_detail,add_comment, order_view


urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/products/', home, name='products_of_category'),
    path('detail/<int:pk>/', product_detail, name='detail'),
    path('add-comment/<int:pk>/', add_comment, name='add_comment'), 
    path('add-order-view/<int:pk>/', order_view, name='order_view')

]   