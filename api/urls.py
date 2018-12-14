# from django.conf.urls import url
# from . import views
#  
# urlpatterns = [
#         url(r'^$', views.index, name='index'),
# ]

from django.conf.urls import url, include
from rest_framework import routers
from api import views
from django.urls import path

#from rest_framework.schemas import get_schema_view
# Routers provide an easy way of automatically determining the URL conf.
router_v1 = routers.DefaultRouter()
router_v1.register(r'products', views.ProductViewSet)
router_v1.register(r'stacks', views.InteroptViewSet)
router_v1.register(r'definitions', views.ScenarioViewSet)
router_v1.register(r'runs', views.RunViewSet)
router_v1.register(r'users', views.UserViewSet)

#router.register(r'qscenario', views.QueryForScenarioViewSet)
#schema_view = get_schema_view(title='MPQE API')

# future
# router_v2 = routers.DefaultRouter()
# router_v2.register(r'run', views.RunViewSet_v2)
# router_v2.register(r'solution', views.ScenarioViewSet_v2)
# router_v2.register(r'product_stack', views.InteroptViewSet_v2)
# router_v2.register(r'products', views.ProductViewSet_v2)
# router_v2.register(r'users', views.UserViewSet_v2)

urlpatterns = [

     #url(r'^schema/$', schema_view),

     #url(r'^$', views.index, name='index'),
     path('v1/', include(router_v1.urls)),     
     
     #future v2
     #path('v2/', include(router_v2.urls)),
     
] 
