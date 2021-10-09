"""bullboard URL Configuration

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
from django.urls import path


# python modules are annoying
from backend.views import login_view, another_view

# This is for URL pathing. If you requested page /, it'll send you to / (which is the login page)
# If we did /blah, it wouldn't work cause we haven't added a path for that.
urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view),
    path('test/', another_view),
    path('admin/', admin.site.urls),
]
