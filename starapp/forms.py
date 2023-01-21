from django import forms
from django.forms import ModelForm
from .models import Period, GroupTab, GroupMember, MemberRecord, Receipt, Fund, Advance, AdvanceTrans
#from bootstrap_datepicker_plus import DatePickerInput  #, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
#from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Submit, Row, Column
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


#from django.db import models

#Start pachena Forms

# creating the Period form
class PeriodForm(forms.ModelForm):
	class Meta:
		model = Period
		fields = ['pr_num','pr_from_date','pr_to_date','pr_due_date','pr_status','pr_proc_status','pr_int_rate',
				  'pr_amount']
		widgets = {
			# 'pr_start_date': DatePickerInput(),
			# 'pr_end_date': DatePickerInput(),
			'pr_from_date': DateTimePickerInput(),
			'pr_to_date': DateTimePickerInput(),
			'pr_due_date': DateTimePickerInput(),
		}

		# creating the GroupTab form
class GroupTabForm(forms.ModelForm):
	class Meta:
		model = GroupTab
		fields = ['gr_num','gr_code','gr_name','gr_cat','gr_status','gr_contact','gr_mobile','gr_email']

# creating the GroupMember form
class GroupMemberForm(forms.ModelForm):
	class Meta:
		model = GroupMember
		fields = ['gm_num','gm_gr_num','gm_ref','gm_fname','gm_initials','gm_nid','gm_sname','gm_date_joined','gm_cat',
				  'gm_status','gm_contact','gm_mobile','gm_email','gm_address_1','gm_address_2','gm_address_3']
		widgets = {
			# 'pr_start_date': DatePickerInput(),
			# 'pr_end_date': DatePickerInput(),
			'gm_date_joined': DateTimePickerInput(),
			#'pr_to_date': DateTimePickerInput(),
			#'pr_due_date': DateTimePickerInput(),
		}

# creating the MemberRecord form
class MemberRecordForm(forms.ModelForm):
	class Meta:
		model = MemberRecord
		fields = ['mr_num','mr_gr_num','mr_gm_num','mr_period','mr_trans_date','mr_value_date','mr_due_date','mr_pamount',
			'mr_aamount','mr_units','mr_pay_ref','mr_dr_cr','mr_paid','mr_status','mr_processed','mr_pay_type']
		widgets = {
			'mr_trans_date': DateTimePickerInput(),
			'mr_value_date': DateTimePickerInput(),
			'pr_due_date': DateTimePickerInput(),
		}

# creating the Receipt form
class ReceiptForm(forms.ModelForm):
	class Meta:
		model = Receipt
		fields = ['rc_num','rc_period','rc_gr_num','rc_gm_num','rc_mr_num','rc_trans_date',
			'rc_aamount','rc_pay_ref','rc_dr_cr','rc_paid','rc_status','rc_processed','rc_pay_type']
		widgets = {
			'rc_trans_date': DateTimePickerInput(),
		}

# creating the Fund form
class FundForm(forms.ModelForm):
	class Meta:
		model = Fund
		fields = ['fd_num','fd_period','fd_trans_date','fd_pamount','fd_aamount','fd_pay_ref','fd_paid',
				  'fd_source','fd_status','fd_processed']

# creating the Advance form
class AdvanceForm(forms.ModelForm):
	class Meta:
		model = Advance
		fields = ['av_num','av_gr_num','av_gm_num','av_period','av_trans_date','av_value_date','av_due_date','av_ramount',
			'av_aamount','av_repay_plan','av_pay_ref','av_disb','av_status','av_processed','av_pay_type']
		widgets = {
			'av_trans_date': DateTimePickerInput(),
			'av_value_date': DateTimePickerInput(),
			'av_due_date': DateTimePickerInput(),
		}

class PayListForm(forms.Form):
		cat_choices = (("1", "Contributions"), ("2", "Advances"))
		pr_period = forms.CharField(max_length=10, help_text='Enter the period you want to run for')
		trans_cat = forms.ChoiceField(choices=cat_choices,help_text='Transaction Category')

class GenContForm(forms.Form):
		comm_choices = (("Y", "Proceed"), ("N", "Stop"))
		Gen_ok = forms.ChoiceField(choices=comm_choices)
		f_period = forms.IntegerField()

class GenTransForm(forms.Form):
	comm_choices = (("Y", "Proceed"), ("N", "Stop"))
	Gen_ok = forms.ChoiceField(choices=comm_choices)
	f_period = forms.IntegerField()

# Start Blog forms

# Start Interactions Form
from django.db import models
#from django import forms
from .models import PostCategory, PostOrigin,BlogPost,PostContribution

#from .models import PostContribution
#from django import forms

from django import forms
#from .models import BlogPost, PostContribution

class PostCategoryForm(forms.Form):
    ct_code = models.CharField(verbose_name='Code', max_length=10, help_text='Enter code uniquely identifying post category')
    ct_desc = models.CharField(max_length=50, blank=True, null=True, help_text='The description of the category')

class PostOriginForm(forms.Form):
    po_num = models.CharField(verbose_name='Code', max_length=10, help_text='Enter code uniquely identifying originator of the post')
    po_name = models.CharField(max_length=100, blank=True, null=True, help_text='The name of the originator')
    po_position = models.CharField(max_length=50, blank=True, null=True, help_text='The position/title of the originator')

class BlogPostForm(forms.Form):
    bp_choices = (('D', 'Draft'), ('R', 'Peered'), ('P', 'Publish'))
    bp_num = models.AutoField(verbose_name='Post Number',help_text='Number uniquely identifying the post')
    bp_ct_code = models.ForeignKey(PostCategory, on_delete=models.CASCADE,verbose_name='Category', help_text='Category into which this post falls')
    bp_po_num = models.ForeignKey(PostOrigin, on_delete=models.CASCADE,verbose_name='Originator', help_text='The originator of the post')
    bp_heading = models.CharField(verbose_name='Heading',max_length=100, help_text='The heading of the post')
    bp_date = models.DateTimeField(auto_now_add=True, help_text='Date on which this post was created')
    bp_body = models.TextField(verbose_name='Message',max_length=200, help_text='The post s message')
    bp_status = models.CharField(verbose_name='Status',max_length=1, choices=bp_choices, help_text='Enter the status of the post')
    bp_file = models.FileField(upload_to='media/', verbose_name = 'Choose File to upload',blank=True,null=True)
    bp_image = models.ImageField(upload_to='media/', verbose_name = 'Choose image to upload',blank=True,null=True)

class PostContributionForm(forms.Form):
    pc_num = models.AutoField(verbose_name='Contribution Number',primary_key=True, help_text='Number uniquely identifying the contribution')
    pc_bp_num = models.ForeignKey(BlogPost, on_delete=models.CASCADE,verbose_name='BlogPost', help_text='The of the post')
    pc_contribution = models.TextField(verbose_name='Contribution',max_length=350, help_text='The contribution to a post')

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('bp_ct_code','bp_po_num','bp_heading','bp_body','bp_status','bp_file','bp_image')

class ContributionForm(forms.ModelForm):
    class Meta:
        model = PostContribution
        fields = ('pc_contributor', 'pc_email', 'pc_contribution')
        #'pc_bp_num',
