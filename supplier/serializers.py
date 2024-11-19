from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id','name', 'email', 'phone', 'category']
        
    def to_internal_value(self, data):
        valid_fields = set(self.fields.keys())
        input_fields = set(data.keys())
        invalid_fields = input_fields - valid_fields
        
        if invalid_fields:
            raise serializers.ValidationError({
                'invalid_fields': f'Os campos seguintes não são válidos: {", ".join(invalid_fields)}'
            })
        
        return super().to_internal_value({k: v for k, v in data.items() if k in valid_fields})
