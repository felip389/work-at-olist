from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dataprocessing.BillCalculator import BillCalculator
from django.template import loader
from datetime import datetime, timedelta


# Create your views here.

@csrf_exempt
def source_billing(request):
    source = request.GET.get('source', '')
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    if month is '' or year is '':
        if datetime.now().month is 1:
            year = str(datetime.now().year-1)
            month = str(12)
        else:
            year = str(datetime.now().year)
            month = str(datetime.now().month-1)

    template = loader.get_template('billing/bill.html')
    b = BillCalculator()
    if b.check_input(source, year, month):
        input_error = True
        context = {
            'input_error': input_error
        }
    elif b.check_date(year, month):
        period_error = True
        context = {
            'period_error': period_error
        }
    else:
        title = year + '/' + month + ' - ' + source
        call_list = b.get_bill(source, year, month)

        total_price = 0
        for call in call_list:
            total_price += call.get_call_price_float()
        total_price = 'R$ %.2f' % total_price

        context = {
            'call_list': call_list,
            'title': title,
            'total_price': total_price
        }

    return HttpResponse(template.render(context, request))

