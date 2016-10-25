"""smartpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from products.views import QuantityListView, ProductListView, ProductCreateVeiw, ConsCreateView, ConsUpdateView
from restaurants.views import RestarauntListView, RestarauntDetailView, OrderCreate, OrderListView, OrderDetailView, \
    CheckoutProductCreate, CheckoutProductListView, CheckoutProductDetailView, ReportCreate, ReportListView, \
    ReportDetailView, ResultView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^consumables/create/$', ConsCreateView.as_view(), name='cons_create'),
    url(r'^consumables/update/$', ConsUpdateView.as_view(), name='cons_update'),
    url(r'^rests/$', RestarauntListView.as_view(), name='list'),
    url(r'^rests/(?P<slug>[\w-]+)/$', RestarauntDetailView.as_view(), name='rest'),
    url(r'^rests/(?P<slug>[\w-]+)/products/$', ProductListView.as_view(), name='products'),
    url(r'^rests/(?P<slug>[\w-]+)/products/add/$', ProductListView.as_view(), name='product_add'),
    url(r'^rests/(?P<slug>[\w-]+)/products/create/$', ProductCreateVeiw.as_view(), name='products_create'),
    url(r'^rests/(?P<slug>[\w-]+)/products/(?P<pk>\d+)/$', QuantityListView.as_view(), name='quants'),
    url(r'^rests/(?P<slug>[\w-]+)/orders/$', OrderListView.as_view(), name='orders'),
    url(r'^rests/(?P<slug>[\w-]+)/orders/create/$', OrderCreate.as_view(), name='order_create'),
    url(r'^rests/(?P<slug>[\w-]+)/orders/(?P<date>\d{4}-\d{2}-\d{2})/', OrderDetailView.as_view(), name='order_detail'),
    url(r'^rests/(?P<slug>[\w-]+)/reports/$', ReportListView.as_view(), name='reports'),
    url(r'^rests/(?P<slug>[\w-]+)/reports/create/$', ReportCreate.as_view(), name='report_create'),
    url(r'^rests/(?P<slug>[\w-]+)/reports/(?P<date>\d{4}-\d{2}-\d{2})/result/$', ResultView.as_view(),
        name='result'),
    url(r'^rests/(?P<slug>[\w-]+)/reports/(?P<date>\d{4}-\d{2}-\d{2})/$', ReportDetailView.as_view(),
        name='report_detail'),
    url(r'^rests/(?P<slug>[\w-]+)/checkout/$', CheckoutProductListView.as_view(), name='checkout'),
    url(r'^rests/(?P<slug>[\w-]+)/checkout/create/$', CheckoutProductCreate.as_view(), name='checkout_create'),
    url(r'^rests/(?P<slug>[\w-]+)/checkout/(?P<date>\d{4}-\d{2}-\d{2})/', CheckoutProductDetailView.as_view(),
        name='checkout_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
