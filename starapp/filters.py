from django import forms
from .models import GroupMember, MemberRecord
import django_filters
#from decimal import Decimal
from django.db.models import Q

class MembContFilter(django_filters.FilterSet):

    class Meta:
        model = MemberRecord
        fields = ['mr_period', 'mr_category', 'mr_gm_num']

#Filter for table

# starapp/filters.py
class TransFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = MemberRecord
        fields = ['query']

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Integer(value)
            return MemberRecord.objects.filter(
                Q(mr_period=value) | Q(mr_units=value)
            )

        return MemberRecord.objects.filter(
            Q(mr_category__icontains=value) | Q(mr_dr_cr__icontains=value)
        )
