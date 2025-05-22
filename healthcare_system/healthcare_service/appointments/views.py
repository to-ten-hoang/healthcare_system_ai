from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Appointment
from .serializers import AppointmentSerializer
import requests
import logging

logger = logging.getLogger(__name__)

class AppointmentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user).order_by('appointment_date')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = self._get_user_id(request)
        if user_id is None:
            return Response({"error": "Unable to fetch user ID"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['user'] = user_id
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_user_id(self, request):
        try:
            token = request.headers.get('Authorization').split()[1]
            response = requests.get('http://localhost:8000/api/accounts/user-info/', headers={'Authorization': f'Bearer {token}'})
            response.raise_for_status()
            return response.json().get('id')
        except Exception as e:
            logger.error(f"Error fetching user ID: {str(e)}")
            return None

class AppointmentUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllAppointmentsView(APIView):
    permission_classes = [IsAdminUser]  # Chỉ admin được phép truy cập

    def get(self, request):
        appointments = Appointment.objects.all().order_by('appointment_date')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)