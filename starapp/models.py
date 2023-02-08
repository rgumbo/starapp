
	# Create your models here.
from django.db import models

	# Create your models here.
from django.db import models
	# from django import django.template.defaultfilters
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
#from slugify import slugify
from django.template.defaultfilters import slugify

	# Create your models here.

#Period Class - Table contains record of operating period
class Period(models.Model):
		pr_statuses = (('1', 'Open'), ('2', 'Close'))
		pr_process_choices = (('1', 'Processed'), ('2', 'Pending'))
		pr_num = models.IntegerField(verbose_name='Period', primary_key=True,help_text='User Assigned Period')
		pr_from_date = models.DateTimeField(verbose_name='From Date', help_text='Starting Date',null=True, blank=True)
		pr_to_date = models.DateTimeField(verbose_name='To Date', help_text='Ending Date',null=True, blank=True)
		pr_due_date = models.DateTimeField(verbose_name='Due Date', help_text='Due Date',null=True, blank=True)
		pr_status = models.CharField(verbose_name='Status', max_length=1, default='2' , choices=pr_statuses, help_text='The perioid s status')
		pr_proc_status = models.CharField(verbose_name='Processing Status', max_length=1, default='2' , choices=pr_process_choices, help_text='The group s status')
		pr_int_rate = models.DecimalField(verbose_name='Interest rate', max_digits=5, decimal_places=2, default=0, help_text='Applicable interest rate')
		pr_amount = models.DecimalField(verbose_name='Contribution Amount', max_digits=15, default=0, decimal_places=2, help_text='The amount members are expected to contribute in the period')
		pr_int_days = models.IntegerField(verbose_name='Interest Days', default=0,help_text='The umber of days to elapse before interest is charged')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')
		class Meta:
			ordering = ['pr_num']
			verbose_name = 'Period'
		def __str__(self):
			return self.pr_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.pr_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

