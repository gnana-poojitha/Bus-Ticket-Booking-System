# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
# from rest_framework import status, generics
# from rest_framework.views import APIView
# from .serializers import UserRegisterSerializer,BusSerializer,BookingSerializer
# from rest_framework.response import Response
# from .models import Bus, Seat , Booking

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserRegisterSerializer(data= request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token':token.key}, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     def post(self,request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)

#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token':token.key,
#                 'user_id':user.id
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class BusListCreateView(generics.ListCreateAPIView):
#     queryset = Bus.objects.all()
#     serializer_class= BusSerializer

# class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer

# class BookingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         seat_id = request.data.get('seat')
#         try:
#             seat = Seat.objects.get(id = seat_id)
#             if seat.is_booked:
#                 return Response({'error': 'Seat already booked'}, status =status.HTTP_400_BAD_REQUEST)
#             seat.is_booked=True
#             seat.save()

#             bookings=Booking.objects.create(
#                 user = request.user,
#                 bus = seat.bus,
#                 seat = seat
#             )

#             serializer =BookingSerializer(bookings)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Seat.DoesNotExist:
#             return Response({'error':'Invalid Seat ID'}, status=status.HTTP_400_BAD_REQUEST)
        
# class UserBookingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         if request.user.id != user_id:
#             return Response({'error':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         bookings = Booking.objects.filter(user_id=user_id)
#         serializer = BookingSerializer(bookings,many=True)
#         return Response(serializer.data)





# authicate, permission, token, status, response, generics, apiviews
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
import stripe

from .serializers import UserRegisterSerializer, BusSerializer, BookingSerializer
from .models import Bus, Seat, Booking




# Stripe setup
stripe.api_key = settings.STRIPE_SECRET_KEY

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'},
         status=status.HTTP_401_UNAUTHORIZED)

class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get('seat')
        try:
            seat = Seat.objects.get(id=seat_id)
            if seat.is_booked:
                return Response({'error': 'Seat already booked'}, status=status.HTTP_400_BAD_REQUEST)

            seat.is_booked = True
            seat.save()

            booking = Booking.objects.create(
                user=request.user,
                bus=seat.bus,
                seat=seat
            )
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({'error': 'Invalid Seat ID'}, status=status.HTTP_400_BAD_REQUEST)

class UserBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        bookings = Booking.objects.filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    try:
        data = request.data
        seat_id = data.get("seatId")
        bus_id = data.get("busId")
        price = int(float(data.get("price")) * 100)  
  # convert to paisa
        origin = data.get("origin")
        destination = data.get("destination")
        user_id = request.user.id

        if not all([seat_id, bus_id, price, origin, destination]):
            return Response({"error": "Missing required fields"}, status=400)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": f"Bus Seat {seat_id}",
                            "description": f"{origin} to {destination}",
                        },
                        "unit_amount": price,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://localhost:5173/payment-success?seatId={seat_id}&busId={bus_id}&userId={user_id}",
            cancel_url="http://localhost:5173/payment-cancel",
        )

        return Response({"id": session.id})

# try:
#     # ... your Stripe code ...
#     return Response({"id": session.id})

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# views.py
class ConfirmBookingAfterPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get("seatId")
        bus_id = request.data.get("busId")

        if not seat_id or not bus_id:
            return Response({"error": "Missing seatId or busId"}, status=400)

        try:
            seat = Seat.objects.get(id=seat_id)
            if seat.is_booked:
                return Response({"error": "Seat already booked"}, status=400)

            seat.is_booked = True
            seat.save()

            booking = Booking.objects.create(
                user=request.user,
                bus=seat.bus,
                seat=seat
            )

            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=201)

        except Seat.DoesNotExist:
            return Response({"error": "Invalid seatId"}, status=400)
