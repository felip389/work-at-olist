from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from snippets.serializers import CallRecordSignalSnippetSerializer
from snippets.models import CallRecordSignalSnippet
import re

# Create your views here.


@csrf_exempt
def snippet_signaling(request):
    try:
        if request.method == 'PUT':
            data = JSONParser().parse(request)

            # input block validation
            # recordId field validation
            record_id = data.get('recordId')
            snippet = CallRecordSignalSnippet.objects.filter(
                recordId=record_id
            )
            if snippet.count() is not 0:
                return HttpResponse('recordId error', status=400)

            # callType field validation
            call_type = data.get('callType')
            if call_type not in ('Start', 'End'):
                return HttpResponse(
                    'callType error - invalid field',
                    status=400
                )

            # call_id field validation
            call_id = data.get('call_id')
            snippet_call_end = CallRecordSignalSnippet.objects.filter(
                call_id=call_id,
                callType='End',
            )
            snippet_call_start = CallRecordSignalSnippet.objects.filter(
                call_id=call_id,
                callType='Start',
            )

            # case 1: call is already finished
            if snippet_call_end.count() is not 0:
                return HttpResponse(
                    'call_id error - Call already finished',
                    status=400
                )

            # case 2: call was started and not yet finished
            if snippet_call_start.count() is not 0:
                if data.get('callType') in 'Start':
                    return HttpResponse(
                        'call_id error - Call already started',
                        status=400
                    )

            # case 3: call was not started and user wants do finish
            if snippet_call_start.count() is 0:
                if data.get('callType') in 'End':
                    return HttpResponse(
                        'call_id error - Call was not started',
                        status=400
                    )

            # source and destination fields validation
            if call_type in 'Start':
                src_re = re.match(r'\d{10,11}', data.get('source'))
                dst_re = re.match(r'\d{10,11}', data.get('destination'))
                if src_re is None:
                    return HttpResponse(
                        'source error - Invalid source',
                        status=400
                    )
                if dst_re is None:
                    return HttpResponse(
                        'destination error - Invalid destination',
                        status=400
                    )

            # if signal is to finish a call and has source/destination filled
            if call_type in 'End':
                data['source'] = ''
                data['destination'] = ''

            # timestamp field validation
            # as there isnt any definition about the timestamp format, the
            # input timestamp will be ignored and we'll consider only the
            # sql generated timestamp
            if 'timestamp' in data:
                data['timestamp'] = ''

            serializer = CallRecordSignalSnippetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Signaling success', status=201)
            return HttpResponse(
                "Field error - {}".format(serializer.errors),
                status=400
            )
    except Exception as e:
        return HttpResponse(str(e), status=500)
