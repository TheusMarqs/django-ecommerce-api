from braces.views import GroupRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

        
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        cart = Cart.objects.get(user_id=user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
class CartClean(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user_id = request.query_params.get('user_id')
        cart = Cart.objects.get(user_id=user_id)
        cart.cart_items.all().delete()
        cart.update_total()
        return Response({"message": "Cart cleared successfully."}, status=status.HTTP_200_OK)
    


class CartItemCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        cart = Cart.objects.get(user_id=user_id)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
            if product.stock < quantity:
                return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            cart.update_total()
            return Response({"message": "Product added to cart."}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CartItemDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user_id = request.data.get('user_id')
        cart = Cart.objects.get(user_id=user_id)
        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)

        except CartItem.DoesNotExist:
            return Response({"error": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class CartViewById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found.'})
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        