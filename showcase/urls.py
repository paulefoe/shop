from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^basket/$', views.basket, name='basket'),
    url(r'^$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.ProductsInCategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),

]

