from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dataprocessing.BillCalculator import BillCalculator


# Create your views here.

@csrf_exempt
def source_billing(request):
    source = request.GET.get('source', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    b = BillCalculator()
    try:
        txt = b.getBill(source, year, month)

    except Exception as e:
        return HttpResponse(str(e))

    return HttpResponse(txt)
