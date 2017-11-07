from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='product_detail'),
]
