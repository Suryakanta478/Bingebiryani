<h2>Your Cart</h2>

{% for item in cart_items %}
<p>{{ item.food.name }} - {{ item.quantity }}</p>
{% endfor %}

<a href="/checkout/">Checkout</a>
