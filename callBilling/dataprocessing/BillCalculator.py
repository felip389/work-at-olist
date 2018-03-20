from snippets.models import CallRecordSignalSnippet
import re
from datetime import datetime
from pytz import timezone


class BillCalculator:

    def getBill(self, source, year, month):
        call_ids = self.get_month_call_ids(source, year, month)

        

        return call_ids

    def get_month_call_ids(self, source, year, month):

        src_re = re.match(r'\d{10,11}', source)
        if src_re is None:
            return
        year_re = re.match(r'\d{4}', year)
        if year_re is None:
            return
        month_re = re.match(r'\d{1,2}', month)
        if month_re is None:
            return
        if month is 12:
            end_year = int(year) + 1
            end_month = 1
        else:
            end_year = int(year)
            end_month = int(month) + 1

        start_timestamp = datetime(int(year), int(month), 1, 0, 0, 0, 0,
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
            call_ids.append(
                source_call_signals.values('call_id')[i]['call_id'])
        return call_ids
