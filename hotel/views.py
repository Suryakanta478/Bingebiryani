from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum
from datetime import date, timedelta
import random, time
from hotel import views
from .models import RoomCategory, Room, RoomBooking, FoodItem, PartyBooking, FoodOrder
import razorpay
import io
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
import random
import time
from django.conf import settings
from django.contrib.auth.models import User
from .utils import auto_bill
from django.http import HttpResponse

def verify_payment(request):
    return HttpResponse("Payment Verified"
)

def failure(request):
    return HttpResponse("Payment Failed ❌")

def success(request):
    return render(request, "success.html")

def party_booking(request):
    if request.method == "POST":
        bill = auto_bill(request)
        return render(request, "bill.html", bill)

    foods = Food.objects.all()
    return render(request, "party.html", {"foods": foods})

def room_booking(request):
    if request.method == "POST":
        bill = auto_bill(request)

        # 🔹 ROOM PRICE ADD
        room_price = 2000   # ya DB se lao
        bill["total"] += room_price
        bill["pay_amount"] += room_price

        return render(request, "bill.html", bill)

def food_order(request):
    if request.method == "POST":
        bill = auto_bill(request)
        return render(request, "bill.html", bill)



def resend_otp(request):
    email = request.session.get("email")   # session se email lo

    if not email:
        return redirect("login")

    otp = str(random.randint(1000, 9999))

    request.session["otp"] = otp
    request.session["time"] = time.time()
    request.session["email"] = email

    send_otp(email, otp)   # tumhara existing function

    return redirect("verify_otp.html")


# 🔹 OTP SEND
def send_otp(email, otp):
    send_mail(
        "Your OTP",
        f"Your OTP is {otp}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

# 🔹 HOME (login check)
def home(request):
    if not request.user.is_authenticated:
        return redirect("signup")

    return render(request, "home.html")

# 🔹 SIGNUP (OTP FLOW)
import uuid
import random
import time

def signup(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        request.session['temp'] = {
            "username": username,
            "email": email,
            "password": password
        }

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        # signup view me (tera same logic)
        username = email.split("@")[0] + str(uuid.uuid4())[:4]

        otp = str(random.randint(1000, 9999))
        request.session['otp'] = otp
        request.session['time'] = time.time()

        send_otp(email, otp)
        return redirect("verify_signup")

    return render(request, "signup.html")

# 🔹 VERIFY SIGNUP OTP

def verify_signup(request):
    if request.method == "POST":

        if time.time() - request.session.get("time", 0) > 300:
            return HttpResponse("OTP Expired")

        if request.POST.get("otp") == request.session.get("otp"):

            data = request.session.get("temp")

            # 🔥 check if user already exists
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"]
                }
            )

            # 🔐 set password only if new user
            if created:
                user.set_password(data["password"])
                user.save()

            # ✅ AUTO LOGIN
            login(request, user)

            # 🧹 VERY IMPORTANT
            login(request, user)

