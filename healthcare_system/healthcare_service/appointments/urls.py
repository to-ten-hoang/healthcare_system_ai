from django.urls import path
from .views import AppointmentCreateView, AppointmentListView, AppointmentUpdateView, AllAppointmentsView

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('list/', AppointmentListView.as_view(), name='appointment-list'),
    path('update/<int:appointment_id>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('all/', AllAppointmentsView.as_view(), name='all-appointments'),  # Thêm endpoint mới
]