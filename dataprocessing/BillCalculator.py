from snippets.models import CallRecordSignalSnippet
import re
from pytz import timezone
from dataprocessing.CallDetails import CallDetails
from datetime import datetime, timedelta


class BillCalculator:

    def __init__(self):
        self.tz = timezone('America/Sao_Paulo')

    def set_tz(self, tz):
        self.tz = tz

    def get_bill(self, source, year, month):
        call_ids = self.get_month_call_ids(source, year, month)
        call_details_list = self.get_call_list(call_ids)
        self.calculate_bill(call_details_list)
        return call_details_list

    def check_input(self, source, year, month):
        src_re = re.match(r'^\d{10,11}$', source)
        if src_re is None:
            return True
        year_re = re.match(r'^\d{4}$', year)
        if year_re is None:
            return True
        month_re = re.match(r'^\d{1,2}$', month)
        if month_re is None:
            return True
        if int(month) == 0 or int(month) > 12:
            return True
        return False

    def check_date(self, year, month):
        now = datetime.now()
        if int(year) > now.year:
            return True
        elif int(year) == now.year:
            if int(month) >= now.month:
                return True
        return False

    def get_month_call_ids(self, source, year, month):
        if int(month) is 12:
            end_year = int(year) + 1
            end_month = 1
        else:
            end_year = int(year)
            end_month = int(month) + 1

        if int(month) is 1:
            previous_year = int(year) - 1
            previous_month = 12
        else:
            previous_year = int(year)
            previous_month = int(month) - 1

        start_timestamp = datetime(previous_year, previous_month, 1, 0, 0, 0, 0,
                                   timezone('America/Sao_Paulo'))
        actual_timestamp = datetime(int(year), int(month), 1, 0, 0, 0, 0,
                                    timezone('America/Sao_Paulo'))
        end_timestamp = datetime(end_year, end_month, 1, 0, 0, 0, 0,
                                 timezone('America/Sao_Paulo'))
        source_call_signals = CallRecordSignalSnippet.objects.filter(
            source=source,
            callType='Start',
            timestamp__gte=start_timestamp,
            timestamp__lt=end_timestamp
        )
        source_call_ids = source_call_signals.values('call_id')
        call_ids = []
        for i in range(0, source_call_ids.count()):
            s = CallRecordSignalSnippet.objects.filter(
                call_id=source_call_ids[i]['call_id'],
                callType='End'
            )
            if s.count() > 0:
                timestamp_aux = s.values('timestamp')[0]['timestamp']
                if timestamp_aux > actual_timestamp:
                    if timestamp_aux < end_timestamp:
                        call_ids.append(
                            s.values('call_id')[0]['call_id'])
        return call_ids

    def get_call_list(self, call_ids):

        call_details_list = []
        for i in call_ids:
            invalid_msg = ''
            start_call_signal = CallRecordSignalSnippet.objects.filter(
                call_id=i,
                callType='Start'
            )
            if start_call_signal.count() == 1:
                is_valid = True
            elif start_call_signal.count() == 0:
                invalid_msg = 'Invalid start signal or missing call_id ' + i
                is_valid = False
            else:
                invalid_msg = 'Invalid signal pair - multiple start entries'
                is_valid = False

            if not is_valid:
                call_details_it = CallDetails()
                call_details_it.set_invalid_msg(invalid_msg)
                call_details_list.append(call_details_it)
                continue

            source = start_call_signal.values('source')[0]['source']
            destination = start_call_signal.values('destination')[0]['destination']
            start = start_call_signal.values('timestamp')[0]['timestamp']

            end_call_signal = CallRecordSignalSnippet.objects.filter(
                call_id=i,
                callType='End'
            )
            if end_call_signal.count() == 1:
                end = end_call_signal.values('timestamp')[0]['timestamp']
                is_valid = True
            elif end_call_signal.count() == 0:
                invalid_msg = 'Unfinished call'
                is_valid = False
            else:
                invalid_msg = 'Invalid signal pair - multiple end entries'
                is_valid = False

            if is_valid:
                if start > end:
                    invalid_msg = 'Invalid signal pair - call must start '\
                                  + 'before it ends!'
                    is_valid = False

            if not is_valid:
                call_details_it = CallDetails()
                call_details_it.set_invalid_msg(invalid_msg)
                call_details_list.append(call_details_it)
                continue

            call_details_it = CallDetails()
            call_details_it.set_values(i, start, end, source, destination)
            call_details_it.set_valid()
            call_details_list.append(call_details_it)

        return call_details_list

    def calculate_bill(self, call_details_list):

        standard_call_charge_time = 6
        reduced_call_charge_time = 22
        standard_call_charge_hourly = 0.09
        reduced_call_charge_hourly = 0
        standing_charge = 0.36

        for it in call_details_list:
            if it.is_valid():
                price = standing_charge
                time = 0
                time_iterator = it.get_start()
                time_stop = it.get_end()
                day_iterator = 0
                i = 0
                while time_iterator < time_stop:
                    if time_iterator.day == time_stop.day:
                        if time_iterator.hour < standard_call_charge_time:
                            aux_call_charge = reduced_call_charge_hourly
                            if time_stop.hour < standard_call_charge_time:
                                aux_call_charge_hour = time_stop.hour
                                aux_call_charge_minute = time_stop.minute
                            else:
                                aux_call_charge_hour = standard_call_charge_time
                                aux_call_charge_minute = 0
                        elif time_iterator.hour < reduced_call_charge_time:
                            aux_call_charge = standard_call_charge_hourly
                            if time_stop.hour < reduced_call_charge_time:
                                aux_call_charge_hour = time_stop.hour
                                aux_call_charge_minute = time_stop.minute
                            else:
                                aux_call_charge_hour = reduced_call_charge_time
                                aux_call_charge_minute = 0
                        else:
                            aux_call_charge = reduced_call_charge_hourly
                            aux_call_charge_hour = time_stop.hour
                            aux_call_charge_minute = time_stop.minute
                    else:
                        if time_iterator.hour < standard_call_charge_time:
                            aux_call_charge = reduced_call_charge_hourly
                            aux_call_charge_hour = standard_call_charge_time
                        elif time_iterator.hour < reduced_call_charge_time:
                            aux_call_charge = standard_call_charge_hourly
                            aux_call_charge_hour = reduced_call_charge_time
                        else:
                            aux_call_charge = reduced_call_charge_hourly
                            aux_call_charge_hour = 0
                            day_iterator += 1
                        aux_call_charge_minute = 0

                    i += 1
                    if i > 1000:
                        msg = 'call too long to calculate bill'
                        it.set_invalid_msg(msg)
                        break

                    time_aux = datetime(
                        it.get_start().year,
                        it.get_start().month,
                        it.get_start().day,
                        aux_call_charge_hour,
                        aux_call_charge_minute,
                        0,
                        0,
                        self.tz
                    )
                    time_aux += timedelta(days=day_iterator)

                    if time_aux > time_stop:
                        time_aux = time_stop

                    aux_delta_time = time_aux - time_iterator
                    aux_delta_time_minutes = aux_delta_time.seconds / 60
                    price += aux_call_charge * aux_delta_time_minutes
                    time += aux_delta_time.seconds
                    time_iterator = time_aux
                it.set_call_price(price)
                it.set_call_time(time)
            else:
                continue
