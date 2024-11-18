from braces.views import GroupRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

class CartCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            cart = serializer.save()
            return Response({'message': 'Cart successfully registered', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    
class CartUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found.'})

        serializer = CartSerializer(cart, data=request.data) 

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cart successfully updated.', 'cart': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class CartDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, *args, **kwargs):
        try:
            cart = Cart.objects.get(pk=pk)
            cart.delete()
            return Response({'message': 'Cart successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)