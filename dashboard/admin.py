from django.contrib import admin
from django.utils.html import format_html
from .models import Stack
from .models import Product
from .models import Run, MatrixOfProduct
from .models import Definition
from django.conf import settings
from datetime import timedelta, datetime, tzinfo

ZERO = timedelta(0)

# A UTC class.
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO    


class RunProxyAdmin(admin.ModelAdmin):

    # actions = None
    actions_on_top = True
    actions_on_bottom = True
    
    list_per_page = 50
        
    list_display = ('id',
                    'definition_id',
                    'product_stack_id',
                    'definition_test_type',
                    'run_status_',
                    'run_starttime',
                    'product_stack_contents',
                    )
    
    list_display_links = ('definition_id',
                             'product_stack_id',)
    
    # list_display_links = None
    
    list_editable = ()  
   
    # list_filter = (xRunProxyFilter,)
    
    list_filter = [
                    'definition__test_type',
                    'run_start',
                    'definition__ready_state',
                     'definition_id__product_stack__products__name',
                     #'definition_id__product_stack__products__version',
                     'definition_id__product_stack__products__arch',
                     ]
          
    
    search_fields = ('id',
                     'definition__name',
                     'definition__product_stack__name',
                     'definition__test_type',
                     'run_status',
                     'definition_id__product_stack__products__name',
                     'definition_id__product_stack__products__version',
                     'definition_id__product_stack__products__arch',)
    
    # readonly_fields = ()
    
    def get_queryset(self, request):
        queryset = MatrixOfProduct.objects.filter(run_status='COMPLETE' ).order_by('definition__name','definition__product_stack__name','-run_start').distinct('definition__name','definition__product_stack__name')    
        # for i in qs:
        #     print (i.id, i.solution.solution_name , i.solution.product_stack.stack_name,  i.solution.testtype)
        # print (qs.query)    
        return queryset
    
    
    

    def run_starttime(self, obj):
        formatedDate = obj.run_start.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate
    run_starttime.short_description = 'Start'
    
    def run_stoptime(self, obj):
        formatedDate = obj.run_stop.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate
    run_stoptime.short_description = 'Stop'     
    
    def run_duration_calc(self, obj):
        timediff = obj.run_stop - obj.run_start
        diffseconds = float(timediff.total_seconds())
        
        day = diffseconds // (24 * 3600)
        diffseconds = diffseconds % (24 * 3600)
        hour = diffseconds // 3600
        diffseconds %= 3600
        minutes = diffseconds // 60
        diffseconds %= 60
        seconds = diffseconds
        return "d:%d h:%d m:%d s:%d" % (day, hour, minutes, seconds)
                
    run_duration_calc.short_description = 'Dur'    

    def run_id(self, obj):
        return u'R-%s' % obj.id

    run_id.short_description = 'RunId'  
    
    def definition_id(self, obj):
        #return format_html('<a href="http://%s:8000/mpqe/dashboard/solution/%s">%s</a> ' % (settings.MPQE_HOST, obj.solution.id, obj.solution.solution_name))
        return format_html('<a href="http://%s:8000/mpqe/report/sbar1?rid=%s&rname=%s&rtype=%s&rstate=%s">%s</a> ' % (settings.MPQE_HOST,  obj.definition.id, obj.definition.name, obj.definition.test_type, obj.definition.ready_state, obj.definition.name))
    

    definition_id.short_description = 'Definition'
    
    def definition_test_type(self, obj):
        return "%s" % obj.definition.test_type

    definition_test_type.short_description = 'Type'
    
    def product_stack_id(self, obj):
        #return format_html('<a href="http://%s:8000/mpqe/dashboard/stack/%s">%s</a> ' % (settings.MPQE_HOST, obj.solution.product_stack.id, obj.solution.product_stack.stack_name))
        return format_html('<a href="http://%s:8000/mpqe/report/pstacks?rname=%s">%s</a> ' % (settings.MPQE_HOST,  obj.definition.product_stack.name, obj.definition.product_stack.name))
    


    product_stack_id.short_description = 'ProdStack'
    
    def product_stack_contents(self, obj):
        p = obj.definition.product_stack.products.all()
        return list(p)        

    product_stack_contents.short_description = 'ProdMatrix'
    
    def run_status_(self, obj):
        colors = {
            'COMPLETE': 'blue',
            'RUNNING': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'ABORT': 'orange',
            'FATAL': 'red',
            'EMERGENCY': 'red',
            'ALERT': 'orange',
            'CRITICAL': 'red',
        }
        return format_html('<font color={}>{}</font>', colors[obj.run_status], obj.run_status,)

    run_status_.short_description = 'Status'    
    
    def doc_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.solution_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/doc.png" width="20" height="20"></a>' % obj.definition.solution_link)

    doc_id.short_description = 'Doc'
    
    def jenkins_id(self, obj):
        # return format_html('<a href="%s" target="_blank">*</a> ' % obj.jenkins)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/jenkins.png" width="20" height="20"></a>' % obj.jenkins)

    jenkins_id.short_description = 'JEN'    
    
    def jira_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.jira_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/jira.png" width="20" height="20"></a>' % obj.definition.jira_link)

    jira_id.short_description = 'JIRA'
        
    def defect_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.defect_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/defect.png" width="20" height="20"></a>' % obj.definition.defect_link)

    defect_id.short_description = 'DEF'    

    def tcms_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.tcms_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/tcms.png" width="20" height="20"></a>' % obj.definition.tcms_link)

    tcms_id.short_description = 'TCMS' 

    def report_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.tcms_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/report.png" width="20" height="20"></a>' % obj.report)

    report_id.short_description = 'RPT' 
    
    # hides the add button on view
    def has_add_permission(self, request, obj=None):
        return False    
    
    def xhas_add_permission(self, request):
        # print request.user.email, request.user.username
        if request.user.is_authenticated:
            # Do something for authenticated users.
            if request.user.is_staff:
                
                if  request.user.groups.filter(name='Management').exists() or request.user.groups.filter(name='Testers').exists(): 
                    return True
                else:
                    return False
            else:
                return False
        else:
            # Do something for anonymous users.
            return False
        
        
