import json

# from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm
from .models import Booking, Menu



# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {'menu': menu_data}
    return render(request, 'menu.html', main_data)

def display_menu_items(request, pk =None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, 'menu_item.html',{'menu_item': menu_item})


# API helper: parse JSON request body safely for Insomnia/API clients.
def _parse_json_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


# API endpoint: list all menu items (GET) or create a new menu item (POST).
@csrf_exempt
def api_menu(request):
    if request.method == 'GET':
        items = list(Menu.objects.values('id', 'name', 'price', 'menu_item_description'))
        return JsonResponse(items, safe=False, status=200)

    if request.method == 'POST':
        payload = _parse_json_body(request)
        if not payload:
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

        name = payload.get('name')
        price = payload.get('price')
        description = payload.get('menu_item_description', '')

        if not name or price is None:
            return JsonResponse({'error': 'Fields "name" and "price" are required.'}, status=400)

        item = Menu.objects.create(name=name, price=price, menu_item_description=description)
        return JsonResponse(
            {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'menu_item_description': item.menu_item_description,
            },
            status=201,
        )

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


# API endpoint: get, update, or delete one menu item by id.
@csrf_exempt
def api_menu_detail(request, pk):
    try:
        item = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return JsonResponse({'error': 'Menu item not found.'}, status=404)

    if request.method == 'GET':
        return JsonResponse(
            {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'menu_item_description': item.menu_item_description,
            },
            status=200,
        )

    if request.method in ['PUT', 'PATCH']:
        payload = _parse_json_body(request)
        if not payload:
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

        # API update supports partial fields for both PUT and PATCH requests.
        item.name = payload.get('name', item.name)
        item.price = payload.get('price', item.price)
        item.menu_item_description = payload.get('menu_item_description', item.menu_item_description)
        item.save()

        return JsonResponse(
            {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'menu_item_description': item.menu_item_description,
            },
            status=200,
        )

    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'message': 'Menu item deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


# API endpoint: list all bookings (GET) or create a new booking (POST).
@csrf_exempt
def api_bookings(request):
    if request.method == 'GET':
        bookings = list(Booking.objects.values('id', 'first_name', 'last_name', 'guest_number', 'comment'))
        return JsonResponse(bookings, safe=False, status=200)

    if request.method == 'POST':
        payload = _parse_json_body(request)
        if not payload:
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

        first_name = payload.get('first_name')
        last_name = payload.get('last_name')
        guest_number = payload.get('guest_number')
        comment = payload.get('comment', '')

        if not first_name or not last_name or guest_number is None:
            return JsonResponse(
                {'error': 'Fields "first_name", "last_name", and "guest_number" are required.'},
                status=400,
            )

        booking = Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            guest_number=guest_number,
            comment=comment,
        )

        return JsonResponse(
            {
                'id': booking.id,
                'first_name': booking.first_name,
                'last_name': booking.last_name,
                'guest_number': booking.guest_number,
                'comment': booking.comment,
            },
            status=201,
        )

    return JsonResponse({'error': 'Method not allowed.'}, status=405)


# API endpoint: get, update, or delete one booking by id.
@csrf_exempt
def api_booking_detail(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)

    if request.method == 'GET':
        return JsonResponse(
            {
                'id': booking.id,
                'first_name': booking.first_name,
                'last_name': booking.last_name,
                'guest_number': booking.guest_number,
                'comment': booking.comment,
            },
            status=200,
        )

    if request.method in ['PUT', 'PATCH']:
        payload = _parse_json_body(request)
        if not payload:
            return JsonResponse({'error': 'Invalid JSON body.'}, status=400)

        # API update supports partial fields for both PUT and PATCH requests.
        booking.first_name = payload.get('first_name', booking.first_name)
        booking.last_name = payload.get('last_name', booking.last_name)
        booking.guest_number = payload.get('guest_number', booking.guest_number)
        booking.comment = payload.get('comment', booking.comment)
        booking.save()

        return JsonResponse(
            {
                'id': booking.id,
                'first_name': booking.first_name,
                'last_name': booking.last_name,
                'guest_number': booking.guest_number,
                'comment': booking.comment,
            },
            status=200,
        )

    if request.method == 'DELETE':
        booking.delete()
        return JsonResponse({'message': 'Booking deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Method not allowed.'}, status=405)
