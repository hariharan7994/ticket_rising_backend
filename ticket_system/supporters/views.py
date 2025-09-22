from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SupporterDetailSerializer
from superadmin.models import Supporter,Designation
from rest_framework import generics, permissions
from .serializers import DesignationSerializer


from .serializers import (
    SupporterSerializer,
    SupporterRegisterSerializer,
    SupporterLoginSerializer,
)
from superadmin.models import Supporter


# ============ Register Supporter (SuperAdmin Only) ============ #
class SupporterRegisterView(APIView):
    permission_classes = [permissions.IsAdminUser]  # only SuperAdmin can create

    def post(self, request):
        serializer = SupporterRegisterSerializer(data=request.data)
        if serializer.is_valid():
            supporter = serializer.save()
            return Response(
                {"message": "Supporter created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============ Supporter Login ============ #
class SupporterLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SupporterLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "designation": (
                    user.supporter.designation.name if user.supporter.designation else None
                ),
            },
            status=status.HTTP_200_OK,
        )
    
#=================supporter logout=================#    
class SupporterLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# ============ Supporter Profile (Authenticated) ============ #
class SupporterProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "supporter"):
            return Response(
                {"error": "Not a supporter"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = SupporterSerializer(request.user.supporter)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # ============ List All Supporters (SuperAdmin Only) ============ #
class SupporterListView(generics.ListAPIView):
    queryset = Supporter.objects.all()
    serializer_class = SupporterDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only superadmin can view supporter list
        if not self.request.user.is_superadmin:
            return Supporter.objects.none()
        return super().get_queryset()


# ============ Retrieve/Update/Delete Supporter (SuperAdmin Only) ============ #
class SupporterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supporter.objects.all()
    serializer_class = SupporterDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict access only for superadmin
        if not self.request.user.is_superadmin:
            return Supporter.objects.none()
        return super().get_queryset()




class DesignationListCreateView(generics.ListCreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAdminUser]  # only SuperAdmin

class DesignationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAdminUser]  # only SuperAdmin
