from rest_framework import serializers
from .models import Organization, AppUser

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

class AppUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'organization', 'organization_id']

    def create(self, validated_data):
        org_id = validated_data.pop('organization_id')
        organization = Organization.objects.get(id=org_id)
        return AppUser.objects.create(organization=organization, **validated_data)
