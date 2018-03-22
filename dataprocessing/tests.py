from dataprocessing.CallDetails import CallDetails
from dataprocessing.BillCalculator import BillCalculator
from datetime import datetime
from pytz import timezone


def shell_test_calculate_bill():
    tz = timezone('America/Sao_Paulo')
    bill_calc = BillCalculator()
    bill_calc.set_tz(tz)

    source = '1234567891'
    destination = '9876543219'

    cd_list = []
    real_price = []
    # 30 minutes on standard time call
    # 0.36 + 30*0.09 = 3.06
    real_price.append(3.06)
    call_id = 0
    start = datetime(2018, 3, 21, 12, 0, 0, 0, tz)
    end = datetime(2018, 3, 21, 12, 30, 0, 0, tz)

    cd_aux = CallDetails()
    cd_aux.set_values(call_id, start, end, source, destination)
    cd_aux.set_valid()
    cd_list.append(cd_aux)

    # 90 minutes on standard time call
    # 0.36 + 90*0.09 = 8.46
    real_price.append(8.46)
    call_id = 1
    start = datetime(2018, 3, 21, 12, 0, 0, 0, tz)
    end = datetime(2018, 3, 21, 13, 30, 0, 0, tz)

    cd_aux = CallDetails()
    cd_aux.set_values(call_id, start, end, source, destination)
    cd_aux.set_valid()
    cd_list.append(cd_aux)

    # 30 minutes between
    # 0.36 + 15*0.09 = 1.71
    real_price.append(1.71)
    call_id = 2
    start = datetime(2018, 3, 21, 21, 45, 0, 0, tz)
    end = datetime(2018, 3, 21, 22, 15, 0, 0, tz)

    cd_aux = CallDetails()
    cd_aux.set_values(call_id, start, end, source, destination)
    cd_aux.set_valid()
    cd_list.append(cd_aux)

    # call starts one day and finishes another on reduced tariff
    # 0.36 + 0 = 0.36
    real_price.append(0.36)
    call_id = 3
    start = datetime(2018, 3, 21, 23, 0, 0, 0, tz)
    end = datetime(2018, 3, 22, 0, 30, 0, 0, tz)

    cd_aux = CallDetails()
    cd_aux.set_values(call_id, start, end, source, destination)
    cd_aux.set_valid()
    cd_list.append(cd_aux)

    # call starts one day and finishes another
    # 0.36 + 86.40 = 86.76
    real_price.append(86.76)
    call_id = 4
    start = datetime(2018, 3, 21, 23, 0, 0, 0, tz)
    end = datetime(2018, 3, 23, 0, 30, 0, 0, tz)

    cd_aux = CallDetails()
    cd_aux.set_values(call_id, start, end, source, destination)
    cd_aux.set_valid()
    cd_list.append(cd_aux)

    bill_calc.calculate_bill(cd_list)

    for i in range(0, len(cd_list)):
        msg = 'Call ' + str(i) + ' should cost ' + str(real_price[i])
        msg += ' and it costs ' + cd_list[i].get_call_price()
        print(msg)
