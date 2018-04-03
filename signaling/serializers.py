from rest_framework import serializers
from signaling.models import CallRecordSignal


class CallRecordSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecordSignal
        fields = (
            'id',
            'callType',
            'call_id',
            'timestamp',
            'source',
            'destination',
        )
