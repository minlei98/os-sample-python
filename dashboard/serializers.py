from .models import Product
from .models import Definition
from .models import Stack
from .models import Run
from django.contrib.auth.models import User
from rest_framework import serializers
 
# Serializers define the API representation. 
class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ('url', 'id', 'name', 'description','version', 'arch', 'phase','props')
        
        
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
 
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
         
# Serializers define the API representation.
class StackSerializer(serializers.HyperlinkedModelSerializer):
 
    class Meta:
        model = Stack
        fields = ('url', 'id', 'name','products')
         
# Serializers define the API representation.
class RunSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Run
        fields = ('url',
                   'id',
                    'definition',
                    'tester',
                     'run_start',
                     'run_stop',
                     'run_step',
                     'run_status',
                     'jenkins',
                     'report',
                     'cdf_original',                 
                     'cdf_teardown',
                     'test_info', 
                     'run_info',
                     'cdf_config', 
                     'run_uuid')            
         
# Serializers define the API representation.         
class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
 
    class Meta:
        model = Definition
        fields = ('url',
            'name',
            'description',
            'version',
            'test_type',
            'ready_state',                
            'solution_repo',
            'product_stack',
            'created_date',
            'modified_date',
            'carbon_provision',
            'carbon_orchestration',
            'carbon_execution',
            'carbon_report',
            'carbon_cfg',
            'solution_link',
            'jira_link',
            'defect_link',
            'tcms_link',)
                
                
                
# Serializers define the API representation.         
class QueryForScenarioSerializer(serializers.HyperlinkedModelSerializer):
 
    class Meta:
        model = Definition
        fields = ('url',
            'name',
            'version'
)