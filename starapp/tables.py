# products/tables.py
import django_tables2 as tables
from starapp.models import MemberRecord

class TransHTMxTable(tables.Table):
    class Meta:
        model = MemberRecord
        template_name = "tables/bootstrap_htmx.html"
