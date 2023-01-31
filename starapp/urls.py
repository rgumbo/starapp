from django.urls import path, include
from . import views

#URLCONFIG
urlpatterns = [
    path('', views.index, name='index'),

#    path('homepage', views.HomePageView, name='homepage'),
    path('homeindex', views.HomeIndexView, name='homeindex'),

    path('addperiod', views.PeriodView, name='addperiod'),
    path('perioddetail/<str:pk>/', views.PeriodDetailView.as_view(), name='perioddetail'),
    path('editperiod/<str:pk>/', views.EditPeriod, name='editperiod'),
    path('period/', views.PeriodIndexView.as_view(), name='period'),
    path('deleteperiod/<str:pk>/', views.DeletePeriod, name='deleteperiod'),

    path('addgroups', views.GroupTabView, name='addgroups'),
    path('groupsdetail/<str:pk>/', views.GroupTabDetailView.as_view(), name='groupsdetail'),
    path('editgroups/<str:pk>/', views.EditGroupTab, name='editgroups'),
    path('groups/', views.GroupIndexView.as_view(), name='groups'),
    path('deletegroups/<str:pk>/', views.DeleteGroupTab, name='deletegroups'),

    path('addmembers', views.MemberView, name='addmembers'),
    path('membersdetail/<str:pk>/', views.MemberDetailView.as_view(), name='membersdetail'),
    path('editmembers/<str:pk>/', views.EditGroupMember, name='editmembers'),
    path('members/', views.MemberIndexView.as_view(), name='members'),
    path('deletemembers/<str:pk>/', views.DeleteMember, name='deletemembers'),

# Member payments
    path('contlist', views.ContListView, name='contlist'),
    path('memberpay/<int:mr_num>/<int:mr_period>/<int:gm_num>/<int:gr_num>/(?P<amount>\d+\.\d({2})/$',views.MemberPayView, name='memberpay'),

    #Generate member contributions
    path('gencont', views.GenContView.as_view(), name='gencont'),

#Generate member transactions
    path('gentrans', views.GenTransView.as_view(), name='gentrans'),

    path('addadvances', views.AdvanceView, name='addadvances'),
    path('advancesdetail/<str:pk>/', views.AdvanceDetailView.as_view(), name='advancesdetail'),
    path('editadvances/<str:pk>/', views.EditAdvance, name='editadvances'),
    path('advances/', views.AdvanceIndexView.as_view(), name='advances'),
    path('deleteadvances/<str:pk>/', views.DeleteAdvance, name='deleteadvances'),

#Reports
    path('g_position', views.g_position, name='g_position'),
    path('g_position_tab', views.TransHTMxTableView1.as_view(), name='g_position_tab'),
    path('g_position_tab1', views.TransHTMxTableView.as_view(), name='g_position_tab1'),
    path('memberrecord_htmx', views.TransHTMxTable1, name='memberrecord_htmx'),

#Blog App
    path('bloghome', views.PostList.as_view(), name='bloghome'),
    path('blogadmin', views.PostListAdmin.as_view(), name='blogadmin'),
    path('post_detail/<slug>/', views.Post_Detail, name='post_detail'),
    path('post_new/', views.post_new, name='post_new'),
    # path('post/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post_edit/<slug>/', views.post_edit, name='post_edit'),
    path('post_remove/<slug>/', views.post_remove, name='post_remove'),
    path('cont_approve/<int:pk>/', views.cont_approve, name='cont_approve'),
    path('cont_remove/<int:pk>/', views.cont_remove, name='cont_remove'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
  ]
