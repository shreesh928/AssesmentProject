from django.urls import path, include
from .views import ClientGetRetrive, ProjectGetRetrive, delete_data, put_client_data, delete_project, ResgisterView, LoginView, UserView

urlpatterns = [
    path("client/",ClientGetRetrive.as_view(),name="client-detail"),
    path("client/<int:pk>/",ClientGetRetrive.as_view(),name="client-byid"),
    path("client/delete/<int:pk>/",delete_data,name="deleteclientdata"),
    path("client/post/",put_client_data,name="client-post"),
    path("project/",ProjectGetRetrive.as_view(),name="project-list"),
    path("project/<int:pk>/",ProjectGetRetrive.as_view(),name="project-patch"),
    path("project/delete/<int:pk>/",delete_project,name="project-delete"),
    path('register/', ResgisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("users/",UserView.as_view(), name="users"),
    path("users/<int:pk>/",UserView.as_view(), name="users"),

]