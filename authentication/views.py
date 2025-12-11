import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, permissions
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import Organization, AppUser
from .serializers import OrganizationSerializer, AppUserSerializer
from django.views.decorators.csrf import csrf_exempt


# Register
@csrf_exempt
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Missing fields'}, status=400)

    # Prevent duplicate username or email
    if DjangoUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    if DjangoUser.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    # Create Django auth user
    auth_user = DjangoUser.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # Create AppUser linked to DjangoUser
    app_user = AppUser.objects.create(
        username=username,
        email=email,
        user=auth_user,
        organization=None
    )

    return Response({
        'message': 'User created successfully',
        'user': {
            'auth_user_id': auth_user.id,
            'app_user_id': str(app_user.id),
            'username': username,
            'email': email
        }
    }, status=201)


# Login
@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Get AppUser by FK
    try:
        app_user = AppUser.objects.get(user=user)
    except AppUser.DoesNotExist:
        return Response({"detail": "AppUser not found"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "auth_user_id": user.id,
        "app_user_id": str(app_user.id),   # UUID
        "username": user.username,
        "email": user.email,
        # "organization": app_user.organization.id if app_user.organization else None,
    })


class CreateUserView(APIView):
    def post(self, request):
        serializer = AppUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User successfully created",
                "user": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = AppUserSerializer(user)
        return Response(serializer.data)


class SearchUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username', '')
        
        if not username:
            return Response({
                "error": "Username parameter is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Case-insensitive substring search
        users = AppUser.objects.filter(username__icontains=username)
        serializer = AppUserSerializer(users, many=True)

        return Response({
            "message": "Search completed",
            "count": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)


class CreateOrganizationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            app_user = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            return Response({"error": "AppUser not found"}, status=404)

        # Check if user already created an organization
        if Organization.objects.filter(users__user=request.user).exists():
            return Response({
                "error": "You have already created an organization"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrganizationSerializer(data=request.data)
        
        if serializer.is_valid():
            organization = serializer.save()
            # Assign creator to the organization
            app_user.organization = organization
            app_user.save()
            
            return Response({
                "message": "Organization successfully created",
                "organization": OrganizationSerializer(organization).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Failed to create organization",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(APIView):
    def get(self, request, org_id):
        try:
            organization = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)

        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=200)


class ListOrganizationUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            app_user = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            return Response({"error": "AppUser not found"}, status=404)

        if not app_user.organization:
            return Response({
                "message": "You are not part of any organization"
            }, status=status.HTTP_400_BAD_REQUEST)

        organization = app_user.organization
        users = AppUser.objects.filter(organization=organization)
        serializer = AppUserSerializer(users, many=True)

        return Response({
            "message": "Users successfully retrieved",
            "organization": organization.name,
            "count": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)


class AssignUserToOrganizationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            assigner = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            return Response({"error": "AppUser not found"}, status=404)

        # Check if assigner is part of an organization
        if not assigner.organization:
            return Response({
                "error": "You are not part of any organization"
            }, status=status.HTTP_400_BAD_REQUEST)

        organization = assigner.organization

        try:
            user_to_assign = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return Response({"message": "User not found"}, status=404)

        # Assign user to the organization
        user_to_assign.organization = organization
        user_to_assign.save()

        return Response({
            "message": "User successfully assigned to organization",
            "organization": organization.name,
            "user": {
                "id": str(user_to_assign.id),
                "username": user_to_assign.username,
                "email": user_to_assign.email
            }
        }, status=200)

