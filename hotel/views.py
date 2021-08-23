from datetime import date, datetime, timedelta
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from hotel.forms import *
from hotel.models import *
from .utils import *
from hotel.parser.hotelParser import parse_hotels
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class RoomsView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        room_list = Room.objects.all()
        types = RoomCategory.objects.all()
        date_now = date.today()
        orders = Order.objects.filter(active=True)
        for order in orders:
            date_check = order.departure_date - date_now
            if order.departure_date > date_now:
                order.room.status = "Свободен"
                order.room.save()
            if order.entry_date <= date_now:
                print(2222222)
                order.active = True
                order.save()
                order.room.status = 'Занят'
                order.room.save()
            if date_check.days <= 0:
                order.active = False
                order.room.status = "Свободен"
                print(11111)
                order.room.save()
                order.save()

        return render(request, 'admin/rooms/rooms_for_admin.html',
                      context={'count': len(new_bookings), 'room_list': room_list, 'type_list': types,
                               'date_now': date_now, 'orders': orders})


class RoomsCategorySort(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk):
        new_bookings = Booking.objects.filter(status='Новый')
        room_list = Room.objects.filter(type=pk)
        types = RoomCategory.objects.all()
        return render(request, 'admin/rooms/rooms_for_admin.html',
                      context={'count': len(new_bookings), 'room_list': room_list, 'type_list': types})


class AddRoomView(PermissionRequiredMixin, View):
    permission_required = 'hotel.add_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        form = AddRoomForm()
        return render(request, 'admin/rooms/add_room.html', context={'count': len(new_bookings), 'form': form})

    def post(self, request):
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.number = form.cleaned_data['number']
            room.type = form.cleaned_data['type']
            if room.number <= 0:
                messages.add_message(request, messages.INFO, "Номер не может быть меньше 1")
                return HttpResponseRedirect('/admin-rooms/add/')
            Room.objects.create(number=room.number, type=room.type)
            messages.add_message(request, messages.INFO, "Номер успешно добавлен")
            return HttpResponseRedirect('/admin-rooms/')
        messages.add_message(request, messages.INFO, "Такой номер уже есть!")
        return HttpResponseRedirect('/admin-rooms/add/')


class DeleteRoom(PermissionRequiredMixin, View):
    permission_required = 'hotel.delete_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, number):
        room = get_object_or_404(Room, pk=number)
        if room.status == 'Занят':
            messages.add_message(request, messages.INFO, "Нельзя удалять занятый номер")
            return HttpResponseRedirect('/admin-rooms/')
        room.delete()
        messages.add_message(request, messages.INFO, "Номер успешно удален")
        return HttpResponseRedirect('/admin-rooms/')


class CategoryView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        types = RoomCategory.objects.all()
        return render(request, 'admin/categories/category_view.html',
                      context={'count': len(new_bookings), 'type_list': types})


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = 'hotel.add_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        form = CategoryForm()
        return render(request, 'admin/categories/add_category.html', context={'count': len(new_bookings), 'form': form})

    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = get_category_fields(form)
            categories = RoomCategory.objects.all()
            for car in categories:
                if category.category_name == car.category_name:
                    messages.add_message(request, messages.INFO, "Категория с таким названием уже есть")
                    return HttpResponseRedirect('/admin-categories/add/')
            if category.persons <= 0:
                messages.add_message(request, messages.INFO, "Количество гостей должно быть больше 0")
                return HttpResponseRedirect('/admin-categories/add/')
            if category.price_per_day <= 0:
                messages.add_message(request, messages.INFO, "Стоимость должна быть больше 0")
                return HttpResponseRedirect('/admin-categories/add/')
            RoomCategory.objects.create(category_name=category.category_name,
                                        price_per_day=category.price_per_day,
                                        persons=category.persons,
                                        image=category.image,
                                        desc=category.desc)
            messages.add_message(request, messages.INFO, "Категория успешно добавлена")
            return HttpResponseRedirect('/admin-categories/')
        return HttpResponseRedirect('/admin-categories/add/')


