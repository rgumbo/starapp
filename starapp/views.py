from django.shortcuts import render, redirect
from .models import Period, GroupTab, GroupMember, MemberRecord, Receipt, Advance, AdvanceTrans,BlogPost\
    , PostContribution,PostCategory,PostOrigin,PostContribution
from .forms import PeriodForm, GroupTabForm, GroupMemberForm, MemberRecordForm, ReceiptForm, \
    AdvanceForm, PayListForm,GenContForm,GenTransForm,ContributionForm, BlogForm
from .filters import MembContFilter, TransFilter
from django.http import HttpResponse
from django_globals import globals
import json
import plotly.express  as px

#Imports for table
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import TransHTMxTable
import django_tables2 as tables


#End imports for table

import datetime
import csv, io
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View, generic
from django.db.models import Sum, F,Avg, Max, Min,Count,Q
from django.core.mail import EmailMessage

from django.views.generic import ListView, DetailView

from django.conf import settings
import csv,io
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Round

#from django.http import HttpResponse
import getpass
from os import environ, getcwd
from decimal import *

#def HomePageView(Request):
#    template = 'starnec/membspace/index.html'
#    context = {}

#    return render (Request, template, context)

def HomeIndexView(Request):
    template = 'homeindex.html'
    context = {}

    return render (Request, template, context)

# Create your views here.
def index(request):
    """View platform index and home page"""
    num_members = 0
    planned_c = 0
    cont_pending = 0
    tot_fund = 0
    contributions = 0
    earnings = 0
    advance = 0
    rep_amnt = 0

    # Count of members
    num_members = GroupMember.objects.all().count()

    # Contributions - Dues and Payments
    tot_cont = MemberRecord.objects.filter(mr_dr_cr='D',mr_category='1').aggregate(tot_cont=Sum('mr_pamount'))
    cont_pay = MemberRecord.objects.filter(mr_dr_cr='C',mr_category='1').aggregate(cont_pay=Sum('mr_aamount'))

    #Advances - Dues and Payments
    tot_adv = MemberRecord.objects.filter(mr_dr_cr='D',mr_category='2').aggregate(tot_adv=Sum('mr_pamount'))
    adv_pay = MemberRecord.objects.filter(mr_dr_cr='C',mr_category='2').aggregate(adv_pay=Sum('mr_aamount'))

    # Interest  - Dues and Payments
    tot_int = MemberRecord.objects.filter(mr_dr_cr='D',mr_category='3').aggregate(tot_int=Sum('mr_pamount'))
    int_pay = MemberRecord.objects.filter(mr_dr_cr='C',mr_category='3').aggregate(int_pay=Sum('mr_aamount'))

    # Penalties - Dues and Payments
    tot_pen = MemberRecord.objects.filter(mr_dr_cr='D',mr_category='3').aggregate(tot_pen=Sum('mr_pamount'))
    pen_pay = MemberRecord.objects.filter(mr_dr_cr='C',mr_category='3').aggregate(pen_pay=Sum('mr_aamount'))

    # Total receipts
    #tot_rec = pen_pay.pen_pay + int_pay.int_pay + adv_pay.adv_pay + cont_pay.cont_pay
    tot_rec = MemberRecord.objects.filter(mr_dr_cr='C').aggregate(tot_rec=Sum('mr_aamount'))

    # Value of Fund
    tot_fund = MemberRecord.objects.filter(mr_dr_cr='D').exclude(mr_category ='2').aggregate(tot_fund=Sum('mr_pamount'))

    context = {
        'num_members': num_members,
        'tot_cont': tot_cont,
        'cont_pay': cont_pay,
        'tot_adv': tot_adv,
        'adv_pay': adv_pay,
        'tot_int': tot_int,
        'int_pay': int_pay,
        'tot_pen': tot_pen,
        'pen_pay': pen_pay,
        'tot_rec': tot_rec,
        'tot_fund': tot_fund,
    }
    return render(request, 'index.html', context=context)

#Group Position View - Table implentation
class TransHTMxTableView(SingleTableMixin, FilterView):
    table_class = TransHTMxTable
    queryset = MemberRecord.objects.all()
    filterset_class = TransFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "starapp/member_record_partial.html"
        else:
            template_name = "starapp/member_record_htmx.html"

        return template_name