# GroupTab Class - Table contains record of fund groups
class GroupTab(models.Model):
		gr_status = (('1', 'Application'), ('2', 'Activated'), ('3', 'Inactivated'))
		gr_cat_choices = (('1', 'Savings Club'), ('2', 'General Membership'), ('3', 'Congregational'), ('4', 'Others'))
		gr_num = models.AutoField(verbose_name='Number', primary_key=True,help_text='System generated number uniquely identifying a group')
		gr_code = models.CharField(verbose_name='Code', max_length=5, help_text='Assigned group identifying code')
		gr_name = models.CharField(verbose_name='Name', max_length=100, help_text='The group s name')
		gr_cat = models.CharField(verbose_name='Category', max_length=1, choices=gr_cat_choices, help_text='The group s category', null=True, blank=True)
		gr_status = models.CharField(verbose_name='Status', max_length=1, default='1' , choices=gr_status, help_text='The group s status', null=True, blank=True)
		gr_contact = models.CharField(verbose_name='Contact Person',max_length=50, help_text='Contact person', null=True, blank=True)
		gr_mobile = models.IntegerField(verbose_name='Mobile Number', help_text='Contact person mobile number', null=True, blank=True)
		gr_email = models.CharField(verbose_name='Email',max_length=50, help_text='Contact person email address', null=True, blank=True)
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

		class Meta:
			ordering = ['gr_num']
			verbose_name = 'Group ID'
		def __str__(self):
			return self.gr_name
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.gr_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#GroupMember Class - Table contains record of fund groups members
class GroupMember(models.Model):
		gm_status = (('1', 'Application'), ('2', 'Activated'), ('3', 'Inactivated'))
		gm_cat_choices = (('1', 'Member'), ('2', 'Borrower'), ('3', 'Type 3'), ('4', 'Type 4'))
		gm_num = models.AutoField(verbose_name='Number', primary_key=True,help_text='System generated number uniquely identifying a group member')
		gm_gr_num = models.ForeignKey(GroupTab, on_delete=models.CASCADE, verbose_name='Group', help_text='Group to which the member belongs')
		gm_ref = models.CharField(verbose_name='Reference', max_length=20, help_text='Member s reference')
		gm_fname = models.CharField(verbose_name='First Name', max_length=100, help_text='The member s first name')
		gm_initials = models.CharField(verbose_name='Initials', max_length=5, help_text='The member s initials')
		gm_nid = models.CharField(verbose_name='National identification Number', max_length=15, help_text='The member s national identification number')
		gm_sname = models.CharField(verbose_name='Surname', max_length=100, help_text='The member s surname')
		gm_date_joined = models.DateTimeField( help_text='Date member joined group',null=True, blank=True)
		gm_cat = models.CharField(verbose_name='Category', max_length=1, choices=gm_cat_choices, help_text='The member s category', null=True, blank=True)
		gm_units = models.IntegerField(verbose_name='Units Held',default=1, help_text='The number of units held')
		gm_status = models.CharField(verbose_name='Status', default='1' ,max_length=1,  choices=gm_status, help_text='The member s status', null=True, blank=True)
		gm_contact = models.CharField(verbose_name='Contact Person',max_length=50, help_text='Contact person', null=True, blank=True)
		gm_mobile = models.IntegerField(verbose_name='Mobile Number', help_text='Contact person mobile number', null=True, blank=True)
		gm_email = models.CharField(verbose_name='Email',max_length=150, help_text='Contact person email address', null=True, blank=True)
		gm_address_1 = models.CharField(verbose_name='Address 1',max_length=150, help_text='Member address 1', null=True, blank=True)
		gm_address_2 = models.CharField(verbose_name='Address 2',max_length=150, help_text='Member address 2', null=True, blank=True)
		gm_address_3 = models.CharField(verbose_name='Address 3',max_length=150, help_text='Member address 3', null=True, blank=True)
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

		class Meta:
			ordering = ['gm_num']
			verbose_name = 'Member'
		def __str__(self):
			return self.gm_sname + '-' + self.gm_fname
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.gm_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#MemberRecord Class - Table contains record of fund groups members transctions
class MemberRecord(models.Model):
		mr_status_choices = (('1', 'Live'), ('2', 'Reversed'), ('3', 'Cancelled'))
		mr_cat_choices = (('1', 'Contributions'), ('2', 'Advances'),('3', 'Interest'),('4', 'Penalties'),('G', 'General'))
		mr_pay_choices = (('1', 'Cheque'), ('2', 'Transfer'), ('3', 'Cash'), ('4', 'Mobile Money'))
		mr_num = models.AutoField(verbose_name='Number', primary_key=True, help_text='System generated number uniquely identifying a group member transaction')
		mr_gr_num = models.ForeignKey(GroupTab, on_delete=models.CASCADE, verbose_name='Group', help_text='Group to which the member belongs')
		mr_gm_num = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='member', verbose_name='Member', help_text='The member belongs')
		mr_period = models.IntegerField(verbose_name='Period', help_text='Period in which transaction occurred')
		mr_trans_date = models.DateTimeField(verbose_name='Transaction Date', help_text='Transaction Date')
		mr_value_date = models.DateTimeField(verbose_name='Value Date', help_text='Transaction s value date',  blank=True, null=True)
		mr_due_date = models.DateTimeField(verbose_name='Due Date', help_text='Transaction s due date',  blank=True, null=True)
		mr_pamount = models.DecimalField(verbose_name='Projected Amount', max_digits=15, default=0, decimal_places=2, help_text='The projected transaction amount')
		mr_aamount = models.DecimalField(verbose_name='Actual Amount', max_digits=15, default=0, decimal_places=2, help_text='The actual transaction amount')
		mr_units = models.IntegerField(verbose_name='Units Held',default=1, help_text='The number of units held')
		mr_pay_ref = models.CharField(verbose_name='Payment Ref',   blank=True, null=True, max_length=20, help_text='The payment reference')
		mr_category = models.CharField(verbose_name='Category', max_length=1, default='1',choices=mr_cat_choices, help_text='Indicates the status of the transaction')
		mr_dr_cr = models.CharField(verbose_name='Debit/Credit', max_length=1, default='D', help_text='The Transaction is a debit or a credit')
		mr_paid = models.CharField(verbose_name='Paid', max_length=1, help_text='Indicates payment in settlement for this transaction', default='N')
		mr_status = models.CharField(verbose_name='Status',default='1', max_length=1, choices=mr_status_choices, help_text='Indicates the status of the transaction')
		mr_processed = models.CharField(verbose_name='Processed', max_length=1, help_text='Indicates transaction has been processed', default='N')
		mr_pay_type = models.CharField(verbose_name='Payment Type',blank=True, null=True, max_length=1, choices=mr_pay_choices, help_text='Payment type', default='N')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, blank=True, null=True,help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, blank=True, null=True,help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

		class Meta:
			ordering = ['mr_num']
			verbose_name = 'Member Record'
		def __str__(self):
			return self.mr_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.mr_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#Receipt Class - Table contains record of receipt for a payment