class UpdateCategoryView(PermissionRequiredMixin, View):
    permission_required = 'hotel.change_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request, category_name):
        new_bookings = Booking.objects.filter(status='Новый')
        category = get_object_or_404(RoomCategory, category_name=category_name)
        form = CategoryForm(initial={
            'category_name': category.category_name,
            'price_per_day': category.price_per_day,
            'persons': category.persons,
            'image': category.image,
            'desc': category.desc,
        })
        return render(request, 'admin/categories/change_category.html',
                      context={'count': len(new_bookings), 'form': form, 'category': category})

    def post(self, request, category_name):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = get_category_fields(form)
            RoomCategory.objects.filter(
                category_name=category_name).update(
                category_name=category.category_name,
                price_per_day=category.price_per_day,
                persons=category.persons,
                image=category.image,
                desc=category.desc)
            messages.add_message(request, messages.INFO, "Категория успешно изменена")
            return HttpResponseRedirect('/admin-categories/')
        messages.add_message(request, messages.INFO, "Категория успешно изменена")
        redirect = '/admin-categories/change_view/{}'.format(category_name)
        return HttpResponseRedirect(redirect)


class DeleteCategory(PermissionRequiredMixin, View):
    permission_required = 'hotel.delete_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request, category_name):
        category = get_object_or_404(RoomCategory, category_name=category_name)
        category.delete()
        messages.add_message(request, messages.INFO, "Категория успешно удалена")
        return HttpResponseRedirect('/admin-categories/')


class ClientsView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        orders = Order.objects.all().order_by('-pk')
        return render(request, 'admin/visitors/visitors.html',
                      context={'count': len(new_bookings), 'orders': orders})


class SettlingView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, number, date_in, date_out):
        new_bookings = Booking.objects.filter(status='Новый')
        form = ClientForm()
        room = get_object_or_404(Room, pk=number)
        return render(request, 'admin/rooms/add_client_to_room.html',
                      context={'count': len(new_bookings), 'form': form, 'room': room, 'date_in': date_in,
                               'date_out': date_out})

    def post(self, request, number, date_in, date_out):
        new_bookings = Booking.objects.filter(status='Новый')
        form = ClientForm(request.POST)
        room = get_object_or_404(Room, pk=number)

        if form.is_valid():
            new_client = get_visitor_fields(form)
            print(len(str(new_client.passport)))
            if len(str(new_client.passport)) < 9 or len(str(new_client.passport)) > 10:
                messages.add_message(request, messages.INFO, "Паспорт должен содержать 9 или 10 цифр!")
                return render(request, 'admin/rooms/add_client_to_room.html',
                              context={'count': len(new_bookings), 'form': form, 'room': room, 'date_in': date_in,
                                       'date_out': date_out})
            new_client = Client.objects.create(
                first_name=new_client.first_name,
                patronymic=new_client.patronymic,
                last_name=new_client.last_name,
                passport=new_client.passport,
                country=new_client.country,
                gender=new_client.gender,
                birthday=new_client.birthday
            )

            new_client.save()

            redirect_url = reverse('make_order_view', args=[room.number, new_client.pk, date_in, date_out])
            return HttpResponseRedirect(redirect_url)
            # return render(request, 'rooms/order.html', context={'room':room, 'client': new_client, 'form': form})
        return render(request, 'admin/rooms/add_client_to_room.html',
                      context={'count': len(new_bookings), 'form': form, 'room': room, 'date_in': date_in,
                               'date_out': date_out})


class MakeOrderView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, client_id, number, date_in, date_out):
        new_bookings = Booking.objects.filter(status='Новый')
        client = get_object_or_404(Client, pk=client_id)
        room = get_object_or_404(Room, pk=number)
        date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
        date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
        days = date_out - date_in
        price = days.days * room.type.price_per_day
        bookings = Booking.objects.all()
        for booking in bookings:
            if booking.room == room and date_in == booking.entry_date and date_out == booking.departure_date:
                booking.status = 'Заселено'
                booking.save()
        return render(request, 'admin/rooms/order.html',
                      context={'count': len(new_bookings), 'room': room, 'client': client, 'date_in': date_in,
                               'date_out': date_out, 'price': price})

    def post(self, request, client_id, number, date_in, date_out):
        room = get_object_or_404(Room, pk=number)
        client = get_object_or_404(Client, pk=client_id)
        date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
        date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
        days = date_out - date_in
        price = days.days * room.type.price_per_day
        persons = request.POST['persons']
        order = Order.objects.create(entry_date=date_in, departure_date=date_out, room=room, client=client, price=price, persons=persons)
        if date_in > date.today():
            order.active = False
            order.save()
        else:
            room.status = "Занят"
            room.save()
        return HttpResponseRedirect('/admin-rooms/')