# This class will create the table just like how we create forms
class TransHTMxTable1(tables.Table):
   class Meta:
        model = MemberRecord
        fields = ('mr_num','mr_gm_num', 'mr_period','mr_trans_date', 'mr_units','mr_dr_cr',
              'mr_category','mr_pamount', 'mr_aamount')

# This View will render table
class TransHTMxTableView1(tables.SingleTableView):
   table_class = TransHTMxTable1
   queryset = MemberRecord.objects.all()
   template_name = "member_record.html"

# home view for Periods. Periods are displayed in a list
class PeriodIndexView(ListView):
    template_name = 'starapp/period/index.html'
    context_object_name = 'period_list'

    def get_queryset(self):
        return Period.objects.all()

# Detail view (view Period detail)
class PeriodDetailView(DetailView):
    model = Period
    template_name = 'starapp/period/period_detail.html'

# New Period view (Create new Period)
def PeriodView(request):
    if request.method == 'POST':
        form = PeriodForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('period')
    form = PeriodForm()
    return render(request, 'starapp/period/period.html', {'form': form})

# Edit a Period
def EditPeriod(request, pk, template_name='starapp/period/edit.html'):
    period = get_object_or_404(Period, pk=pk)
    form = PeriodForm(request.POST or None, instance=period)
    if form.is_valid():
        form.save()
        return redirect('period')
    return render(request, template_name, {'form': form})

# Delete Period
def DeletePeriod(request, pk, template_name='starapp/period/confirm_delete.html'):
    period = get_object_or_404(Period, pk=pk)
    if request.method == 'POST':
        period.delete()
        return redirect('period')
    return render(request, template_name, {'object': period})

# home view for the group. Groups are displayed in a list

class GroupIndexView(ListView):
    template_name = 'starapp/groups/index.html'
    context_object_name = 'GroupTab_list'

    def get_queryset(self):
        return GroupTab.objects.all()

# Detail view (view Group detail)
class GroupTabDetailView(DetailView):
    model = GroupTab
    template_name = 'starapp/groups/groups_detail.html'

# New Group view (Create new post)
def GroupTabView(request):
    if request.method == 'POST':
        form = GroupTabForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('groups')
    form = GroupTabForm()
    return render(request, 'starapp/groups/groups.html', {'form': form})

# Edit a Group
def EditGroupTab(request, pk, template_name='starapp/groups/edit.html'):
    grouptab = get_object_or_404(GroupTab, pk=pk)
    form = GroupTabForm(request.POST or None, instance=grouptab)
    if form.is_valid():
        form.save()
        return redirect('groups')
    return render(request, template_name, {'form': form})

# Delete GroupTab
def DeleteGroupTab(request, pk, template_name='starapp/groups/confirm_delete.html'):
    grouptab = get_object_or_404(GroupTab, pk=pk)
    if request.method == 'POST':
        GroupTab.delete()
        return redirect('groups')
    return render(request, template_name, {'object': grouptab})

# home view for Members. Members are displayed in a list

class MemberIndexView(ListView):
    template_name = 'starapp/members/index.html'

    context_object_name = 'Member_list'
    def get_queryset(self):
        return GroupMember.objects.all()

# Detail view (view Member detail)
class MemberDetailView(DetailView):
    model = GroupMember
    template_name = 'starapp/members/members_detail.html'

# New Member view (Create new post)
def MemberView(request):
    if request.method == 'POST':
        form = GroupMemberForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('members')
    form = GroupMemberForm()
    return render(request, 'starapp/members/members.html', {'form': form})

# Edit a Member
def EditGroupMember(request,pk, template_name='starapp/members/edit.html'):
    member = get_object_or_404(GroupMember, pk=pk)
    form = GroupMemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('members')
    return render(request, template_name, {'form': form})
def memb_new(request):
    if request.method == "POST":
        form = GroupMemberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.ad_user_c = request.user
            post.save()

            return redirect('members')
    else:
        form = GroupMemberForm()
    return render(request, 'starapp/members/post_edit.html', {'form': form})

