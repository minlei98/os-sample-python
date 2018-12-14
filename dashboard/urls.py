# from django.conf.urls import url
# from . import views
#  
# urlpatterns = [
#         url(r'^$', views.index, name='index'),
# ]

from django.conf.urls import url, include
from rest_framework import routers
from . import views
from . import reports
from django.urls import path


#from rest_framework.schemas import get_schema_view
#router.register(r'qscenario', views.QueryForScenarioViewSet)
#schema_view = get_schema_view(title='MPQE API')

urlpatterns = [
    

     url(r'^home', views.home, name='home'),
     url(r'^report/bar', reports.bar_chart, name='bar_chart'),
     url(r'^report/sbar1', reports.bar_stack_chart1, name='bar_stack_chart1'),
     url(r'^report/sbar', reports.bar_stack_chart, name='bar_stack_chart'),
     
     url(r'^report/pstacks', reports.product_stack_chart, name='product_stack_chart'),
     
     
     url(r'^report/line', reports.line_chart, name='line_chart'),
     url(r'^report/mline', reports.multi_line_chart, name='multi_line_chart'),
     url(r'^report/pie', reports.pie_chart, name='pie_chart'),
     url(r'^report/pie1', reports.pie_chart1, name='pie_chart1'),

     url(r'^report/meter', reports.meter_chart, name='meter_chart'),     
     url(r'^report/recipes', reports.recipes_chart, name='recipes_chart'), 
     url(r'^report/runs', reports.runs_chart, name='runs_chart'), 
     url(r'^report', reports.report, name='report'),
     
          
     #url(r'^schema/$', schema_view),
     url(r'^$', views.index, name='index'),
     url(r'^line', views.index, name='index'),
          
] 