class UpdateVisitorView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, client_id):
        new_bookings = Booking.objects.filter(status='Новый')
        client = get_object_or_404(Client, client_id=client_id)
        form = ClientForm(initial={
            'first_name': client.first_name,
            'patronymic': client.patronymic,
            'last_name': client.last_name,
            'country': client.country,
            'passport': client.passport,
            'birthday': client.birthday,
            'gender': client.gender,
        })
        return render(request, 'admin/visitors/change_visitor.html',
                      context={'count': len(new_bookings), 'form': form, 'client': client})

    def post(self, request, client_id):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = get_visitor_fields(form)
            if len(str(client.passport)) < 9 or len(str(client.passport)) > 10:
                messages.add_message(request, messages.INFO, "Паспорт должен содержать 9 или 10 цифр!")
                return HttpResponseRedirect('/clients/update_client/{}'.format(client_id))
            Client.objects.filter(client_id=client_id).update(
                first_name=client.first_name,
                patronymic=client.patronymic,
                last_name=client.last_name,
                passport=client.passport,
                country=client.country,
                gender=client.gender,
                birthday=client.birthday
            )
            messages.add_message(request, messages.INFO, "Данные о посетителе успешно изменены")
            return HttpResponseRedirect('/clients/')
        return HttpResponseRedirect('/clients/update_client/{}'.format(client_id))


class PricesView(PermissionRequiredMixin, View):
    permission_required = 'hotel.delete_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        hotels = parse_hotels()

        return render(request, 'admin/other_prices.html', context={'count': len(new_bookings), 'hotels': hotels})


