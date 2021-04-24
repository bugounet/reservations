from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'owner_name',
            'resource',
            'start_datetime',
            'end_datetime',
            'title',
            'id',
        ]

    owner_name = serializers.CharField(source="owner.username", read_only=True)

    def update(self, instance, validated_data):
        resource = validated_data.pop("resource", None)
        if resource is not None and resource.pk != instance.resource_id:
            instance.resource = resource
        instance.start_datetime = validated_data.get(
            'start_datetime', instance.start_datetime
        )
        instance.end_datetime = validated_data.get(
            'end_datetime', instance.end_datetime
        )
        instance.title = validated_data.get(
            'title', instance.title
        )
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        print(request, request.user)
        if request and hasattr(request, "user"):
            validated_data['owner'] = request.user
        return super(BookingSerializer, self).create(validated_data)


class BookingWithoutResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'owner_name',
            'start_datetime',
            'end_datetime',
            'title',
            'id',
        ]

    owner_name = serializers.CharField(source="owner.username", read_only=True)
