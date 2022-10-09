from django.urls import path
from . import views

urlpatterns = [
    path('ticket/all/', views.TicketList.as_view()),
    path('ticket/my_ticket/', views.StaffTicketList.as_view()),
    path('ticket/<int:pk>', views.TicketDetail.as_view()),
    path('ticket/create/', views.TicketCreator.as_view()),
    path('ticket/update/<int:pk>', views.TicketUpdator.as_view()),
    path('user/register/', views.RegisterView.as_view()),
    path('user/all/', views.UserView.as_view()),
    path('user/change_password/<int:pk>', views.ChangePasswordView.as_view()),
    path('user/<int:pk>', views.RetrieveUpdateUserView.as_view()),
    
]