class HistoryView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        orders = Order.objects.filter(active=False, entry_date__lte=date.today()).order_by('-pk')
        return render(request, 'admin/orders_history.html', context={'count': len(new_bookings), 'orders': orders, 'today': str(date.today())})

    def post(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        date_in = request.POST['date_in']
        date_out = request.POST['date_out']
        date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
        date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
        orders = Order.objects.filter(active=False)
        if date_out <= date_in:
            messages.add_message(request, messages.INFO, "Даты выбраны некоректно!")
            return render(request, 'admin/orders_history.html',
                          context={'count': len(new_bookings), 'orders': orders, 'today': str(date.today())})
        for order in orders:
            if (date_in >= order.entry_date and date_in <= order.departure_date) or (
                    date_out >= order.entry_date and date_out <= order.departure_date) or (
                    order.entry_date >= date_in and order.departure_date <= date_out):
                print("1")
                continue
            else:
                print("2")
                orders = orders.exclude(pk=order.pk)
        return render(request, 'admin/orders_history.html',
                      context={'count': len(new_bookings), 'orders': orders, 'today': str(date.today())})


class FindByDate(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        min_departure = date.today() + timedelta(days=1)
        return render(request, 'admin/rooms/view_settling_by_date.html',
                      context={'count': len(new_bookings), 'today': str(date.today()),
                               'min_departure': str(min_departure)})

    def post(self, request):
        date_in = request.POST['date_in']
        date_out = request.POST['date_out']
        room_list = Room.objects.all()
        if date_out <= date_in:
            messages.add_message(request, messages.INFO, "Даты выбраны некоректно!")
            new_bookings = Booking.objects.filter(status='Новый')
            min_departure = date.today() + timedelta(days=1)
            return render(request, 'admin/rooms/view_settling_by_date.html',
                          context={'count': len(new_bookings), 'today': str(date.today()),
                                   'min_departure': str(min_departure)})
        room_list, date_in, date_out = get_free_rooms(date_in, date_out, room_list)
        new_bookings = Booking.objects.filter(status='Новый')
        types = RoomCategory.objects.all()
        return render(request, 'admin/rooms/view_free_rooms.html',
                      context={'count': len(new_bookings), 'room_list': room_list, 'date_in': date_in,
                               'date_out': date_out, 'types': types})


class SortFreeRooms(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk, date_in, date_out):
        new_bookings = Booking.objects.filter(status='Новый')
        if pk == 10000:
            room_list = Room.objects.all()
        else:
            room_list = Room.objects.filter(type=pk)
        types = RoomCategory.objects.all()
        room_list, date_in, date_out = get_free_rooms(date_in, date_out, room_list)
        return render(request, 'admin/rooms/view_free_rooms.html',
                      context={'count': len(new_bookings), 'room_list': room_list, 'types': types, 'date_in': date_in,
                               'date_out': date_out})


class MainPageView(View):

    def get(self, request):
        types = RoomCategory.objects.all()
        return render(request, 'client/main.html', context={'types': types})


class BookingView(LoginRequiredMixin, View):

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        min_departure = date.today() + timedelta(days=1)
        return render(request, 'client/booking_date_check.html', context={'today': str(date.today()), 'min_departure': str(min_departure)})

    def post(self, request):
        date_in = request.POST['date_in']
        date_out = request.POST['date_out']
        if date_out <= date_in:
            min_departure = date.today() + timedelta(days=1)
            messages.add_message(request, messages.INFO, "Даты выбраны некоректно!")
            return render(request, 'client/booking_date_check.html', context={'today': str(date.today()), 'min_departure': str(min_departure)})
        room_list = Room.objects.all()
        categories = RoomCategory.objects.all()
        room_list, date_in, date_out = get_free_rooms(date_in, date_out, room_list)
        for category in categories:
            cn = []
            for room in room_list:
                if room.type.pk == category.pk:
                    cn.append(room.number)
            category.free_rooms = len(cn)
            category.save()
        return render(request, 'client/view_free.html',
                      context={'types': categories, 'date_in': date_in, 'date_out': date_out, 'today': str(date.today())})


class FinalBookingView(LoginRequiredMixin, View):

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk, date_in, date_out):
        category = get_object_or_404(RoomCategory, pk=pk)
        date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
        date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
        days = date_out - date_in
        final_price = days.days * category.price_per_day
        user = request.user
        client_user = ClientUser.objects.filter(user=user).first()

        if client_user.first_name == None:
            client_user.first_name = ''
            client_user.save()
        if client_user.last_name == None:
            client_user.last_name = ''
            client_user.save()
        if client_user.patronymic == None:
            client_user.patronymic = ''
            client_user.save()
        if client_user.phone == None:
            client_user.phone = ''
            client_user.save()

        form = VisitorForm(initial={
            'first_name': client_user.first_name,
            'last_name': client_user.last_name,
            'patronymic': client_user.patronymic,
            'phone': client_user.phone,
        })
        return render(request, 'client/booking.html',
                      context={'final_price': final_price, 'type': category, 'form': form, 'date_in': date_in,
                               'date_out': date_out})

    def post(self, request, pk, date_in, date_out):
        category = get_object_or_404(RoomCategory, pk=pk)
        rooms = Room.objects.filter(type=category)
        room_list, date_in, date_out = get_free_rooms(date_in, date_out, rooms)
        room = room_list.first()
        days = date_out - date_in
        final_price = days.days * category.price_per_day
        user = request.user
        client_user = ClientUser.objects.filter(user=user).first()
        form = VisitorForm(request.POST or None)
        if form.is_valid():
            client_user.first_name = form.cleaned_data['first_name']
            client_user.last_name = form.cleaned_data['last_name']
            client_user.patronymic = form.cleaned_data['patronymic']
            client_user.phone = form.cleaned_data['phone']
            client_user.save()
            persons = int(request.POST.get('persons'))
            Booking.objects.create(entry_date=date_in, departure_date=date_out, price=final_price, user=client_user,
                                   room=room, persons=persons)
            return HttpResponseRedirect('/confirm/')
        return render(request, 'client/booking.html',
                      context={'final_price': final_price, 'type': category, 'form': form, 'date_in': date_in,
                               'date_out': date_out})


class LoginView(View):

    def get(self, request):
        form = LoginForm(request.POST or None)
        return render(request, 'client/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.user.is_superuser or request.user.is_staff:
                    return HttpResponseRedirect('/admin-rooms/')
                return HttpResponseRedirect('/')

        return render(request, 'client/login.html', context={'form': form})


class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'client/register.html', context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            ClientUser.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                patronymic=form.cleaned_data['patronymic']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'client/register.html', context={'form': form})


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('main_page')


class ConfirmPage(View):
    def get(self, request):
        return render(request, 'client/confirm.html')


class BookingsView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        bookings = Booking.objects.all().order_by('-pk')
        return render(request, 'admin/bookings.html',
                      context={'count': len(new_bookings), 'bookings': bookings, 'today': date.today()})

    def post(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        date_in = request.POST['date_in']
        date_out = request.POST['date_out']
        date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
        date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
        bookings = Booking.objects.filter(entry_date=date_in, departure_date=date_out)
        if date_out <= date_in:
            bookings = Booking.objects.all().order_by('-pk')
            messages.add_message(request, messages.INFO, "Даты выбраны некоректно!")

            return render(request, 'admin/bookings.html', context={'count': len(new_bookings), 'bookings': bookings, 'today': date.today()})
        return render(request, 'admin/bookings.html',
                      context={'count': len(new_bookings), 'bookings': bookings, 'today': str(date.today())})


class DeleteBookingView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete()
        new_bookings = Booking.objects.filter(status='Новый')
        bookings = Booking.objects.all()
        return render(request, 'admin/bookings.html',
                      context={'count': len(new_bookings), 'bookings': bookings, 'today': date.today()})


class ConfirmBookingView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = 'Подтвержден'
        booking.save()
        new_bookings = Booking.objects.filter(status='Новый')
        bookings = Booking.objects.all().order_by('-pk')
        return render(request, 'admin/bookings.html',
                      context={'count': len(new_bookings), 'bookings': bookings, 'today': date.today()})


class BookingSettlingView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        date_in = booking.entry_date
        date_out = booking.departure_date
        new_bookings = Booking.objects.filter(status='Новый')
        form = ClientForm(initial={
            'first_name': booking.user.first_name,
            'last_name': booking.user.last_name,
            'patronymic': booking.user.patronymic,
        })
        return render(request, 'admin/rooms/add_client_to_room.html',
                      context={'form': form, 'count': len(new_bookings), 'room': booking.room, 'date_in': date_in,
                               'date_out': date_out})


class OccupiedRoomView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        types = RoomCategory.objects.all()
        orders = Order.objects.filter(active=True)
        return render(request, 'admin/rooms/occupied_rooms.html',
                      context={'orders': orders, 'count': len(new_bookings), 'type_list': types})


class EvictView(PermissionRequiredMixin, View):
    permission_required = 'hotel.view_room'

    def get_login_url(self):
        return '/login/'

    def get(self, request, number):
        room = get_object_or_404(Room, pk=number)
        order = Order.objects.filter(active=True, room=room).first()
        order.active = False
        order.departure_date = date.today()
        room.status = 'Свободен'
        room.save()
        order.save()
        return HttpResponseRedirect('/admin-rooms/')


class StaffView(PermissionRequiredMixin, View):

    permission_required = 'hotel.delete_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        new_bookings = Booking.objects.filter(status='Новый')
        staff = Employee.objects.all()
        return render(request, 'admin/staff.html', context={'count': len(new_bookings), 'staff': staff})


class StaffDelete(PermissionRequiredMixin, View):

    permission_required = 'hotel.delete_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return HttpResponseRedirect('/staff/')


class StaffAdd(PermissionRequiredMixin, View):
    permission_required = 'hotel.delete_roomcategory'

    def get_login_url(self):
        return '/login/'

    def get(self, request):
        form = StaffForm()
        new_bookings = Booking.objects.filter(status='Новый')
        return render(request, 'admin/staff_add.html',
                      context={'count': len(new_bookings), 'form': form})

    def post(self, request):
        form = StaffForm(request.POST or None)
        new_bookings = Booking.objects.filter(status='Новый')
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            if new_user.username != "":
                new_user.set_password(form.cleaned_data['password'])
                new_user.is_staff = True
                new_user.is_active = True

                new_user.save()

                Employee.objects.create(
                    user=new_user,
                    phone=form.cleaned_data['phone'],
                    salary=form.cleaned_data['salary'],
                    passport=form.cleaned_data['passport'],
                    position=form.cleaned_data['position'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    patronymic=form.cleaned_data['patronymic']
                )
                user = User.objects.filter(username=new_user.username).first()
                permission = Permission.objects.get(name='Can view Комната')
                print(1)
                user.user_permissions.add(permission)
                user.save()
            else:
                Employee.objects.create(
                    phone=form.cleaned_data['phone'],
                    salary=form.cleaned_data['salary'],
                    passport=form.cleaned_data['passport'],
                    position=form.cleaned_data['position'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    patronymic=form.cleaned_data['patronymic']
                )
                user = User.objects.filter(username="Manager3")
            return HttpResponseRedirect('/staff/')
        return render(request, 'admin/staff_add.html', context={'count': len(new_bookings), 'form': form})








