from signaling.models import CallRecordSignal
import re
from dateutil.parser import parse
from dataprocessing.SignalResult import SignalResult


class SignalValidator:

    def validate(self, data, test):
        e = SignalResult()

        record_id_name = 'id'
        call_id_name = 'call_id'
        callType_name = 'callType'
        source_name = 'source'
        destination_name = 'destination'


        # input block validation
        # id field validation
        record_id = data.get(record_id_name)
        try:
            record_id = int(record_id)
        except ValueError:
            e.set_result(
                'id error - input id is not a number',
                400,
                False
            )
            return e

        signal = CallRecordSignal.objects.filter(
            id=record_id
        )
        if record_id < 0:
            e.set_result(
                'id error - input id is not positive',
                400,
                False
            )
            return e

        if signal.count() is not 0:
            e.set_result(
                'id error - an id already exists',
                400,
                False
            )
            return e
        if test is False:
            if record_id <= 100:
                e.set_result(
                    'id error - ids from 0 to 100 are reserved',
                    400,
                    False
                )
                return e
        else:
            if record_id > 100:
                e.set_result(
                    'id error - ids starting from 100 are reserved for production',
                    400,
                    False
                )
                return e

        # callType field validation
        call_type = data.get(callType_name)
        if call_type not in ('Start', 'End'):
            e.set_result(
                'callType error - invalid field',
                400,
                False
            )
            return e

        # call_id field validation
        call_id = data.get(call_id_name)
        try:
            call_id = int(call_id)
        except ValueError:
            e.set_result(
                'call_id error - input call_id is not a number',
                400,
                False
            )
            return e
        if call_id < 0:
            e.set_result(
                'call_id error - input call_id is negative',
                400,
                False
            )
            return e
        if test is False:
            if record_id <= 50:
                e.set_result(
                    'call_id error - ids from 0 to 50 are reserved',
                    400,
                    False
                )
                return e
        else:
            if record_id > 50:
                e.set_result(
                    'call_id error - ids starting from 50 are reserved for production',
                    400,
                    False
                )
                return e

        signal_call_end = CallRecordSignal.objects.filter(
            call_id=call_id,
            callType='End',
        )
        signal_call_start = CallRecordSignal.objects.filter(
            call_id=call_id,
            callType='Start',
        )

        # case 1: call is already finished
        if signal_call_end.count() is not 0:
            e.set_result(
                'call_id error - Call already finished',
                400,
                False
            )
            return e

        # case 2: call was started and not yet finished
        if signal_call_start.count() is not 0:
            if data.get(callType_name) in 'Start':
                e.set_result(
                    'call_id error - Call already started',
                    400,
                    False
                )
                return e

        # case 3: call was not started and user wants do finish
        if signal_call_start.count() is 0:
            if data.get(callType_name) in 'End':
                e.set_result(
                    'call_id error - Call was not started',
                    400,
                    False
                )
                return e

        # source and destination fields validation
        if call_type in 'Start':
            src_re = re.match(r'^\d{10,11}$', data.get(source_name))
            dst_re = re.match(r'^\d{10,11}$', data.get(destination_name))
            if src_re is None:
                e.set_result(
                    'source error - Invalid source',
                    400,
                    False
                )
                return e
            if dst_re is None:
                e.set_result(
                    'destination error - Invalid destination',
                    400,
                    False
                )
                return e

        # if signal is to finish a call and has source/destination filled
        if call_type in 'End':
            data[source_name] = ''
            data[destination_name] = ''

        # timestamp format iso 8601 combined date and time

        dte = data.get('timestamp')
        dte_re = re.match(r'^\d{4}-\d\d-\d\d.\d\d:\d\d:\d\d[+-]\d\d:\d\d$', dte)
        if dte_re is None:
            e.set_result(
                'timestamp error - Invalid timestamp',
                400,
                False
            )
            return e
        dte = parse(dte)

        # if user fills timestamp in, it should not have a negative
        # time delta from start to end
        if call_type in 'End':
            if 'timestamp' in data:
                dts = signal_call_start.values_list('timestamp').get()[0]
                if dte < dts:
                    e.set_result(
                        'timing error - call timing error, cannot signal'
                        + ' call end with a timestamp earlier than call'
                        + ' start',
                        400,
                        False
                    )
                    return e

        e.set_result('signaling success', 201, True)
        return e
