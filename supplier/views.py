from braces.views import GroupRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class SupplierCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SupplierSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Supplier successfully registered', 'supplier': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class SupplierView(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class SupplierViewById(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response({'detail': 'Supplier not found.'})
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class SupplierUpdate(APIView):
    def put(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response({'detail': 'Supplier not found.'})

        serializer = SupplierSerializer(supplier, data=request.data) 

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Supplier successfully updated.', 'supplier': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class SupplierDelete(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
            supplier.delete()
            return Response({'message': 'Supplier successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response({'detail': 'Supplier not found.'}, status=status.HTTP_404_NOT_FOUND)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)