class Receipt(models.Model):
		rc_status_choices = (('1', 'Live'), ('2', 'Reversed'), ('3', 'Cancelled'))
		rc_proc_choices = (('1', 'Pending'), ('2', 'Processed'))
		rc_pay_choices = (('1', 'Cheque'), ('2', 'Transfer'), ('3', 'Cash'), ('4', 'Mobile Money'))
		rc_num = models.AutoField(verbose_name='Number', primary_key=True, help_text='System generated number uniquely identifying a receipt')
		rc_gr_num = models.ForeignKey(GroupTab, on_delete=models.CASCADE, verbose_name='Group', help_text='Group to which the member belongs')
		rc_gm_num = models.ForeignKey(GroupMember, on_delete=models.CASCADE, verbose_name='Member', help_text='The member belongs')
		#rc_mr_num = models.ForeignKey(MemberRecord, related_name='memb_trans',on_delete=models.CASCADE, verbose_name='Member Record', help_text='The member transaction')
		rc_mr_num1 = models.CharField(verbose_name='Member Record',max_length=20, default=0, help_text='The member transaction to which funds to be applied')
		rc_period = models.IntegerField(verbose_name='Period', help_text='Period in which transaction occurred')
		rc_trans_date = models.DateTimeField(verbose_name='Transaction Date', help_text='Transaction Date')
		rc_value_date = models.DateTimeField(verbose_name='Value Date', help_text='Transaction s value date',  blank=True, null=True)
		rc_due_date = models.DateTimeField(verbose_name='Due Date', help_text='Transaction s due date',  blank=True, null=True)
		rc_pamount = models.DecimalField(verbose_name='Projected Amount', max_digits=15, default=0, decimal_places=2, help_text='The projected transaction amount')
		rc_aamount = models.DecimalField(verbose_name='Actual Amount', max_digits=15, default=0, decimal_places=2, help_text='The actual transaction amount')
		rc_balance = models.DecimalField(verbose_name='Balance', max_digits=15, default=0, decimal_places=2, help_text='The balance on the advance')
		rc_pay_ref = models.CharField(verbose_name='Payment Ref', max_length=20, help_text='The payment reference')
		rc_dr_cr = models.CharField(verbose_name='Debit/Credit', default='D',max_length=1, help_text='The Transaction is a debit or a credit')
		rc_paid = models.CharField(verbose_name='Paid', max_length=1, help_text='Indicates payment in settlement for this transaction', default='N')
		rc_status = models.CharField(verbose_name='Status',default='1', max_length=1, choices=rc_status_choices, help_text='Indicates the status of the transaction')
		rc_processed = models.CharField(verbose_name='Processed', max_length=1, choices=rc_proc_choices, help_text='Indicates transaction has been processed', default='N')
		rc_pay_type = models.CharField(verbose_name='Payment Type', max_length=1, choices=rc_pay_choices, help_text='Payment type', default='3')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

		class Meta:
			ordering = ['rc_num']
			verbose_name = 'Receipt'
		def __str__(self):
			return self.rc_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.rc_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#Fund Class - Table contains record amount put in the fund per period