class RunAdmin(admin.ModelAdmin):

    # actions = None
    actions_on_top = True
    actions_on_bottom = True
    
    list_per_page = 50
    ordering = ['-id']
        
    list_display = ('id',
                      'solution_id',
                       'product_stack_id',
                       'solution_testtype',
                         'run_step',
                          'run_status_',
                           'testinfo_id',
                           'tester',
                            'run_starttime',
                             'run_stoptime',
                              'run_duration_calc',
                              'doc_id',
                              'jira_id',
                               'jenkins_id',
                               'defect_id',
                               'tcms_id',
                               'report_id')
    
    list_display_links = ('id',
                           'solution_id',
                             'product_stack_id',
                              'doc_id',
                              'jira_id',
                               'jenkins_id',
                               'defect_id',
                               'tcms_id',
                               'report_id')
    
    # list_display_links = None
    
    list_editable = ()  
    list_filter = ['run_start',
                   'definition__ready_state',
                   'run_status',
                   'definition__test_type',
                   'run_step',
                   'tester']
    
    search_fields = ('id',
                     'definition__name',
                     'definition__product_stack__stack_name',
                     'definition__test_type',
                     'run_status',
                     'run_step',
                     'solution_id__product_stack__products__name',
                     'solution_id__product_stack__products__version',
                     'solution_id__product_stack__products__arch',
                     'tester__email',
                     'tester__username')
    
    # readonly_fields = ()

    def run_starttime(self, obj):
        formatedDate = obj.run_start.strftime("%Y-%m-%d %H:%M:%S")
        return formatedDate

    run_starttime.short_description = 'Start'
    
    def run_stoptime(self, obj):
        timediff = obj.run_stop - obj.run_start
        diffseconds = float(timediff.total_seconds())
        if diffseconds == 0:
            return '- - -' 
        else:
            formatedDate = obj.run_stop.strftime("%Y-%m-%d %H:%M:%S")
            return formatedDate
    
    run_stoptime.short_description = 'Stop' 
    
    
    def run_duration_calc(self, obj):
        timediff = obj.run_stop - obj.run_start
        diffseconds = float(timediff.total_seconds())
        
        if diffseconds ==0:
            # means the run is in play
            utc = UTC()
            currenttime = datetime.now(utc)            
            timediff = currenttime - obj.run_start
            diffseconds = float(timediff.total_seconds())            
            
            day = diffseconds // (24 * 3600)
            diffseconds = diffseconds % (24 * 3600)
            hour = diffseconds // 3600
            diffseconds %= 3600
            minutes = diffseconds // 60
            diffseconds %= 60
            seconds = diffseconds
            return "d:%d h:%d m:%d s:%d" % (day, hour, minutes, seconds)
            
        else:
            
            # means the run is done    
            day = diffseconds // (24 * 3600)
            diffseconds = diffseconds % (24 * 3600)
            hour = diffseconds // 3600
            diffseconds %= 3600
            minutes = diffseconds // 60
            diffseconds %= 60
            seconds = diffseconds
            return "d:%d h:%d m:%d s:%d" % (day, hour, minutes, seconds)
                
    run_duration_calc.short_description = 'Elapsed'    

    def run_id(self, obj):
        return u'R-%s' % obj.id

    run_id.short_description = 'RunId'  
    
    def solution_id(self, obj):
        #return format_html('<a href="http://%s:8000/mpqe/dashboard/solution/%s">%s</a> ' % (settings.MPQE_HOST, obj.solution.id, obj.solution.solution_name))
        return format_html('<a href="http://%s:8000/mpqe/report/sbar1?rid=%s&rname=%s&rtype=%s&rstate=%s">%s</a> ' % (settings.MPQE_HOST,  obj.definition.id, obj.definition.name, obj.definition.test_type, obj.definition.ready_state, obj.definition.name))


    solution_id.short_description = 'Definition'
    
    def solution_testtype(self, obj):
        return "%s" % obj.definition.test_type

    solution_testtype.short_description = 'Type'
    
    def product_stack_id(self, obj):
        #return format_html('<a href="http://%s:8000/mpqe/dashboard/stack/%s">%s</a> ' % (settings.MPQE_HOST, obj.solution.product_stack.id, obj.solution.product_stack.stack_name))
        return format_html('<a href="http://%s:8000/mpqe/report/pstacks?rname=%s">%s</a> ' % (settings.MPQE_HOST,  obj.definition.product_stack.name, obj.definition.product_stack.name))
        

    product_stack_id.short_description = 'ProdStack'
    
    def run_status_(self, obj):
        colors = {
            'COMPLETE': 'blue',
            'RUNNING': 'green',
            'WARNING': 'orange',
            'ERROR': 'red',
            'ABORT': 'red',
            'FATAL': 'red',
            'EMERGENCY': 'red',
            'ALERT': 'red',
            'CRITICAL': 'red',
            'CANCELLED': 'red',
            }
        return format_html('<font color={}>{}</font>', colors[obj.run_status], obj.run_status,)

    run_status_.short_description = 'Status'    
    
    def doc_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.solution_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/doc.png" width="20" height="20"></a>' % obj.definition.solution_link)

    doc_id.short_description = 'Doc'
    
    def jenkins_id(self, obj):
        # return format_html('<a href="%s" target="_blank">*</a> ' % obj.jenkins)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/jenkins.png" width="20" height="20"></a>' % obj.jenkins)

    jenkins_id.short_description = 'JEN'    
    
    def jira_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.jira_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/jira.png" width="20" height="20"></a>' % obj.definition.jira_link)

    jira_id.short_description = 'JIRA'
        
    def defect_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.defect_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/defect.png" width="20" height="20"></a>' % obj.definition.defect_link)

    defect_id.short_description = 'DEF'    

    def tcms_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.tcms_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/tcms.png" width="20" height="20"></a>' % obj.definition.tcms_link)

    tcms_id.short_description = 'TCMS' 

    def report_id(self, obj):
        # return format_html('<a href="%s" target="_blank">***</a> ' % obj.solution.tcms_link)
        return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/report.png" width="20" height="20"></a>' % obj.report)
    report_id.short_description = 'RPT'
    
    
    def testinfo_id(self, obj):
        
        if obj.test_info.startswith('http'):
            return format_html('<a href="%s"  target="_blank"> <img border="0" alt="***" src="/static/images/report.png" width="20" height="20"></a>' % obj.test_info)
        else:
            return format_html('%s' % obj.test_info)
        
    testinfo_id.short_description = 'Test Info'
    
    
    
    
    
    
     
    
    def xhas_add_permission(self, request):
        # print request.user.email, request.user.username
        if request.user.is_authenticated:
            # Do something for authenticated users.
            if request.user.is_staff:
                
                if  request.user.groups.filter(name='Management').exists() or request.user.groups.filter(name='Testers').exists(): 
                    return True
                else:
                    return False
            else:
                return False
        else:
            # Do something for anonymous users.
            return False
        
# class XRunProxyFilter(SimpleListFilter):
#     
#     
#     title = 'Interop Product Matrix'
#     parameter_name = 'COMPLETE'
#     default_value = None
# 
#     def lookups(self, request, model_admin):
#         return ( ('COMPLETE', 'Complete'),  )
#         #return None
# 
#     def queryset(self, request, queryset):
#         print (self.value())
#         print (request)
#         print (queryset)
# 
#         queryset = queryset.filter( Q(run_status='COMPLETE') )
#         queryset = queryset.filter( Q(definition__test_type='INTEROP'))
# 
#        
#         print (queryset)
#         return queryset
#     
#     def value(self):
#         """
#         Overriding this method will allow us to always have a default value.
#         """
#         return 'Complete'        

        
admin.site.register(MatrixOfProduct, RunProxyAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Product)
admin.site.register(Stack)
admin.site.register(Definition)

