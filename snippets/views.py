from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from snippets.serializers import CallRecordSignalSnippetSerializer
from dataprocessing.SignalValidator import SignalValidator

# Create your views here.


@csrf_exempt
def snippet_signaling(request):
    try:
        if request.method == 'PUT':
            data = JSONParser().parse(request)
            validator = SignalValidator()
            e = validator.validate(data, False)
            if not e.is_valid():
                return HttpResponse(
                    e.get_msg(),
                    status=e.get_http_code()
                )
            serializer = CallRecordSignalSnippetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(e.get_msg(), status=e.get_http_code())
            return HttpResponse(
                "Field error - {}".format(serializer.errors),
                status=400
            )
    except Exception as e:
        return HttpResponse(str(e), status=500)