class Fund(models.Model):
		fd_status = (('1', 'Available'), ('2', 'Committed'))
		fd_source_choices = (('1', 'Contributions'), ('2', 'Earnings'))
		fd_num = models.AutoField(verbose_name='Number', primary_key=True, help_text='System generated number uniquely identifying a fund')
		fd_period = models.IntegerField(verbose_name='Period', help_text='Period in which transaction occurred')
		fd_trans_date = models.DateTimeField(verbose_name='Transaction Date', help_text='Transaction Date')
		fd_pamount = models.DecimalField(verbose_name='Projected Amount', max_digits=15, default=0, decimal_places=2, help_text='The projected transaction amount')
		fd_aamount = models.DecimalField(verbose_name='Actual Amount', max_digits=15, default=0, decimal_places=2, help_text='The actual transaction amount')
		fd_pay_ref = models.CharField(verbose_name='Payment Ref', max_length=1, help_text='The payment reference')
		fd_paid = models.CharField(verbose_name='Paid', max_length=1, help_text='Indicates payment in settlement for this transaction', default='N')
		fd_status = models.CharField(verbose_name='Status', max_length=1, choices=fd_status, help_text='Indicates the status of the transaction')
		fd_processed = models.CharField(verbose_name='Processed', max_length=1, help_text='Indicates transaction has been processed', default='N')
		fd_source = models.CharField(verbose_name='Source', max_length=1, choices=fd_source_choices, help_text='Indicates source of funds', default='N')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

		class Meta:
			ordering = ['fd_num']
			verbose_name = 'Fund'
		def __str__(self):
			return self.fd_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.fd_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#Advance Class - Table contains record of advances to borrowers
class Advance(models.Model):
		av_status = (('1', 'Applied'), ('2', 'Approved'), ('3', 'Declined'))
		av_disb_choices = (('1', 'Pending'), ('2', 'Disbursed'))
		av_pay_choices = (('1', 'Cheque'), ('2', 'Transfer'), ('3', 'Cash'), ('4', 'Mobile Money'))
		av_proc_choices = (('1', 'Pending'), ('2', 'Processed'))
		av_num = models.AutoField(verbose_name='Number', primary_key=True, help_text='System generated number uniquely identifying a receipt')
		av_gm_num = models.ForeignKey(GroupMember, related_name='a_member',on_delete=models.CASCADE, verbose_name='Member', help_text='The member advanced money')
		av_gr_num = models.ForeignKey(GroupTab, related_name='a_group',on_delete=models.CASCADE, verbose_name='Group',default=1, help_text='The member s group')
		av_period = models.IntegerField(verbose_name='Period', help_text='Period in which transaction occurred')
		av_trans_date = models.DateTimeField(verbose_name='Transaction Date', help_text='Transaction Date')
		av_value_date = models.DateTimeField(verbose_name='Value Date', help_text='Transaction s value date',  blank=True, null=True)
		av_due_date = models.DateTimeField(verbose_name='Due Date', help_text='Transaction s due date',  blank=True, null=True)
		av_ramount = models.DecimalField(verbose_name='Requested Amount', max_digits=15, default=0, decimal_places=2, help_text='Requested amount')
		av_aamount = models.DecimalField(verbose_name='Advanced Amount', max_digits=15, default=0, decimal_places=2, help_text='Advanced amount')
		av_balance = models.DecimalField(verbose_name='Balance Amount', max_digits=15, default=0, decimal_places=2, help_text='Balance on the Advance')
		av_repay_plan = models.IntegerField(verbose_name='Repayment Plan', default=1, help_text='Repayment Plan')
		av_pay_ref = models.CharField(verbose_name='Payment Ref', max_length=20, help_text='The payment reference')
		av_disb = models.CharField(verbose_name='Disbursed ?', max_length=1, choices=av_disb_choices, help_text='Indicates advance waas disbursed' )
		av_status = models.CharField(verbose_name='Status', max_length=1, choices=av_status, help_text='Indicates the status of the advance')
		av_processed = models.CharField(verbose_name='Processed ?', max_length=1, choices=av_proc_choices, default='1', help_text='Indicates the processing status')
		av_pay_type = models.CharField(verbose_name='Payment Type', max_length=1, choices=av_pay_choices, help_text='Payment Type')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')
		class Meta:
			ordering = ['av_num']
			verbose_name = 'Advance'
		def __str__(self):
			return self.av_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.av_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

