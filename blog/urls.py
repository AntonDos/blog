"""blog URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from blog.views import register_view
from posts.views import index_view
from shop.views import ProductsView, product_details_view, PurchaseView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", index_view, name="index_view"),
    path("register/", register_view, name="register_view"),
    path("", ProductsView.as_view(), name="products_view"),
    path(
        "product/<int:product_id>/", product_details_view, name="product_details_view"
    ),
    path("purchases/", PurchaseView.as_view(), name="purchases_view"),
    path("api/", include("api.urls", namespace="api")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)