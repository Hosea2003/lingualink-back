from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import stripe
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
class StripeView(APIView):
    def post(self):
        data = self.request.data
        price_id = data.get('price_id')
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
        except Exception as e:
            return Response({
                'error':'Something went wrong when creating stripe checkout'
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return redirect(checkout_session.url)
    
class PriceView(APIView):
    def get(self, request):
        products = stripe.Product.list()
        result=[]

        for product in products["data"]:
            prices=stripe.Price.list(product=product["id"])
            _product={
                "name":product["name"],
                "id":product["id"],
                "prices":prices["data"]
            }
            result.append(_product)

        return Response(result)