# Interest record class - maintains records for basis of charging interest
class InterestRecord(models.Model):
		ir_status_choices = (('1', 'Live'), ('2', 'Reversed'), ('3', 'Cancelled'))
		ir_cat_choices = (('1', 'Contributions'), ('2', 'Advances'), ('3', 'Interest'), ('4', 'Penalties'), ('G', 'General'))
		ir_num = models.AutoField(verbose_name='Number', primary_key=True, help_text='System generated number uniquely identifying an interest record')
		ir_gr_num = models.ForeignKey(GroupTab, on_delete=models.CASCADE, verbose_name='Group', help_text='Group to which the member belongs')
		ir_gm_num = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='memberint', verbose_name='Member', help_text='The member belongs')
		ir_av_num = models.IntegerField(verbose_name='Advance', blank=True,	null=True, help_text='The advance being recorded')
		ir_period = models.IntegerField(verbose_name='Period', help_text='Period in which transaction occurred')
		ir_trans_date = models.DateTimeField(verbose_name='Transaction Date', help_text='Transaction Date')
		ir_from_date = models.DateTimeField(verbose_name='From Date', help_text='Interest start date', blank=True,	null=True)
		ir_to_date = models.DateTimeField(verbose_name='To Date', help_text='Interest end date', blank=True, null=True)
		ir_int_bal = models.DecimalField(verbose_name='Int. Balance', max_digits=15, default=0, decimal_places=2, help_text='Balance on which interest is charged - Before payment')
		ir_balance = models.DecimalField(verbose_name='Actual Amount', max_digits=15, default=0, decimal_places=2, help_text='Balance - After payment')
		ir_days = models.IntegerField(verbose_name='Days', default=0, help_text='Number of days on to charge interest on')
		ir_pay_ref = models.CharField(verbose_name='Payment Ref', blank=True, null=True, max_length=20, help_text='The payment reference')
		ir_category = models.CharField(verbose_name='Category', max_length=1, default='1', choices=ir_cat_choices, help_text='Indicates the status of the transaction')
		ir_paid = models.CharField(verbose_name='Paid', max_length=1, help_text='Indicates payment in settlement for this transaction', default='N')
		ir_status = models.CharField(verbose_name='Status', default='1', max_length=1, choices=ir_status_choices, help_text='Indicates the status of the transaction')
		ir_processed = models.CharField(verbose_name='Processed', max_length=1,	help_text='Indicates transaction has been processed', default='N')
		ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
		ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
		ad_date_c = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text='Date record was created')
		ad_date_a = models.DateTimeField(auto_now=True, blank=True, null=True, help_text='Date record was last amended')
		ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
		ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
		ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
		ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')
		class Meta:
			ordering = ['ir_num']
			verbose_name = 'Interest Record'
		def __str__(self):
			return self.ir_status
		def get_absolute_url(self):
			return reverse('Index', args=[str(self.ir_num)])
		def get_post_url(self):
			return reverse('edit', kwargs={'pk': self.pk})

#Start Blog Models
class PostCategory(models.Model):
    ct_code = models.CharField(verbose_name='Code', max_length=10, primary_key=True,help_text='Enter code uniquely identifying post category')
    ct_desc = models.CharField(max_length=50, blank=True, null=True, help_text='The description of the category')
    ct_seo_title = models.CharField(verbose_name = 'SEO Title',max_length=300, blank=True, null=True, help_text='The SEO title of the blog')
    ct_seo_desc = models.CharField(verbose_name = 'SEO Description',max_length=250, blank=True, null=True, help_text='The SEO description of the blog')
    slug = models.SlugField(max_length=250, unique=True, help_text='The slug field for the blog for user facing title', blank=True)
    ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
    ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
    ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
    ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
    ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
    ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
    ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
    ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

    class Meta:
        ordering = ['ct_desc']
        verbose_name = 'Blog Category'

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.ct_desc)
        super(PostCategory, self).save(*arg, **kwargs)

    def __str__(self):
        return self.ct_desc

    def get_absolute_url(self):
        return reverse('IndexView', args=[str(self.ct_desc)])

    def get_post_url(self):
        return reverse('edit', kwargs={'pk': self.pk})

class PostOrigin(models.Model):
    po_num = models.CharField(verbose_name='Code', max_length=10, primary_key=True,help_text='Enter code uniquely identifying originator of the post')
    po_name = models.CharField(max_length=100, blank=True, null=True, help_text='The name of the originator')
    po_position = models.CharField(max_length=50, blank=True, null=True, help_text='The position/title of the originator')
    ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
    ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
    ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
    ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
    ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
    ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
    ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
    ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

    class Meta:
        ordering = ['po_name']
        verbose_name = 'PostOrigin'

    def __str__(self):
        return self.po_name

    def get_absolute_url(self):
        return reverse('IndexView', args=[str(self.po_name)])

    def get_post_url(self):
        return reverse('edit', kwargs={'pk': self.pk})

