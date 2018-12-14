from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

#https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
solution_repo_default = '''https://gitlab.cee.redhat.com/PIT/CSS_OCP_CNS.git'''

resource_check = '''resource_check:

  # Open Stack Resources
  - ci-rhos
  - rdo-cloud
  
  # Application lifecycle Management (ALM) lifecycle management (governance, development, and maintenance) of computer programs.
  - polarion
  
  # Universal Message Bus
  - umb
  
  # Gerrit is web-based team code collaboration tool. Software developers in a team can review each other's modifications
  # on their source code using a Web browser and approve or reject those changes. It integrates closely with Git, a
  # distributed version control system.
  - gerrit:gerrit.host.prod.eng.bos.redhat.com
  
  # Build system
  # - brew
  
  # Zabbix is a mature and effortless enterprise-class open source monitoring solution for network monitoring and application monitoring of millions of metrics.
  #- zabbix-sysops
  
  # Errata tool is the approved errata delivery tool for Red Hat.  It includes auditing, testing, and a stage-gate process with approvals that helps Red Hat prove the integrity of the files we deliver. 
  #- errata
  
  # Whenever a Brew build is attached to an advisory in the Errata Tool, an automated RPMDiff job is scheduled and examined.
  #- rpmdiff
  
  # Coverity Scan. Static Analysis. Finds defects in your Java, C/C++, C#, JavaScript, Ruby, or Python
  #- covscan
  
  #- beaker - future not supported
  
  #- gitlab - future not supported
  
  #- beaker - future not supported
  
  #- others - future not supported
    
'''


provisioner_default_1 = '''provision:
  - name: test_machine_01
    role: hypervisor
    description: "bare metal server to host OCP_CNS test environment"
    provider:
      name: beaker
      credential: beaker
      jobgroup: ci-ops-pit
      arch: x86_64
      tag: "RTT_ACCEPTED"
      whiteboard: Carbon bare metal server to host OCP_CNS test environment (Internal)
      distro: RHEL-7.4
      variant: Server
      host_requires_options: ["arch=x86_64", "memory>=65000", "processors>=400"]
      key_values: ["DISKSPACE>=100000", "HVM=1"]
      taskparam: [ "RESERVETIME=345600" ]
    ansible_params:
      ansible_user: root
      ansible_ssh_private_key_file: keys/carbon
'''





provisioner_default = '''provision:
  - name: str_product_host_1
    role: str_monitor
    description: open stack instance 1
    provider:
      name: openstack
      credential: openstack
      flavor: m1.small
      floating_ip_pool: 10.8.240.0
      hostname: str_product_host_1_y0shm
      image: rhel-7.4-server-x86_64-released
      keypair: pit-jenkins
      networks:
      - pit-jenkins
    provisioner: openstack-libcloud 
    ansible_params:
      ansible_ssh_private_key_file: ../mpqe-utils/keys/str.pem
      ansible_user: cloud-user
 
  - name: str_product_host_2
    role: str_monitor
    description: null
    provider:
      credential: openstack
      flavor: m1.small
      floating_ip_pool: 10.8.240.0
      hostname: str_product_host_2_92lm8
      image: rhel-7.4-server-x86_64-released
      keypair: pit-jenkins
      name: openstack
      networks:
      - pit-jenkins
    provisioner: openstack-libcloud  
    ansible_params:
      ansible_ssh_private_key_file: ../mpqe-utils/keys/str.pem
      ansible_user: cloud-user

  - name: str_product_host_3
    role: str_test
    description: null
    provider:
      credential: openstack
      flavor: m1.small
      floating_ip_pool: 10.8.240.0
      hostname: str_product_host_3_izs1c
      image: rhel-7.4-server-x86_64-released
      keypair: pit-jenkins
      name: openstack
      networks:
      - pit-jenkins
    provisioner: openstack-libcloud
    ansible_params:
      ansible_ssh_private_key_file: ../mpqe-utils/keys/str.pem
      ansible_user: cloud-user

  - name: str_client_1
    role: str_static
    description: pytest test environment
    ip_address: 10.8.248.163
    ansible_params:
      ansible_ssh_private_key_file: ../mpqe-utils/keys/str.pem
      ansible_user: cloud-user

  - name: localhost
    role: local
    description: jenkins slave
    ip_address: 127.0.0.1
    ansible_params:
      ansible_connection: local
'''









report_default = '''report:
  - name: Report Portal
    description: "Dashboard"
    ansible_options:
      extra_vars:
        username: root
        password: password
'''





ochestration_default_1 = '''#orchestrate:

# system configuration
# product(s) install
# product(s) configuration
# test setup

orchestrate:

  - name: ansible/product1
    description: "install product 1"
    orchestrator: ansible
    hosts: hypervisor
    ansible_options:
      extra_vars:
        username: root
        password: ci-ops-pit
    ansible_galaxy_options:
      roles:
        - product1

  - name: ansible/product2
    description: "install product 2"
    orchestrator: ansible
    hosts: hypervisor
    ansible_options:
      extra_vars:
        username: root
        password: ci-ops-pit
    ansible_galaxy_options:
      roles:
        - product2


  - name: ansible/product3
    description: "install product 3"
    orchestrator: ansible
    hosts: hypervisor
    ansible_options:
      extra_vars:
        username: root
        password: ci-ops-pit
    ansible_galaxy_options:
      roles:
        - product3
'''


