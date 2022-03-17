"""drfDemo URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='API接口文档',
        default_version='v1',
        description='接口文档平台',
        # terms_of_service='http://api.xxx.com',
        contact=openapi.Contact(email='hybpjx@qq.com'),
        license=openapi.License(name='License')
    ),
    public=True,  # 允许所有人访问
    # 权限类
    permission_classes=(permissions.IsAuthenticated,),  # 允许所有人访问
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("students.urls")),
    path("api/", include("stuapi.urls")),
    path("seri/", include("sers.urls")),
    path("req/", include("req.urls")),
    path("demo/", include("demo.urls")),
    path("school/", include("school.urls")),
    path("opt/", include("opt.urls")),

    path('docs/', include_docs_urls(title='说明文档')),

    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),

]
