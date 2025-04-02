# Online store

Online store with catalog, shopping cart, payment, promo codes.
Also admin panel (with saving invoice) and sending email after successful payment were implemented.


Folders:
- online_store (project folder)
- store (catalog)
- orders
- cart for storing goods in cart (via Django session)
- payment (via Stripe)
- coupons for using promo codes for discounts


Used technologies:
- Django
- SQLite3
- RabbitMQ
- Celery
- Stripe, webhook
- xhtml2pdf (for generating pdf's invoice from HTML)