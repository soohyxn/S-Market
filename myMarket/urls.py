"""myMarket URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # 관리자 페이지
    path('foods/', include('foods.urls')), # 상품 관련 페이지
    path('', include('single_pages.urls')), # 상품 관련 외의 페이지
    path('accounts/', include('allauth.urls')), # 회원 로그인/회원가입
    path('markdownx/', include('markdownx.urls')), # 마크다운
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 이미지 경로