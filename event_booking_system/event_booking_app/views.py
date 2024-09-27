from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer

# APIView for listing all events (publicly accessible)
class ListEventView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# APIView for creating events (admin-only access)
class CreateEventView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# APIView for booking an event (authenticated users only)
class BookEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid():
            try:
                serializer.save()  # Call save without passing user; it's handled in serializer
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# APIView for viewing user bookings (authenticated users only)
class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related('event')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
