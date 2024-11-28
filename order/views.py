from braces.views import GroupRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

class OrderCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order successfully registered', 'order': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class OrderViewById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'})
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class OrderViewByClientId(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            orders = Order.objects.filter(client=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'})
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class OrderUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'})

        serializer = OrderSerializer(order, data=request.data) 

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order successfully updated.', 'order': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class OrderDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({'message': 'Order successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)