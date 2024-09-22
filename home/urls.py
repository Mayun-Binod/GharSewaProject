from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('error/', views.error, name='error'),
    
    # Searching
    path('search/', views.search, name='search'),
    path('search_user/', views.searchProvider, name='search_user'),
    
    path('login/', views.handleLogin, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    

    path('user_register/', views.user_register, name='user_register'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('logout/', views.handleLogout, name='logout'),
    
    # Services
    path('services/', views.services, name='services'),
    path('services/<int:myid>/', views.serviceView, name='serviceView'),
    path('add_service/', views.addService, name='add_service'),
    
   
    # User Profile
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile/', views.profile, name='profile'),
    
    # Edit Profile
    path('editprofile/', views.edit_profile, name='editprofile'),
    
    # Admin Panel
    path('admin_home/', views.admin_home, name= 'admin_home'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('all_services/', views.allServices, name= 'allservices'),
    path('all_users/', views.allUsers, name= 'allusers'),
    path('all_customers/', views.allCustomers, name= 'allcustomers'),
    
    path('feedback/', views.feedback, name='feedback'),
    path('deleteFeedback/<int:myid>', views.deleteFeedback, name= 'deleteFeedback'),


    path('admin_booking/', views.adminBooking, name= 'admin_booking'),
    path('city_list/', views.adminCity, name= 'city_list'),
    path('delete_city/<int:pid>', views.deleteCity, name= 'delete_city'),

    
    path('admin_profile/', views.adminProfile, name= 'admin_profile'),
    path('edit_admin/<int:pid>', views.editAdmin, name= 'edit_admin'),
    path('changeadminpass/<int:pid>', views.changeAdminpass, name= 'changeadminpass'),

    # CRUD function
    path('editservices/<int:pid>', views.editServices, name= 'editservices'),
    path('deleteService/<int:myid>', views.deleteService, name='deleteService'),
    path('deleteCustomer/<int:myid>', views.deleteCustomer, name='deleteCustomer'),
    path('deleteUser/<int:myid>', views.deleteUser, name='deleteUser'),
    
    path('acceptUser/<int:myid>', views.acceptUser, name='acceptUser'),

    # Book Services
    path('booking/<int:pid>', views.customerBooking, name='booking'),
    path('booking_details/', views.bookingDetails, name='booking_details'),
    path('user_booking/', views.userBooking, name='user_booking'),
    path('notification/', views.notification, name='notification'),
    
    path('accept_confirmation/<int:pid>', views.accept_confirmation, name='accept_confirmation'),
    
    # Customer Cancellation
    path('cancel_booking/<int:pid>', views.cancelBooking, name= 'cancel_booking'),
    
    # Service Provider Cancellations
    path('spcancel_booking/<int:pid>', views.spcancelBooking, name= 'spcancel_booking'),
    
    path('booking_status/<int:pid>', views.bookingStatus, name= 'booking_status'),

    
]