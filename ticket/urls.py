from django.urls import path
from . import views

urlpatterns = [
    path('ticket/', views.TicketView.as_view()),
    path('ticket/<int:pk>', views.TicketDetailView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('category/', views.TicketCategoryView.as_view()),
    path('category/<int:pk>', views.TicketCategoryDetailView.as_view()),
    path('user/client/', views.ClientView.as_view()),
    path('user/client/<int:pk>', views.ClientDetailView.as_view()),
    path('user/staff/', views.StaffView.as_view()),
    path('user/staff/<int:pk>', views.StaffDetailView.as_view()),
    
]