import random
from .models import FoodItem as Food

def auto_bill(request):
    order_id = "ORD" + str(random.randint(10000, 99999))

    food_ids = request.POST.getlist('food[]')
    qtys = request.POST.getlist('qty[]')
    payment_type = request.POST.get('payment_type', 'full')

    items = []
    total = 0

    for i in range(len(food_ids)):
        if food_ids[i] != "":
            try:
                food = Food.objects.get(id=food_ids[i])

                qty = int(qtys[i])
                price = food.price
                item_total = price * qty

                total += item_total

                items.append({
                    "name": food.name,
                    "qty": qty,
                    "price": price,
                    "total": item_total
                })
            except:
                pass

    pay_amount = int(total * 0.3) if payment_type == "advance" else total

    return {
        "order_id": order_id,
        "items": items,
        "total": total,
        "pay_amount": pay_amount,
        "payment_type": payment_type
    }