ochestration_default = '''# orchestrate:
# system configuration
# product(s) install
# product(s) configuration
# test setup

orchestrate:
  - name: ../mpqe-utils/playbooks/testclient_install.yml
    description: setup monitor systems
    orchestrator: ansible
    hosts:
    - str_product_host_1
    - str_product_host_2
    ansible_options:
      extra_vars:
        abrt_bool: true
        monitor_bool: true 

  - name: ../mpqe-utils/playbooks/testclient_install.yml
    orchestrator: ansible
    description: setup test client systems
    hosts:
    - str_product_host_3  
    ansible_options:
      extra_vars:
        test_bool: true

'''
























execution_default_1 = '''execute:
  - name: test suite 01
    description: "execute tests against test clients"
    executor: runner
    hosts: driver
    git:
      - repo: https://server.com/myproject.git
        version: test-ver-0.1
        dest: /tmp
    shell:
      - chdir: /tmp
        command: /usr/bin/restraint --host 1={{testclient01}}:8081 --job foo.xml
    artifacts: retraint-*, test.log

  - name: test suite 02
    description: "execute tests against test clients"
    executor: runner
    hosts: driver
    git:
      - repo: https://server.com/myproject.git
        version: test-ver-0.1
        dest: /tmp
    script:
      - chdir: /tmp
        name: tests.sh arg1 arg2
    artifacts: retraint-*, test.log
 
  - name: test suite 03
    description: "execute tests against test clients"
    executor: runner
    hosts: driver
    git:
      - repo: https://server.com/myproject.git
        version: test-ver-0.1
        dest: /tmp
    playbook:
      - chdir: /tmp
        name: test.yml
    artifacts: retraint-*, test.log

'''





execution_default = '''execute:
  - name: profile updater
    description: creates master str profile combining the ansible inv and str template file
    executor: runner
    hosts:
    - localhost
    shell:
    - chdir: ../mpqe-utils/utils
      command: python profile_updater.py --profile=carbon_str_template1.yml --inventory=../../scenario/{
        localhost.data_folder }/inventory --output=carbon_str_updated.yml
      ignore_rc: true

  - name: str execution
    description: execute STR tests on the clients
    executor: runner
    hosts:
    - localhost  
    shell:
    - chdir: ../mpqe-utils/utils
      command: python str_runner.py --user=strjenkins --pw=redhat --group=str --loglevel=DEBUG
      ignore_rc: true
'''
















carboncfg_definition = '''# carbon config file
[defaults]
data_folder=/tmp
dep_check_endpoint=http://semaphore.op.redhat.com/api/v1
log_level=info

[jenkins]
tear_down=true
carbon_branch=master
'''










creds_definition = '''
[credentials:beaker]
hub_url=https://beaker.engineering.redhat.com
keytab=/etc/jenkins.keytab-pit-jenkins.rhev-ci-vms.eng.rdu2.redhat.com
keytab_principal=jenkins/pit-jenkins.rhev-ci-vms.eng.rdu2.redhat.com@REDHAT.COM

[credentials:openstack]
auth_url=https://ci-rhos.centralci.eng.rdu2.redhat.com:13000/v2.0
tenant_name=pit-jenkins
username=pit-jenkins
password=password
'''




def get_default_data():
    return { 'variant':'Server' }    

    
class Product(models.Model):
    
  
    name = models.CharField(max_length=100,default='default', blank=False, null=False)
    version = models.CharField(max_length=100,default='1', blank=False, null=False)
    arch = models.CharField(max_length=100,default='x86-64')
    description = models.TextField(default='', blank=False, null=False)    
    PHASE_STATE = (
        ('MAINTENANCE', 'Maintenance'),
        ('PLANNING', 'Planning'),
        ('DEVELOPMENT', 'Development'),
        ('UNSUPPORTED', 'Unsupported'),
        ('TESTING', 'Testing'),
    )
    phase = models.CharField(max_length=11, choices=PHASE_STATE, default='MAINTENANCE')    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    props = JSONField(null=True, blank=True, default=get_default_data)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.version, self.arch)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = '1. Products'
        ordering = ('name','version','arch')
        
     

