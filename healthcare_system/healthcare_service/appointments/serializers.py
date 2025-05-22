from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor_name', 'appointment_date', 'status', 'created_at']
        read_only_fields = ['created_at']  # Bỏ 'user' khỏi read_only_fields