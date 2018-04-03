from dataprocessing.CallDetails import CallDetails
from dataprocessing.BillCalculator import BillCalculator
from dataprocessing.SignalValidator import SignalValidator
from datetime import datetime
from pytz import timezone

from signaling.models import CallRecordSignal


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


def shell_test_signaling_validator():

    validator = SignalValidator()
    error_count = 0

    # clear test ids
    aux = CallRecordSignal.objects.filter(
        id__lt=100
    )
    aux.delete()
    aux = CallRecordSignal.objects.filter(
        call_id__lt=50
    )
    aux.delete()

    # generating payload
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    # generating data on database

    # call_id 10 = started and not finished call
    data_to_add = CallRecordSignal(
        id=10,
        callType="Start",
        call_id=10,
        timestamp="2018-01-01 08:37:35-03:00",
        source='12345678901',
        destination='09876543210'
    )
    data_to_add.save()

    # call_id 11 = started and finished call
    data_to_add = CallRecordSignal(
        id=11,
        callType="Start",
        call_id=11,
        timestamp="2018-01-01 08:37:35-03:00",
        source='12345678901',
        destination='09876543210'
    )
    data_to_add.save()
    data_to_add = CallRecordSignal(
        id=12,
        callType="End",
        call_id=11,
        timestamp="2018-01-01 09:37:35-03:00",
        source='12345678901',
        destination='09876543210'
    )
    data_to_add.save()

    # call_id 12 = started call
    data_to_add = CallRecordSignal(
        id=13,
        callType="Start",
        call_id=12,
        timestamp="2018-01-01 08:37:35-03:00",
        source='11111111111',
        destination='09876543210'
    )
    data_to_add.save()

    print("/-------------------------------/")
    print("/---Signaling validator tests---/")
    print("/-------------------------------/")
    print("")
    print("1 - Validating \"id\" field.\n")

    # valid id
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("1.1 - This payload has a valid id: id = 1.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # string valid id
    should_be_valid = True
    data = {
        'id': "1",
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("1.2 - This payload has a valid string id: id = \"2\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # string invalid
    should_be_valid = False
    data = {
        'id': "t",
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("1.3 - This payload has an invalid string id: id = \"t\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # negative value
    should_be_valid = False
    data = {
        'id': -1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("1.4 - This payload has a negative id: id = -1.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # existing value
    should_be_valid = False
    data = {
        'id': 10,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("1.5 - This payload has a duplicate id: id = 10.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")
    print("/-------------------------------/")
    print("")

    # validating callType field
    print("2 - Validating \"callType\" field.\n")
    data["id"] = 1

    # valid callType 1
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("2.1 - This payload has a valid callType: callType = \"Start\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # valid callType 2
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("2.2 - This payload has a valid callType: callType = \"End\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # valid callType 2 - with call initialized
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 10,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("2.3 - Now this call_id has a proper start signal: callType = \"End\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")
    data["call_id"] = 1

    should_be_valid = False
    # invalid callType 1
    data = {
        'id': 1,
        'callType': "end",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("2.4 - This payload has a valid callType: callType = \"end\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid callType 2
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "wasd",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("2.5 - This payload has a valid callType: callType = \"wasd\".")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")
    print("/-------------------------------/")
    print("")

    # validating call_id field
    print("3 - Validating \"call_id\" field.\n")

    # valid starting call_id
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("3.1 - This payload is a valid starting call signal.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # valid finishing call_id
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 10,
        'timestamp': "2018-01-01 18:37:35-03:00"
    }

    # data_to_add was already added on last test session
    err = validator.validate(data, True)
    print("3.2 - This payload is a valid ending call signal.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid call_id
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': "wasd",
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("3.3 - This payload has an invalid call_id.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid starting call_id - call finished
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 11,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    err = validator.validate(data, True)
    print("3.4 - This start signal has the same call_id of an ended call.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid finishing call_id - call finished
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 11,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    err = validator.validate(data, True)
    print("3.5 - This end signal has the same call_id of an ended call.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid starting call_id - call already started
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 10,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    err = validator.validate(data, True)
    print("3.6 - This start signal has the same call_id of a started call.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid finishing call_id - call not started
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 12,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    err = validator.validate(data, True)
    print("3.7 - This end signal has a new call_id.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid finishing call_id - call not started
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': -12,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }

    err = validator.validate(data, True)
    print("3.8 - This end signal has a negative call_id.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")
    print("/-------------------------------/")
    print("")

    # validating source field
    print("4 - Validating \"source\" field.\n")

    # valid source field
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("4.1 - This start signal has a valid source.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid source field - letters
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "asdaasddsa",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("4.2 - This start signal has an invalid source with letters.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid source field - smaller size
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "012345",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("4.3 - This start signal has an invalid source with less digits.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid source field - bigger size
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "0123456789123412",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("4.4 - This start signal has an invalid source with more digits.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid source field - end call

    should_be_valid = True
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 10,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "asdaasddsa",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("4.5 - This end signal has an invalid source.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")
    print("/-------------------------------/")
    print("")

    # validating destination field
    print("5 - Validating \"destination\" field.\n")

    # valid destination field
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("5.1 - This start signal has a valid destination.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid destination field - letters
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "asdaasddsa"
    }
    err = validator.validate(data, True)
    print("5.2 - This start signal has an invalid destination with letters.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid destination field - smaller size
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "012345"
    }
    err = validator.validate(data, True)
    print("5.3 - This start signal has an invalid destination with less digits.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid destination field - bigger size
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "0123456789123412"
    }
    err = validator.validate(data, True)
    print("5.4 - This start signal has an invalid destination with more digits.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid destination field - end call

    should_be_valid = True
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 10,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "asdaasddsa"
    }
    err = validator.validate(data, True)
    print("5.5 - This end signal has an invalid source.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1

    print("")
    print("/-------------------------------/")
    print("")

    # validating timestamp field
    print("6 - Validating \"timestamp\" field.\n")

    # valid timestamp
    should_be_valid = True
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("6.1 - This timestamp is valid.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # invalid timestamp
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "Start",
        'call_id': 1,
        'timestamp': "2018-01-01 18:37:35",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("6.2 - This timestamp is invalid because it has no tz info.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    # end timestamp older than start timestamp
    should_be_valid = False
    data = {
        'id': 1,
        'callType': "End",
        'call_id': 10,
        'timestamp': "2018-01-01 00:37:35-03:00",
        'source': "12345678901",
        'destination': "98765432109"
    }
    err = validator.validate(data, True)
    print("6.3 - This timestamp is invalid, it is older than start call signal.")
    print("Is valid? %s" % err.is_valid())
    if not err.is_valid():
        print("Error message: %s" % err.get_msg())
    print("Should be %s" % should_be_valid)
    if should_be_valid != err.is_valid():
        error_count += 1
    print("")

    print("")
    print("/-------------------------------/")
    print("Error count = %s" % error_count)
    print("/-------------------------------/")

    # clear test ids
    aux = CallRecordSignal.objects.filter(
        id__lt=100
    )
    aux.delete()
    aux = CallRecordSignal.objects.filter(
        call_id__lt=50
    )
    aux.delete()

