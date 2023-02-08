# app super user is admin

from django.contrib import admin
from django.db import models
#from import_export.admin import ImportExportModelAdmin

# Register your models here.

from .models import Period, GroupTab, GroupMember, MemberRecord, Receipt, Fund, Advance, BlogPost\
    , InterestRecord, PostContribution,PostCategory,PostOrigin,PostContribution

#Start StarApp Admin Config

# Define the Period admin class
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('pr_num','pr_from_date','pr_to_date','pr_due_date','pr_status','pr_proc_status','pr_int_rate',
                    'pr_amount')

# Register the Period admin class with the associated model
admin.site.register(Period, PeriodAdmin)

# Define the GroupTab admin class
class GroupTabAdmin(admin.ModelAdmin):
    list_display = ('gr_num','gr_code','gr_name','gr_cat','gr_status','gr_contact','gr_mobile','gr_email')

# Register the GroupTab admin class with the associated model
admin.site.register(GroupTab, GroupTabAdmin)

# Define the GroupMember admin class
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('gm_num','gm_gr_num','gm_ref','gm_fname','gm_initials','gm_nid','gm_sname','gm_date_joined',
                'gm_cat','gm_units','gm_status','gm_contact','gm_mobile','gm_email','gm_address_1',
                    'gm_address_2','gm_address_3')

# Register the GroupMember admin class with the associated model
admin.site.register(GroupMember, GroupMemberAdmin)

# Define the MemberRecord admin class
class MemberRecordAdmin(admin.ModelAdmin):
    list_display = ('mr_num','mr_gr_num','mr_gm_num','mr_period','mr_trans_date','mr_value_date','mr_due_date',
                    'mr_pamount','mr_aamount','mr_units','mr_pay_ref','mr_dr_cr','mr_paid','mr_status',
                    'mr_processed','mr_pay_type')

# Register the MemberRecord admin class with the associated model
admin.site.register(MemberRecord, MemberRecordAdmin)

# Define the Receipt admin class
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('rc_num','rc_gr_num','rc_gm_num','rc_mr_num1','rc_period','rc_trans_date','rc_value_date','rc_due_date',
			'rc_pamount','rc_aamount','rc_pay_ref','rc_dr_cr','rc_paid','rc_status','rc_processed','rc_pay_type')

# Register the Receipt admin class with the associated model
admin.site.register(Receipt, ReceiptAdmin)

# Define the Fund admin class
class FundAdmin(admin.ModelAdmin):
    list_display = ('fd_num','fd_period','fd_trans_date','fd_pamount','fd_aamount','fd_pay_ref','fd_paid',
                    'fd_source','fd_status','fd_processed')

# Register the Fund admin class with the associated model
admin.site.register(Fund, FundAdmin)

# Define the Advance admin class
class AdvanceAdmin(admin.ModelAdmin):
    list_display = ('av_num','av_gm_num','av_period','av_trans_date','av_value_date','av_due_date','av_ramount',
			'av_aamount','av_repay_plan','av_pay_ref','av_disb','av_status','av_processed','av_pay_type')

# Register the Advance admin class with the associated model
admin.site.register(Advance, AdvanceAdmin)

# Define the Interest Record admin class
class InterestRecordAdmin(admin.ModelAdmin):
    list_display = ('ir_num','ir_gr_num','ir_gm_num','ir_av_num','ir_period','ir_trans_date','ir_from_date','ir_to_date',
'ir_int_bal','ir_balance','ir_days','ir_pay_ref','ir_category','ir_paid','ir_status','ir_processed')

# Register the GroupMember admin class with the associated model
admin.site.register(InterestRecord, InterestRecordAdmin)

# Block Models admin registration Start here
# Define the PostCategory admin class
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('ct_code','ct_desc','ct_seo_title','ct_seo_desc','slug')

# Register the admin class with the PostCategory model
admin.site.register(PostCategory, PostCategoryAdmin )

# Define the PostOrigin admin class
class PostOriginAdmin(admin.ModelAdmin):
    list_display = ('po_num','po_name','po_position')

# Register the admin class with the PostOrigin model
admin.site.register(PostOrigin, PostOriginAdmin)

# Define the BlogPost admin class
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('bp_heading', 'slug', 'bp_status','bp_date')
    list_filter = ("bp_status",)
    search_fields = ['bp_heading', 'bp_body']
    prepopulated_fields = {'slug': ('bp_heading',)}

# Register the admin class with the BlogPost model
admin.site.register(BlogPost, BlogPostAdmin)

# Define the PostContribution admin class
class PostContributionAdmin(admin.ModelAdmin):
    list_display = ('pc_contributor', 'pc_contribution', 'pc_bp_num', 'ad_date_c', 'pc_active')
    list_filter = ('pc_active', 'ad_date_c')
    search_fields = ('pc_contributor', 'pc_email', 'pc_contribution')
    actions = ['approve_contributions']

    def approve_contributions(self, request, queryset):
        queryset.update(pc_active=True)

# Register the admin class with the PostContribution model
admin.site.register(PostContribution, PostContributionAdmin)
