from django.urls import path
from .views import *
urlpatterns = [
    path('admin-rooms/', RoomsView.as_view(), name='all_rooms_admin'),
    path('admin-rooms/<int:pk>', RoomsCategorySort.as_view(), name='type_rooms_admin'),
    path('occupied_rooms/', OccupiedRoomView.as_view(), name='occupied_rooms'),
    path('evict/<int:number>', EvictView.as_view(), name='evict'),

    path('staff/', StaffView.as_view(), name='staff_view'),
    path('staff-delete/<int:pk>', StaffDelete.as_view(), name='staff_delete'),
    path('staff/add', StaffAdd.as_view(), name='staff_add'),


    path('admin-rooms/add/', AddRoomView.as_view(), name='add_room_view'),
    path('admin-rooms-delete/<int:number>', DeleteRoom.as_view(), name='delete_room'),
    path('settling/', FindByDate.as_view(), name='find_by_date'),
    path('settling/<int:pk>/in=<str:date_in>/out=<str:date_out>', SortFreeRooms.as_view(), name='free_sort_rooms'),

    path('make_order_view/<int:number>/<int:client_id>/in=<str:date_in>/out=<str:date_out>/', MakeOrderView.as_view(), name='make_order_view'),
    path('add_client_to_room/<int:number>/in=<str:date_in>/out=<str:date_out>/', SettlingView.as_view(), name='settling_view_add_client'),

    path('admin-categories/add/', AddCategoryView.as_view(), name='add_category_view'),
    path('admin-categories/', CategoryView.as_view(), name='all_categories'),
    path('admin-categories/delete/<str:category_name>', DeleteCategory.as_view(), name='delete_category'),
    path('admin-categories/change_view/<str:category_name>', UpdateCategoryView.as_view(), name='update_category_view'),

    path('admin_bookings/', BookingsView.as_view(), name='bookings'),
    path('admin_bookings_cancel/<int:pk>', DeleteBookingView.as_view(), name='delete_booking'),
    path('admin_bookings_confirm/<int:pk>', ConfirmBookingView.as_view(), name='confirm_booking'),
    path('admin_booking_settling/booking=<int:pk>/', BookingSettlingView.as_view(), name='settling_booking'),

    path('clients/', ClientsView.as_view(), name='clients_view'),

    path('clients/update_client/<int:client_id>/', UpdateVisitorView.as_view(), name='update_client_view'),

    path('view_prices/', PricesView.as_view(), name='view_prices'),
    path('view_history/', HistoryView.as_view(), name='view_history'),

    path('', MainPageView.as_view(), name="main_page"),
    path('booking_dates/', BookingView.as_view(), name="booking_dates"),
    path('booking_dates/<int:pk>/in=<str:date_in>/out=<str:date_out>', FinalBookingView.as_view(), name="booking"),
    path('login/', LoginView.as_view(), name="login"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', MyProjectLogout.as_view(), name="logout"),
    path('confirm/', ConfirmPage.as_view(), name='cofrim')
]
