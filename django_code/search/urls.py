from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.Course_Num_ListView.as_view(), name='Course_Num_changelist'),
    # path('add/', views.Course_Num_CreateView.as_view(), name='Course_Num_add'),
    # path('<int:pk>/', views.Course_Num_UpdateView.as_view(), name='Course_Num_change'),
]
