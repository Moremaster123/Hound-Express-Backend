from rest_framework import serializers

from .models import Estatus, Guia


class EstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = ["id", "status", "timestamp", "updatedBy"]


class GuiaSerializer(serializers.ModelSerializer):
    history = EstatusSerializer(many=True, read_only=True)
    updatedBy = serializers.CharField(write_only=True, required=False, max_length=20)

    class Meta:
        model = Guia
        fields = [
            "id", "trackingNumber", "recipient", "origin", "destination",
            "createdAt", "updatedAt", "currentStatus", "updatedBy", "history",
        ]
        read_only_fields = ["id", "updatedAt"]
        extra_kwargs = {"trackingNumber": {"validators": []}}

    def validate_trackingNumber(self, value):
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError("El número de guía es obligatorio.")
        repetidas = Guia.objects.filter(trackingNumber__iexact=value)
        if self.instance:
            repetidas = repetidas.exclude(pk=self.instance.pk)
        if repetidas.exists():
            raise serializers.ValidationError("Ya existe una guía con este número.")
        return value

    def validate(self, data):
        for field in ["recipient", "origin", "destination"]:
            if field in data:
                data[field] = data[field].strip()
        return data

    def create(self, validated_data):
        updated_by = validated_data.pop("updatedBy", "sistema")
        guia = super().create(validated_data)
        Estatus.objects.create(guideId=guia, status=guia.currentStatus, updatedBy=updated_by)
        return guia

    def update(self, instance, validated_data):
        updated_by = validated_data.pop("updatedBy", "sistema")
        previous_status = instance.currentStatus
        guia = super().update(instance, validated_data)
        if guia.currentStatus != previous_status:
            Estatus.objects.create(guideId=guia, status=guia.currentStatus, updatedBy=updated_by)
        return guia