# ✅ sirf unwanted data hatao
            request.session.pop("otp", None)
            request.session.pop("time", None)
            request.session.pop("temp", None)

            # ✅ HOME PAGE
            return redirect("home")

        else:
            return HttpResponse("Wrong OTP ❌")

    return render(request, "verify.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)

        # 🔴 user find karo username se
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("User not found ❌")

        # 🔴 authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            otp = str(random.randint(1000, 9999))

            print("OTP:", otp)
            print("EMAIL:", user_obj.email)

            # session save
            request.session["login_user"] = user.id
            request.session["otp"] = otp
            request.session["time"] = time.time()
            request.session["email"] = user_obj.email

            # 🔥 send OTP on email
            send_otp(user_obj.email, otp)

            return redirect("home")
        else:
            return HttpResponse("Wrong password ❌")

    return render(request, 'login.html')

# 🔹 VERIFY LOGIN OTP
def verify_login(request):
    if request.method == "POST":

        # OTP expire check
        if time.time() - request.session.get("time", 0) > 300:
            return HttpResponse("OTP Expired ⏰")

        # OTP verify
        if request.POST.get("otp") == request.session.get("otp"):

            # Get user from session
            user = User.objects.get(id=request.session.get("login_user"))

            # Auto login
            login(request, user)

            # Clear session
            login(request, user)

# ✅ sirf unwanted data hatao
            request.session.pop("otp", None)
            request.session.pop("time", None)
            request.session.pop("temp", None)

            return redirect("home")

        else:
            return HttpResponse("Wrong OTP ❌")

    return render(request, "verify.html")

# 🔹 FORGOT PASSWORD
def forgot(request):
    if request.method == "POST":

        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():
            return HttpResponse("User not found")

        otp = str(random.randint(1000, 9999))

        request.session["email"] = email
        request.session["otp"] = otp
        request.session["time"] = time.time()

        send_otp(email, otp)
        return redirect("reset")

    return render(request, "forgot.html")


# 🔹 RESET PASSWORD
def reset(request):
    if request.method == "POST":

        if time.time() - request.session.get("time", 0) > 300:
            return HttpResponse("OTP Expired")

        if request.POST.get("otp") == request.session.get("otp"):

            user = User.objects.get(email=request.session.get("email"))
            user.set_password(request.POST.get("password"))
            user.save()

            request.session.flush()
            return redirect("login")

    return render(request, "reset.html")


# 🔹 LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")


# 🔹 PROFILE
@login_required
def profile(request):
    bookings = RoomBooking.objects.filter(user=request.user)
    food_orders = FoodOrder.objects.filter(user=request.user)

    return render(request, "profile.html", {
        "bookings": bookings,
        "food_orders": food_orders
    })


# 🔹 ROOM BOOKING
@login_required
def book_room(request):

    rooms = Room.objects.all()

    if request.method == "POST":

        room = Room.objects.get(id=request.POST.get("room"))

        if not room.available:
            return HttpResponse("Room not available")

        RoomBooking.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            room=room,
            check_in=request.POST.get("checkin"),
            check_out=request.POST.get("checkout")
        )

        room.available = False
        room.save()

        return redirect("/payment/")

    return render(request, "book_room.html", {"rooms": rooms})


# 🔹 DASHBOARD
@login_required
def dashboard(request):

    earnings = RoomBooking.objects.filter(
        payment_status=True
    ).aggregate(Sum('room__price'))

    food_sales = FoodOrder.objects.filter(
        paid=True
    ).aggregate(Sum('total_price'))

    return render(request, "dashboard.html", {
        "room_earnings": earnings,
        "food_earnings": food_sales
    })


# 🔹 MENU
@login_required
def menu(request):
    items = MenuItem.objects.all()
    foods = FoodItem.objects.all()

    context = {
        'items': items,
        'foods': foods
    }

    return render(request, 'menu.html', context)

# 🔹 PARTY BOOKING
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET)
)