class BlogPost(models.Model):
    bp_choices = (('D', 'Draft'), ('R', 'Peered'), ('P', 'Publish'))
    bp_num = models.AutoField(verbose_name='Post Number',primary_key=True, help_text='Number uniquely identifying the post')
    bp_ct_code = models.ForeignKey(PostCategory, on_delete=models.CASCADE,verbose_name='Category', help_text='Category into which this post falls')
    bp_po_num = models.ForeignKey(PostOrigin, on_delete=models.CASCADE,verbose_name='Originator', help_text='The originator of the post')
    bp_heading = models.CharField(verbose_name='Heading',max_length=100, help_text='The heading of the post')
    bp_seo_title = models.CharField(verbose_name = 'SEO Title',max_length=300, blank=True, null=True, help_text='The SEO title of the blog')
    bp_seo_desc = models.CharField(verbose_name = 'SEO Description',max_length=250, blank=True, null=True, help_text='The SEO description of the blog')
    slug = models.SlugField(max_length=250, unique=True, help_text='The slug field for the blog for user facing title', blank=True)
    bp_date = models.DateTimeField(auto_now_add=True, help_text='Date on which this post was created')
    bp_body = models.TextField(verbose_name='Message',max_length=350, help_text='The post s message')
    bp_status = models.CharField(verbose_name='Status',max_length=1, choices=bp_choices, default='D', help_text='Enter the status of the post')
    bp_file = models.FileField(upload_to='media/', verbose_name='Attachment File', help_text = 'Choose File to upload',blank=True,null=True)
    bp_image = models.ImageField(upload_to='media/', verbose_name='Image', help_text='Choose image to upload',blank=True,null=True)
    ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The user creating the record')
    ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
    ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
    ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
    ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
    ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
    ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
    ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

    class Meta:
        ordering = ['bp_date']
        verbose_name = 'Blog Post'

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.bp_heading)
        super(BlogPost, self).save(*arg, **kwargs)

    def __str__(self):
        return self.bp_heading

    def get_absolute_url(self):
        #return reverse('Index', args=[str(self.bp_heading)])
        return reverse('index', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_post_url(self):
        return reverse('edit', kwargs={'pk': self.pk})

class PostContribution(models.Model):
    pc_num = models.AutoField(verbose_name='Contribution Number',primary_key=True, help_text='Number uniquely identifying the contribution')
    pc_bp_num = models.ForeignKey(BlogPost, on_delete=models.CASCADE,verbose_name='BlogPost', db_column='pc_bp_num', related_name='contributions', help_text='The Reference post for this contribution')
    pc_contribution = models.TextField(verbose_name='Contribution',max_length=350, help_text='The contribution to a post')
    pc_email = models.EmailField(verbose_name='Email', blank=True, null=True,help_text='The contributor s email')
    pc_contributor = models.CharField(verbose_name='Contributor',max_length=50, blank=True, null=True, help_text='The name of the contributor')
    pc_active = models.BooleanField(verbose_name='Accepted',default=False , help_text='Indicates whether contribution is accepted or not')
    ad_user_c = models.CharField(max_length=30, blank=True, null=True, help_text='The Creating record')
    ad_user_a = models.CharField(max_length=30, blank=True, null=True, help_text='The last amending user')
    ad_date_c = models.DateTimeField(auto_now_add=True, help_text='Date record was created')
    ad_date_a = models.DateTimeField(auto_now=True, help_text='Date record was last amended')
    ad_device_c = models.CharField(max_length=100, blank=True, null=True, help_text='The Device creating the record')
    ad_device_a = models.CharField(max_length=100, blank=True, null=True, help_text='The Last amending device')
    ad_ipadress_c = models.CharField(max_length=50, blank=True, null=True, help_text='The record creating ip address')
    ad_ipadress_a = models.CharField(max_length=50, blank=True, null=True, help_text='The last amending ip address')

    class Meta:
        ordering = ['ad_date_c']
        verbose_name = 'Contribution'

    def __str__(self):
        return self.pc_contribution

    def get_absolute_url(self):
        return reverse('Index', args=[str(self.pc_num)])

    def get_post_url(self):
        return reverse('edit', kwargs={'pk': self.pk})

    def approve_contributions(self):
        self.pc_active=True
        self.save()
