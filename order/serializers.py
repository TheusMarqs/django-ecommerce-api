from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Order
        fields = ['client', 'date', 'total']
        
    def to_internal_value(self, data):
        valid_fields = set(self.fields.keys())
        input_fields = set(data.keys())
        invalid_fields = input_fields - valid_fields
        
        if invalid_fields:
            raise serializers.ValidationError({
                'invalid_fields': f'Os campos seguintes não são válidos: {", ".join(invalid_fields)}'
            })
        
        return super().to_internal_value({k: v for k, v in data.items() if k in valid_fields})
    
    def get_date(self, obj):
        # Retorne a data formatada como string
        return obj.date.strftime("%Y-%m-%d %H:%M:%S")
