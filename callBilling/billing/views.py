from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dataprocessing.BillCalculator import BillCalculator
from django.template import loader


# Create your views here.

@csrf_exempt
def source_billing(request):
    source = request.GET.get('source', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    debug = request.GET.get('debug', '')
    b = BillCalculator()

    call_list = b.get_bill(source, year, month)
    try:
        log = b.generate_log(call_list, debug)

    except Exception as e:
        return HttpResponse(str(e))

    title = year + '/' + month + ' - ' + source

    template = loader.get_template('billing/bill.html')
    context = {
        'log': log,
        'title': title
    }

    return HttpResponse(template.render(context, request))
