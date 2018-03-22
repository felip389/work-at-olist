from snippets.models import CallRecordSignalSnippet
import re
from dateutil.parser import parse
from dataprocessing.SignalResult import SignalResult


class SignalValidator:

    def validate(self, data):
        e = SignalResult()

        # input block validation
        # recordId field validation
        record_id = data.get('recordId')
        snippet = CallRecordSignalSnippet.objects.filter(
            recordId=record_id
        )
        if snippet.count() is not 0:
            e.set_result(
                'recordId error - a recordId already exists',
                400,
                False
            )
            return e

        # callType field validation
        call_type = data.get('callType')
        if call_type not in ('Start', 'End'):
            e.set_result(
                'callType error - invalid field',
                400,
                False
            )
            return e

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
            e.set_result(
                'call_id error - Call already finished',
                400,
                False
            )
            return e

        # case 2: call was started and not yet finished
        if snippet_call_start.count() is not 0:
            if data.get('callType') in 'Start':
                e.set_result(
                    'call_id error - Call already started',
                    400,
                    False
                )
                return e

        # case 3: call was not started and user wants do finish
        if snippet_call_start.count() is 0:
            if data.get('callType') in 'End':
                e.set_result(
                    'call_id error - Call was not started',
                    400,
                    False
                )
                return e

        # source and destination fields validation
        if call_type in 'Start':
            src_re = re.match(r'\d{10,11}', data.get('source'))
            dst_re = re.match(r'\d{10,11}', data.get('destination'))
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
            data['source'] = ''
            data['destination'] = ''

        # if user fills timestamp in, it should not have a negative
        # time delta from start to end
        # timestamp format iso 8601 combined date and time in UTC
        if call_type in 'End':
            if 'timestamp' in data:
                dts = snippet_call_start.values_list('timestamp').get()[0]
                dte = data.get('timestamp')
                dte = parse(dte)
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