class Stack(models.Model):
    
    
    class Meta:
        verbose_name = 'Product Stack'
        verbose_name_plural = '2. Product Stacks'
        ordering = ('name',)     
    
    name = models.CharField(max_length=100,default='default', blank=False, null=False, unique=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return '%s' % self.name 
      
             
class Definition(models.Model):
    
    name = models.CharField(max_length=100 ,default="default", blank=False, null=False, unique=True)
    version = models.CharField(max_length=100, default="1.0", blank=False, null=False)
    description = models.TextField(default="description", blank=False, null=False)
    
    READY_STATE = (
        ('PRODUCTION', 'Production'),
        ('DEVELOPMENT', 'Development'),
    )
    ready_state = models.CharField(max_length=11, choices=READY_STATE, default='DEVELOPMENT')    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    product_stack = models.ForeignKey(Stack, on_delete=models.DO_NOTHING,)
         
    # carbon definitions
    carbon_provision = models.TextField(default=provisioner_default, blank=False, null=False)
    carbon_orchestration = models.TextField(default=ochestration_default, blank=False, null=False)
    
    TEST_TYPE = (
        ('INTEROP', 'Interop'),
        ('SCENARIO', 'Customer-Scenario'),
        ('SYSTEM', 'System'),
    )
    test_type = models.CharField(max_length=18, choices=TEST_TYPE, default='INTEROP')
        
    carbon_execution = models.TextField(default=execution_default, blank=False, null=False)
    carbon_report = models.TextField(default=report_default, blank=False, null=False)
    carbon_cfg = models.TextField(default=carboncfg_definition, blank=False, null=False)
    carbon_resource_check = models.TextField(default=resource_check, blank=False, null=False)

    solution_repo = models.CharField(max_length=1000,default=solution_repo_default, blank=True, null=True)
    solution_link = models.CharField(max_length=1000, default="https://docs.engineering.redhat.com/display/MPQE/MPQE+Home", blank=True, null=True)
    jira_link = models.CharField(max_length=1000, default="https://projects.engineering.redhat.com/secure/Dashboard.jspa", blank=True, null=True)
    defect_link = models.CharField(max_length=1000, default="https://bugzilla.redhat.com/", blank=True, null=True)
    tcms_link = models.CharField(max_length=1000, default="https://polarion.engineering.redhat.com/polarion/", blank=True, null=True)
    
    
        
    def __str__(self):
        return '%s-%s' % (self.name,self.version)

    class Meta:
        verbose_name = 'Definition'
        verbose_name_plural = '3. Test Definitions'
        ordering = ('name','version',)
        
        
        
class Run(models.Model):
    
    class Meta:
        verbose_name = 'Test Run'
        verbose_name_plural = '4. Test Runs'
        ordering = ('-id',)

     
    def get_id(self):
        return str(self.id)
     
    runid = property(get_id)    
    definition = models.ForeignKey(Definition, on_delete=models.DO_NOTHING,help_text="Field defines the test definition associated to this run")
    tester = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text="Field for the user who executed the run")
    run_start = models.DateTimeField(default=timezone.now, help_text="Field that defines the start date / time of a run")
    run_stop = models.DateTimeField(default=timezone.now, help_text="Field that defines the stop date / time of a run")
    run_uuid = models.CharField(max_length=500,default="", help_text="Field that defines the uid of a run")
    jenkins = models.CharField(max_length=500,default="https://jenkins", help_text="Field link to define the Jenkins runner job associated to this job")
    report = models.CharField(max_length=500,default="https://report", help_text="Field link to define  a run report associated to this job")
     
    TEST_STEP = (
        ('INITIALIZING', 'Initializing'),
        ('ENVIRONMENT', 'Environment'),
        ('VALIDATION', 'Validation'),
        ('PROVISIONING', 'Provisioning'),
        ('ORCHESTRATION', 'Orchestration'),
        ('EXECUTION', 'Execution'),
        ('REPORTING', 'Reporting'),
        ('CLEANUP', 'Cleanup'),
        ('COMPLETE', 'Complete'),
        ('STR', 'STR'),
    ) 
    run_step = models.CharField(max_length=13, choices=TEST_STEP, default='INITIALIZING',help_text="Field to represent the step of a run")
     
    TEST_STATUS = (
        ('RUNNING', 'Running'),
        ('COMPLETE', 'Complete'),
        ('ERROR', 'Error'),
        ('ABORT', 'Abort'),
        ('WARNING', 'Warning'),
        ('FATAL', 'Fatal'),
        ('EMERGENCY', 'Emergency'),
        ('ALERT', 'Alert'),
        ('CANCELLED', 'Cancelled'),
        ('CRITICAL', 'Critical'),
    ) 
    run_status = models.CharField(max_length=9, choices=TEST_STATUS,default='RUNNING', verbose_name='Status',help_text="Field to represent the status of a run")
    cdf_original = models.TextField(default='', blank=True, null=False, help_text="Field to contain the original carbon descriptor file")
    cdf_teardown = models.TextField(default='', blank=True, null=False, help_text="Field to contain the updated carbon descriptor file used for carbon cleanup process")
    cdf_config = models.TextField(default='', blank=True, null=False, help_text="Field to contain the carbon configuration file")
    run_info = models.TextField(default='', blank=True, null=False, help_text="Field to contain json defining keys and profile to delete after a run")
    test_info = models.TextField(default='-', blank=True, null=False, help_text="Field to contain test results or STR report link")

    
    def __str__(self):
        return "{}".format(self.definition)
             

class MatrixOfProduct(Run):


    class Meta:
        verbose_name = 'View Product Matrix'
        verbose_name_plural = 'View Product Matrix (Completed)'
        ordering = ('definition__name','definition__product_stack__name','-run_start',) 
        
        proxy = True