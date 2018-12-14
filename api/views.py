from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from dashboard.models import Product
from dashboard.models import Definition
from dashboard.models import Stack
from dashboard.models import Run

from django.contrib.auth.models import User
from dashboard.serializers import ProductSerializer
from dashboard.serializers import UserSerializer
from dashboard.serializers import ScenarioSerializer
from dashboard.serializers import StackSerializer
from dashboard.serializers import RunSerializer
from dashboard.serializers import  QueryForScenarioSerializer

from rest_framework import viewsets


from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
from django.http import JsonResponse



class ProductViewSet(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['put', 'get', 'post', 'delete']
        
    def get_queryset(self):
        
        queryset = Product.objects.all().order_by('-id')
        name = self.request.query_params.get('name', None)
        ver = self.request.query_params.get('ver', None)
        if name is not None:
            queryset = queryset.filter(name=name)
            
        if ver is not None:
            queryset = queryset.filter(version=ver)
        return queryset
    
# class RegistrationViewSet(viewsets.ModelViewSet):
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer    
    
class InteroptViewSet(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer    
         
class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = ScenarioSerializer
    http_method_names = ['put', 'get', 'post', 'delete']
    
        
    def get_queryset(self):
        
        # query for scenario
        queryset = Definition.objects.all().order_by('-id')
        
        # query scenarios by product name,ver and arch
        # http://127.0.0.1:8000/api/scenario/?product_name=rhel&product_ver=6&product_arch=x86-64
        
        name = self.request.query_params.get('product_name', None)
        if name is not None:
            queryset = queryset.filter(product_stack__products__name = name).distinct()
            
        ver = self.request.query_params.get('product_ver', None)
        if ver is not None:
            queryset = queryset.filter(product_stack__products__version = ver).distinct()
            
        arch = self.request.query_params.get('product_arch', None)
        if arch is not None:
            queryset = queryset.filter(product_stack__products__arch = arch).distinct()
            
        testtype = self.request.query_params.get('test_type', None)
        if testtype is not None:
            queryset = queryset.filter(test_type = testtype).distinct()
             
        readystate = self.request.query_params.get('ready_state', None)
        if readystate is not None:
            queryset = queryset.filter(ready_state = readystate).distinct()
            
        return queryset    
    


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    http_method_names = ['put', 'get', 'post', 'delete']
    
    # runid = property(get_id)    
    # solution = models.ForeignKey(Solution, on_delete=models.DO_NOTHING,help_text="Field defines the solution associated to this run")
    # tester = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text="Field for the user who executed the run")
    # run_start = models.DateTimeField(default=timezone.now, help_text="Field that defines the start date / time of a run")
    # run_stop = models.DateTimeField(default=timezone.now, help_text="Field that defines the stop date / time of a run")
    # run_uuid = models.CharField(max_length=500,default="", help_text="Field that defines the uid of a run")
    # jenkins = models.CharField(max_length=500,default="https://jenkins", help_text="Field link to define the Jenkins runner job associated to this job")
    # report = models.CharField(max_length=500,default="https://report", help_text="Field link to define  a run report associated to this job")
    #  
    # TEST_STEP = (
    #     ('INITIALIZING', 'Initializing'),
    #     ('ENVIRONMENT', 'Environment'),
    #     ('VALIDATION', 'Validation'),
    #     ('PROVISIONING', 'Provisioning'),
    #     ('ORCHESTRATION', 'Orchestration'),
    #     ('EXECUTION', 'Execution'),
    #     ('REPORTING', 'Reporting'),
    #     ('CLEANUP', 'Cleanup'),
    #     ('COMPLETE', 'Complete'),
    #     ('STR', 'STR'),
    # ) 
    # run_step = models.CharField(max_length=13, choices=TEST_STEP, default='INITIALIZING',help_text="Field to represent the step of a run")
    #  
    # TEST_STATUS = (
    #     ('RUNNING', 'Running'),
    #     ('COMPLETE', 'Complete'),
    #     ('ERROR', 'Error'),
    #     ('ABORT', 'Abort'),
    #     ('WARNING', 'Warning'),
    #     ('FATAL', 'Fatal'),
    #     ('EMERGENCY', 'Emergency'),
    #     ('ALERT', 'Alert'),
    #     ('CANCELLED', 'Cancelled'),
    #     ('CRITICAL', 'Critical'),
    # ) 
    # run_status = models.CharField(max_length=9, choices=TEST_STATUS,default='RUNNING', verbose_name='Status',help_text="Field to represent the status of a run")
    
    # cdf_original = models.TextField(default='', blank=True, null=False, help_text="Field to contain the original carbon descriptor file")
    # cdf_teardown = models.TextField(default='', blank=True, null=False, help_text="Field to contain the updated carbon descriptor file used for carbon cleanup process")
    # cdf_config = models.TextField(default='', blank=True, null=False, help_text="Field to contain the carbon configuration file")
    # run_info = models.TextField(default='', blank=True, null=False, help_text="Field to contain json defining keys and profile to delete after a run")
    # test_info = models.TextField(default='-', blank=True, null=False, help_text="Field to contain test results or STR report link")
    
        
    def get_queryset(self):
        
        # query for scenario
        queryset = Run.objects.all().order_by('-id')
        
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id = id).distinct()
            return queryset
        
        run_step = self.request.query_params.get('run_step', None)
        if run_step is not None:
            queryset = queryset.filter(run_step = run_step).distinct()
        
        
        run_status = self.request.query_params.get('run_status', None)
        if run_status is not None:
            queryset = queryset.filter(run_status = run_status).distinct()
        

        import datetime
        run_start = self.request.query_params.get('run_start', None)
        format_str = '%Y-%m-%d'
        if run_start is not None:
            print (run_start)
            run_start_obj = datetime.datetime.strptime(run_start, format_str)
            queryset = queryset.filter(run_start__date__gte=run_start_obj)
            #queryset = queryset.filter(run_start__range=["2011-01-01", "2011-01-31"]).distinct()
            
        run_stop = self.request.query_params.get('run_stop', None)
        format_str = '%Y-%m-%d'
        if run_stop is not None:
            print (run_stop)
            run_stop_obj = datetime.datetime.strptime(run_stop, format_str)
            # add 1 day because its really 0 hundred hours
            queryset = queryset.filter(run_stop__date__lte=run_stop_obj)
        
        
        # query scenarios by product name,ver and arch
        # http://127.0.0.1:8000/api/scenario/?product_name=rhel&product_ver=6&product_arch=x86-64
        # http://127.0.0.1:8000/api/scenario/?product_name=rhel&product_ver=5&product_arch=x86-64
#         name = self.request.query_params.get('product_name', None)
#         if name is not None:
#             queryset = queryset.filter(product_stack__products__name = name).distinct()
#             
#         ver = self.request.query_params.get('product_ver', None)
#         if ver is not None:
#             queryset = queryset.filter(product_stack__products__version = ver).distinct()
#             
#         arch = self.request.query_params.get('product_arch', None)
#         if arch is not None:
#             queryset = queryset.filter(product_stack__products__arch = arch).distinct()
            
        return queryset



         
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class QueryForScenarioViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class =  QueryForScenarioSerializer
    http_method_names = ['get']
        
    def get_queryset(self):
        
        # query for scenario
        queryset = Definition.objects.all().order_by('-id')
        
        # query string
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(product_stack__products__name = name).distinct()
            
        ver = self.request.query_params.get('ver', None)
        if ver is not None:
            queryset = queryset.filter(pproduct_stack__products__version = ver).distinct()
            
        arch = self.request.query_params.get('arch', None)
        if arch is not None:
            queryset = queryset.filter(product_stack__products__arch = arch).distinct()
            
        return queryset
    
    
             