def memb_edit(request, pk):
    post = get_object_or_404(GroupMember, pk=pk)
    if request.method == "POST":
        form = GroupMemberForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.ad_user_a = request.user
            post.save()
            return redirect('members', pk=post.pk)
    else:
        form = GroupMemberForm(instance=post)
    return render(request, 'starapp/members/post_edit.html', {'form': form,'post': post})

# Delete Member
def DeleteMember(request, pk, template_name='starapp/members/confirm_delete.html'):
    member = get_object_or_404(GroupMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('members')
    return render(request, template_name, {'object': member})

# Group member payment

def MembPayList(request):
    #payment_list = Receipt.objects.values('py_date','py_reference','py_mm_num__mm_name','py_ed_num','py_num','py_amount') #.filter(py_status='O')
    payment_list = MemberPayment1.objects.all()
    context = {'payment_list' : payment_list}

    return render(request, 'starapp/payments/paylist.html', context)

def SubmitPayView(request, pk, gm_num,gr_num):

    member = GroupMember.objects.get(gm_num = gm_num)
    memberdue = MemberRecord.objects.get(mr_num = pk)

    new_payment = None
    if request.method == 'POST':

        form = ReceiptForm(data=request.POST or None)

        if form.is_valid():

            # Create Receipt object but don't save to database yet
            new_payment = form.save(commit=False)
            new_payment.rc_mr_num = pk
            new_payment.rc_gm_num = gm_num
            new_payment.rc_gr_num = gr_num
            new_payment.rc_status = 'O'

            new_payment.py_user = request.user

            new_payment.save()
            messages.success(request,"Payment submitted successfully")
        return redirect('payment')
    else:
        form = ReceiptForm()
    return render(request, 'starapp/payments/submitpay.html', {'form': form,'new_payment': new_payment})
# Borrower payment

def MembReturnsSearch(request):
    ereturns_list = EmployerDues.objects.all().order_by('ed_period','ed_mm_num')
    #returns_filter = MembReturnsFilter(request.GET, queryset=ereturns_list)
    return render(request, 'starnec/membspace/members/necreturnslist.html', {'ereturns_list': ereturns_list })


def ContListView(request):

        total = 0
        cont_list = MemberRecord.objects.values('mr_num', 'mr_gr_num','mr_gm_num', 'mr_gm_num__gm_sname',
            'mr_gm_num__gm_fname','mr_period', 'mr_trans_date', 'mr_value_date', 'mr_due_date',
            'mr_pamount', 'mr_aamount', 'mr_units', 'mr_pay_ref', 'mr_dr_cr',
             'mr_paid', 'mr_status', 'mr_processed','mr_pay_type', 'mr_category').order_by('mr_period', 'mr_gm_num')
            #.filter(mr_period=pr_period, mr_category=trans_cat).order_by(
            #'mr_period', 'mr_gm_num')
        cont_list1 = MembContFilter(request.GET, queryset=cont_list)
        total = cont_list1.qs.aggregate(Total=Sum('mr_pamount'))

        context = {'filter': cont_list1,'total':total}

        return render(request, 'starapp/reports/cont_rpt1.html', context)

class ContListView1(ListView):
    template_name = 'starapp/reports/index.html'
    context_object_name = 'cont_list'

    def get_queryset(self):
        return MemberRecord.objects.values('mr_num', 'mr_gr_num', 'mr_gm_num', 'mr_period', 'mr_trans_date',
            'mr_value_date', 'mr_due_date','mr_pamount', 'mr_aamount', 'mr_units', 'mr_pay_ref', 'mr_dr_cr',
             'mr_paid', 'mr_status', 'mr_processed','mr_pay_type', 'mr_category').order_by('mr_period', 'mr_gm_num')

def MemberPayView(request, mr_num, mr_period, gm_num, gr_num, amount):
    context = {}
    # dictionary for initial data with field names as keys
    initial_dict = {"rc_mr_num1": mr_num,"rc_period": mr_period, "rc_gm_num":  gm_num, "rc_gr_num":gr_num,
                    "rc_pamount": amount,"rc_dr_cr": 'C'}

    # add the dictionary during initialization
    form = ReceiptForm(request.POST or None, initial = initial_dict)

    context['form'] = form
    template_name = 'starapp/payments/submitpay.html'

    if request.method == 'POST':
        #form = form(request.POST or None)
        if form.is_valid():
            f_gr_num = form.cleaned_data['rc_gr_num']
            f_gm_num = form.cleaned_data['rc_gm_num']
            f_period = form.cleaned_data['rc_period']
            f_trans_date = form.cleaned_data['rc_trans_date']
            f_pamount = form.cleaned_data['rc_pamount']
            f_aamount = form.cleaned_data['rc_aamount']
            f_mr_num1 = form.cleaned_data['rc_mr_num1']
            f_status = form.cleaned_data['rc_status']
            f_processed = form.cleaned_data['rc_processed']
            f_pay_type = form.cleaned_data['rc_pay_type']

            f_pamount = (f_pamount* -1)
            f_aamount = (f_aamount* -1)

            form.save()

            membdue = MemberRecord()
            membdue.mr_gr_num = f_gr_num
            membdue.mr_gm_num = f_gm_num
            membdue.mr_period = f_period
            membdue.mr_trans_date = f_trans_date
            membdue.mr_value_date = f_trans_date
            membdue.mr_due_date = f_trans_date
            membdue.mr_pamount = f_pamount
            membdue.mr_aamount = f_aamount
            membdue.mr_units = 0
            membdue.mr_pay_ref = f_mr_num1
            membdue.mr_category = 'G'
            membdue.mr_dr_cr = 'C'
            membdue.mr_paid = 'N'
            membdue.mr_status = f_status
            membdue.mr_processed = f_processed
            membdue.mr_pay_type = f_pay_type

            membdue.save()

            messages.success(request, "Payment submitted successfully")
            return redirect('contlist')
        else:
             form = ReceiptForm()
    return render(request, template_name, context)

# home view for Advance. Advance are displayed in a list
class AdvanceIndexView(ListView):
    template_name = 'starapp/advances/index.html'
    context_object_name = 'advance_list'

    def get_queryset(self):
        return Advance.objects.all()

# Detail view (view Advance detail)
class AdvanceDetailView(DetailView):
    model = Advance
    template_name = 'starapp/advances/advance_detail.html'

# NewAdvance view (Create new Fund)
def AdvanceView(request):
    form = AdvanceForm(request.POST)
    if request.method == 'POST':
        #form = AdvanceForm(request.POST)
        if form.is_valid():
            f_gr_num = form.cleaned_data['av_gr_num']
            f_gm_num = form.cleaned_data['av_gm_num']
            f_period = form.cleaned_data['av_period']
            f_trans_date = form.cleaned_data['av_trans_date']
            f_value_date = form.cleaned_data['av_value_date']
            f_due_date = form.cleaned_data['av_due_date']
            f_ramount = form.cleaned_data['av_ramount']
            f_aamount = form.cleaned_data['av_aamount']
            f_pay_ref = form.cleaned_data['av_pay_ref']
            f_status = form.cleaned_data['av_status']
            f_processed = form.cleaned_data['av_processed']
            f_pay_type = form.cleaned_data['av_pay_type']

            form.save()

            membdue = MemberRecord()
            membdue.mr_gr_num = f_gr_num
            membdue.mr_gm_num = f_gm_num
            membdue.mr_period = f_period
            membdue.mr_trans_date = f_trans_date
            membdue.mr_value_date = f_value_date
            membdue.mr_due_date = f_due_date
            membdue.mr_pamount = f_ramount
            membdue.mr_aamount = f_aamount
            membdue.mr_pay_ref = f_pay_ref
            membdue.mr_dr_cr = 'D'
            membdue.mr_paid = 'N'
            membdue.mr_status = f_status
            membdue.mr_category = '2'
            membdue.mr_processed = f_processed
            membdue.mr_pay_type = f_pay_type

            membdue.save()

            return redirect('advances')
        else:
            form = ReceiptForm()
    return render(request, 'starapp/advances/advance.html', {'form': form})

# Edit a Advance
def EditAdvance(request, pk, template_name='starapp/advances/edit.html'):
    advance = get_object_or_404(Advance, pk=pk)
    form = AdvanceForm(request.POST or None, instance=advance)
    if form.is_valid():
        form.save()
        return redirect('advances')
    return render(request, template_name, {'form': form})

# Delete Advance
def DeleteAdvance(request, pk, template_name='starapp/advances/confirm_delete.html'):
    advance = get_object_or_404(Advance, pk=pk)
    if request.method == 'POST':
        advance.delete()
        return redirect('advances')
    return render(request, template_name, {'object': advance})

# Views for Payment process

class LedgerListView(View):
        form_class = PayListForm
        template_name = 'starapp/payments/mainaccessl.html'

        def get(self, request, *args, **kwargs):
            form = self.form_class()
            return render(request, self.template_name, {'PayListForm': form})

        def post(self, request, *args, **kwargs):
            form_class = PayListForm
            form = self.form_class(request.POST)
            context = {'form': form}
            if form.is_valid():

                trans_cat = form.cleaned_data['trans_cat']
                pr_period = form.cleaned_data['trans_cat']

                cont_list = MemberRecord.objects.values('mr_num','mr_gr_num','mr_gm_num','mr_period','mr_trans_date','mr_value_date','mr_due_date',
                'mr_pamount','mr_aamount','mr_units','mr_pay_ref','mr_dr_cr','mr_paid','mr_status','mr_processed',
                'mr_pay_type','mr_category').filter(mr_period=pr_period, mr_category=trans_cat).order_by('mr_period','mr_gm_num')

            return render(request, 'starapp/payments/cont_rpt.html', {'cont_list' : cont_list})

class GenContView(View):
    form_class = GenContForm
    template_name = 'starapp/gendues/membdues.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'GenContForm': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            pr_num =  form.cleaned_data['f_period']
            pr_proc_status = form.cleaned_data['Gen_ok']

    #Loop through periods
            period_rec = Period.objects.filter(pr_status='1').order_by('pr_num')[:1]
            memb_list   =   GroupMember.objects.all()

            if period_rec :

                for pr in period_rec:

                    l_pr_num = pr.pr_num
                    l_pr_from_date = pr.pr_from_date
                    l_pr_to_date = pr.pr_to_date
                    l_pr_due_date = pr.pr_due_date
                    l_pr_status = pr.pr_status
                    l_pr_proc_status = pr.pr_proc_status
                    l_pr_int_rate = pr.pr_int_rate
                    l_pr_amount = pr.pr_amount

                for m_list in memb_list:
                    l_gm_num = m_list.gm_num
                    l_gm_gr_num = m_list.gm_gr_num
                    l_gm_units = m_list.gm_units
                    member = GroupMember.objects.get(pk=l_gm_num)
                    #m_group = GroupTab.objects.get(pk=l_gm_gr_num)

                    membdue = MemberRecord()
                    membdue.mr_gr_num = m_list.gm_gr_num
                    membdue.mr_gm_num = member #m_list.gm_num
                    membdue.mr_period = l_pr_num
                    membdue.mr_trans_date = l_pr_from_date
                    membdue.mr_value_date = l_pr_from_date
                    membdue.mr_due_date = l_pr_due_date
                    membdue.mr_pamount = (l_gm_units * l_pr_amount)
                    membdue.mr_aamount = 0
                    membdue.mr_units = l_gm_units
                    membdue.mr_pay_ref = 'P'
                    membdue.mr_dr_cr = 'D'
                    membdue.mr_paid = 'N'
                    membdue.mr_status = '1'
                    membdue.mr_processed = 'N'
                    membdue.mr_pay_type = 'P'

                    membdue.save()
                return redirect('contlist')

        return render(request, self.template_name, {'GenContForm': form})
class GenTransView(View):
    global l_pr_num
    global l_pr_from_date
    global l_pr_to_date
    global l_pr_due_date
    global l_pr_status
    global l_pr_proc_status
    global l_pr_int_rate
    global l_pr_amount

    form_class = GenTransForm
    template_name = 'starapp/gendues/membdues.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'GenContForm': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            pr_num =  form.cleaned_data['f_period']
            pr_proc_status = form.cleaned_data['Gen_ok']

    #Loop through periods
            period_rec = Period.objects.filter(pr_status='1').order_by('pr_num')[:1]
            rec_list	=	Receipt.objects.filter(rc_processed='1')
            adv_list	=	Advance.objects.filter(av_processed='1')

            for pr in period_rec:

                l_pr_num = pr.pr_num
                l_pr_from_date = pr.pr_from_date
                l_pr_to_date = pr.pr_to_date
                l_pr_due_date = pr.pr_due_date
                l_pr_status = pr.pr_status
                l_pr_proc_status = pr.pr_proc_status
                l_pr_int_rate = pr.pr_int_rate
                l_pr_amount = pr.pr_amount

    # Generating payments

            for r_list in rec_list:
                l_gm_num = r_list.rc_gm_num
                l_gm_gr_num = r_list.rc_gr_num
                l_amount = r_list.rc_aamount
                l_rc_num = r_list.rc_num

                pr = Period.objects.get(pr_num=pr_num)
                l_pr_num = pr.pr_num
                l_pr_from_date = pr.pr_from_date
                l_pr_to_date = pr.pr_to_date
                l_pr_due_date = pr.pr_due_date
                l_pr_status = pr.pr_status
                l_pr_proc_status = pr.pr_proc_status
                l_pr_int_rate = pr.pr_int_rate
                l_pr_amount = pr.pr_amount

                #member = GroupMember.objects.get(pk=r_list.rc_gm_num)
                #m_group = GroupTab.objects.get(pk=r_list.rc_gr_num)

                rec_update  = Receipt()
                membdue = MemberRecord()
                membdue.mr_gr_num = r_list.rc_gr_num
                membdue.mr_gm_num = r_list.rc_gm_num
                membdue.mr_period = l_pr_num
                membdue.mr_trans_date = l_pr_from_date
                membdue.mr_value_date = l_pr_from_date
                membdue.mr_due_date = l_pr_due_date
                membdue.mr_pamount = l_amount
                membdue.mr_aamount = l_amount
                membdue.mr_pay_ref = 'P'
                membdue.mr_category = 'G'
                membdue.mr_dr_cr = 'C'
                membdue.mr_paid = 'N'
                membdue.mr_status = '1'
                membdue.mr_processed = 'N'
                membdue.mr_pay_type = 'P'

                membdue.save()
                Receipt.objects.filter(rc_num=l_rc_num).update(rc_processed = '2')

  #Creating advance transactions
            for a_list in adv_list:
                    l_gm_num = a_list.av_gm_num
                    l_gm_gr_num = a_list.av_gr_num
                    l_amount = a_list.av_aamount
                    l_av_num = a_list.av_num
                    l_amount = (l_amount * -1)

                    pr = Period.objects.get(pr_num=pr_num)
                    l_pr_num = pr.pr_num
                    l_pr_from_date = pr.pr_from_date
                    l_pr_to_date = pr.pr_to_date
                    l_pr_due_date = pr.pr_due_date
                    l_pr_status = pr.pr_status
                    l_pr_proc_status = pr.pr_proc_status
                    l_pr_int_rate = pr.pr_int_rate
                    l_pr_amount = pr.pr_amount

                    #print(a_list.av_gr_num,a_list.av_gm_num,l_pr_num,l_amount)
                    membdue = MemberRecord()
                    membdue.mr_gr_num = a_list.av_gr_num
                    membdue.mr_gm_num = a_list.av_gm_num
                    membdue.mr_period = l_pr_num
                    membdue.mr_trans_date = l_pr_from_date
                    membdue.mr_value_date = l_pr_from_date
                    membdue.mr_due_date = l_pr_due_date
                    membdue.mr_pamount = l_amount
                    membdue.mr_aamount = l_amount
                    membdue.mr_pay_ref = 'P'
                    membdue.mr_dr_cr = 'D'
                    membdue.mr_paid = 'N'
                    membdue.mr_status = '1'
                    membdue.mr_category = '2'
                    membdue.mr_processed = 'N'
                    membdue.mr_pay_type = 'P'

                    membdue.save()
                    Advance.objects.filter(av_num=l_av_num).update(av_processed='2')
            return redirect('contlist')

        return render(request, self.template_name, {'GenTransForm': form})
def g_position(request):

        dataset = MemberRecord.objects.values('mr_period').annotate(
            cont_sum=Sum('mr_pamount', filter=Q(mr_category='1')),
            rec_sum=Sum('mr_pamount', filter=Q(mr_dr_cr ='C')),
            adv_sum=Sum('mr_aamount', filter=Q(mr_category='2'))) \
            .order_by('mr_period')

        periods = list()
        con_series_data = list()
        adv_series_data = list()
        rec_series_data = list()

        for entry in dataset:
            periods.append('%s Period' % entry['mr_period'])
            con = entry['cont_sum']
            if con is None:
                con = 0
            con = float(con)
            adv = entry['adv_sum']
            if adv is None:
                adv = 0
            adv = float(adv)
            rec = entry['rec_sum']
            if rec is None:
                rec = 0
            rec = float(rec)

            con_series_data.append(con)
            adv_series_data.append(adv)
            rec_series_data.append(rec)

        con_series = {
            'name': 'Contributions',
            'data': con_series_data,
            'color': 'purple'
        }

        adv_series = {
            'name': 'Advances',
            'data': adv_series_data,
            'color': 'red'
        }

        rec_series = {
            'name': 'Receipts',
            'data': rec_series_data,
            'color': 'green'
        }

        chart = {
            'chart': {'type': 'column'},
            'title': {'text': 'Group Financial Dashboard'},
            'xAxis': {'periods': periods},
            'series': [con_series, adv_series,rec_series]
        }

        dump = json.dumps(chart, cls=DecimalEncoder)

        return render(request, 'starapp/reports/charts/g_position.html', {'chart': dump})
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        #  if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

#Start Blog Views

#Start Commspace Views

class PostList(generic.ListView):

    queryset = BlogPost.objects.filter(bp_status='P').order_by('-ad_date_c')
    template_name = 'starapp/commspace/index.html'

    context_object_name = 'post_list'
    paginate_by = 20

class PostListAdmin(generic.ListView):

    queryset = BlogPost.objects.exclude(bp_status='P').order_by('-ad_date_c')
    template_name = 'starapp/commspace/index.html'

    context_object_name = 'post_list'
    paginate_by = 20

class PostDetail(generic.DetailView):
    model = BlogPost
    template_name = 'starapp/commspace/post_detail.html'

@login_required
def Post_Detail(request, slug):

    c_user = request.user
    print(c_user)

    template_name = 'starapp/commspace/post_detail.html'
    post = get_object_or_404(BlogPost, slug=slug)

    if request.user.username in ("reg","xx"):
        contributions = post.contributions.all()
        #print(c_user)
    else:
        contributions = post.contributions.filter(pc_active=True)
        print(request.user.username)

    new_contribution = None
    # Contribution posted
    if request.method == 'POST':
        contribution_form = ContributionForm(data=request.POST)

        if contribution_form.is_valid():

            # Create Contribution object but don't save to database yet
            new_contribution = contribution_form.save(commit=False)
            # Assign the current post to the Contribution
            new_contribution.pc_bp_num = post
            # Save the comment to the database
            new_contribution.save()
    else:
        contribution_form = ContributionForm()

    return render(request, template_name, {'post': post,
                                           'contributions': contributions,
                                           'new_contribution': new_contribution,
                                           'contribution_form': contribution_form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.ad_user_c = request.user
            post.save()

            return redirect('post_detail', slug=post.slug)
    else:
        form = BlogForm()
    return render(request, 'starapp/commspace/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.ad_user_a = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = BlogForm(instance=post)
    return render(request, 'starapp/commspace/post_edit.html', {'form': form,'post': post})

@login_required
def post_remove(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.delete()
    return redirect('bloghome')

@login_required
def cont_approve(request, pk):
    contribution = get_object_or_404(PostContribution, pk=pk)
    contribution.approve_contributions()
    return redirect('bloghome')

@login_required
def cont_remove(request, pk):
    contribution = get_object_or_404(PostContribution, pk=pk)
    contribution.delete()
    return redirect('bloghome')
