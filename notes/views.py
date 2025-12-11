from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from authentication.models import AppUser

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            app_user = AppUser.objects.get(user=self.request.user)
            if app_user.organization:
                return Note.objects.filter(organization=app_user.organization)
            return Note.objects.filter(user=self.request.user)
        except AppUser.DoesNotExist:
            return Note.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            app_user = AppUser.objects.get(user=request.user)
            if not app_user.organization:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"error": "You are not part of any organization"})
            
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                "organization": app_user.organization.name,
                "notes": serializer.data
            })
        except AppUser.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"error": "AppUser not found"})

    def perform_create(self, serializer):
        try:
            app_user = AppUser.objects.get(user=self.request.user)
            if not app_user.organization:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"error": "You are not part of any organization"})
            serializer.save(user=self.request.user, organization=app_user.organization)
        except AppUser.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"error": "AppUser not found"})
