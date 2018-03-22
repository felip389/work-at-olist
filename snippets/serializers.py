from rest_framework import serializers
from snippets.models import CallRecordSignalSnippet


class CallRecordSignalSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecordSignalSnippet
        fields = (
            'recordId',
            'callType',
            'call_id',
            'timestamp',
            'source',
            'destination',
        )
