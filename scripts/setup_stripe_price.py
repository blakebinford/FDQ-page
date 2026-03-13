import stripe
from decouple import config

stripe.api_key = config('STRIPE_SECRET_KEY')

price = stripe.Price.create(
    product='prod_U8qcEHOqJbUEKS',
    currency='usd',
    unit_amount=50000,  # $500.00
)

print(f'Price ID: {price.id}')
print(f'Amount: ${price.unit_amount / 100:.2f}')
print(f'Product: {price.product}')