@login_required
def party(request):

    if request.method == "POST":
        try:
            # 🔹 Get form data
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            people = int(request.POST.get("people", 1))  # default to 1
            date = request.POST.get("date")
            food_ids = request.POST.getlist("food[]")
            quantities = request.POST.getlist("qty[]")
            payment_type = request.POST.get("payment")

            # 🔹 Calculate total
            total = 0

            # 🔹 CREATE BOOKING
            booking = PartyBooking.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                people=people,
                date=date,
                payment_type=payment_type,
                total_price=0
            )

            # 🔹 ADD FOOD ITEMS
            for i in range(len(food_ids)):
                if quantities[i] == "":
                    continue
                qty = int(quantities[i])
                if qty <= 0:
                    continue

                food = FoodItem.objects.get(id=food_ids[i])
                BookingItem.objects.create(
                    booking=booking,
                    food_item=food,
                    quantity=qty
                )
                total += food.price * qty

            # 🔹 PER PERSON COST
            total += people * 500

            # 🔹 UPDATE TOTAL
            booking.total_price = total
            booking.save()

            # 🔹 PAYMENT LOGIC
            if payment_type == "advance":
                amount = int(total * 0.3)
            else:
                amount = total

            amount_paise = amount * 100

            # 🔹 RAZORPAY ORDER
            order = client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": "1"
            })

            # 🔹 SAVE SESSION
            request.session['booking_id'] = booking.id
            request.session['pay_amount'] = amount

            # 🔹 CREATE PDF
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            y = 800
            p.drawString(200, y, "Party Booking Bill")
            y -= 40
            p.drawString(50, y, f"Name: {name}")
            y -= 20
            p.drawString(50, y, f"Email: {request.user.email}")
            y -= 20
            p.drawString(50, y, f"Phone: {phone}")
            y -= 20
            p.drawString(50, y, f"People: {people}")
            y -= 40

            for item in booking.items.all():
                price = item.food_item.price * item.quantity
                p.drawString(50, y, f"{item.food_item.name} x {item.quantity} = ₹{price}")
                y -= 20

            y -= 20
            p.drawString(50, y, f"Total: ₹{total}")
            p.showPage()
            p.save()
            pdf = buffer.getvalue()
            buffer.close()

            # 🔹 EMAIL
            email = EmailMessage(
                "Your Booking Bill",
                "Attached is your bill",
                settings.EMAIL_HOST_USER,
                [request.user.email]
            )
            email.attach("bill.pdf", pdf, "application/pdf")
            email.send(fail_silently=True)

            # 🔹 GO TO PAYMENT PAGE
            return render(request, "payment.html", {
                "order_id": order['id'],
                "amount": amount,
                "razorpay_key": settings.RAZORPAY_KEY
            })

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, "party.html", {"foods": foods})

# 🔹 PAYMENT
@login_required
def payment(request):

    client = razorpay.Client(
        auth=("rzp_test_SPYWvGotl2ezQR", "WlGCwHfVSB6DYDppop6yZ0iy")
    )

    order = client.order.create({
        "amount": 50000,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "payment.html", {"order": order})


# 🔹 PAYMENT SUCCESS
@login_required
def payment_success(request):

    # 🔹 Agar AJAX call hai (Razorpay handler)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"status": "Payment Successful"})

    # 🔹 Normal flow (page redirect ke liye)
    booking_id = request.session.get("booking_id")
    paid_amount = request.session.get("pay_amount")

    if not booking_id:
        return redirect("party")

    try:
        booking = PartyBooking.objects.get(id=booking_id)
    except PartyBooking.DoesNotExist:
        return redirect("party")

    # 🔹 Mark booking confirmed
    booking.confirmed = True
    booking.save()

    # 🔹 LOGIN FIX (agar logout ho gaya ho)
    if not request.user.is_authenticated:
        user_id = request.session.get("user_id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                login(request, user)
            except User.DoesNotExist:
                return redirect("login")

    return render(request, "success.html", {
        "total": booking.total_price,
        "paid": paid_amount
    })

# 🔹 PAYMENT HISTORY
@login_required
def payment_history(request):
    payments = RoomBooking.objects.filter(
        user=request.user,
        payment_status=True
    )
    return render(request, "payment.html", {"payments": payments})

def verify_otp(request):
    return HttpResponse("OTP page")

# PAYMENT
@login_required
def party(request):
    import random

    foods = FoodItem.objects.all()

    if request.method == "POST":
        food_ids = request.POST.getlist('food[]')
        quantities = request.POST.getlist('qty[]')
        payment_type = request.POST.get("payment_type")

        items = []
        total = 0

        for i in range(len(food_ids)):
            food = FoodItem.objects.get(id=food_ids[i])
            qty = int(quantities[i])
            price = food.price * qty

            total += price

            items.append({
                "name": food.name,
                "qty": qty,
                "price": price
            })

        # ✅ ORDER ID generate
        order_id = "ORD" + str(random.randint(10000, 99999))

        # ✅ PAYMENT LOGIC
        if payment_type == "advance":
            paid = int(total * 0.3)
        else:
            paid = total

        # ✅ FINAL DATA
        data = {
            "order_id": order_id,
            "items": items,
            "total": total,
            "paid": paid
        }

        return render(request, "payment.html", data)

    return render(request, "party.html", {"foods": foods})
