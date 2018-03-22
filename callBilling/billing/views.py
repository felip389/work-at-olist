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
    b = BillCalculator()
    try:

        call_list = b.get_bill(source, year, month)

    except Exception as e:
        return HttpResponse(str(e))

    title = year + '/' + month + ' - ' + source

    total_price = 0
    for call in call_list:
        total_price += call.get_call_price_float()
    total_price = 'R$ %.2f' % total_price

    template = loader.get_template('billing/bill.html')
    context = {
        'call_list': call_list,
        'title': title,
        'total_price': total_price
    }

    return HttpResponse(template.render(context, request))

