from datetime import datetime

from hotel.models import Order, Booking


def get_category_fields(form):
    category = form.save(commit=False)
    category.category_name = form.cleaned_data['category_name']
    category.price_per_day = form.cleaned_data['price_per_day']
    category.persons = form.cleaned_data['persons']
    category.image = form.cleaned_data['image']
    category.desc = form.cleaned_data['desc']
    return category


def get_visitor_fields(form):
    new_client = form.save(commit=False)
    new_client.first_name = form.cleaned_data['first_name']
    new_client.patronymic = form.cleaned_data['patronymic']
    new_client.last_name = form.cleaned_data['last_name']
    new_client.passport = form.cleaned_data['passport']
    new_client.country = form.cleaned_data['country']
    new_client.gender = form.cleaned_data['gender']
    new_client.birthday = form.cleaned_data['birthday']
    return new_client


def check_free(entity, room_list, date_in, date_out):
    if (date_in >= entity.entry_date and date_in <= entity.departure_date) or (
            date_out >= entity.entry_date and date_out <= entity.departure_date) or (
            entity.entry_date >= date_in and entity.departure_date <= date_out):
        for room in room_list:
            print("1")
            if room.number == entity.room.number:
                print("2")
                room_list = room_list.exclude(number=room.number)
    return room_list


def get_free_rooms(date_in, date_out, room_list):
    date_in = datetime.strptime(date_in, "%Y-%m-%d").date()
    date_out = datetime.strptime(date_out, "%Y-%m-%d").date()
    orders = Order.objects.filter(active=True)
    bookings = Booking.objects.all()

    for order in orders:
        room_list = check_free(order, room_list, date_in, date_out)
    for booking in bookings:
        room_list = check_free(booking, room_list, date_in, date_out)
    return room_list, date_in, date_out



