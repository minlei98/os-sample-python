# Generated by Django 2.1.1 on 2018-09-11 16:14

import dashboard.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=100)),
                ('description', models.TextField(default='')),
                ('version', models.CharField(default='1', max_length=100)),
                ('arch', models.CharField(default='x86-64', max_length=100)),
                ('type', models.CharField(default='prod', max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('props', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dashboard.models.get_default_data, null=True)),
            ],
            options={
                'ordering': ('name', 'version'),
            },
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('run_stop', models.DateTimeField(default=django.utils.timezone.now)),
                ('run_duration', models.CharField(default='d:0 h:0 m:0: s:0', max_length=500)),
                ('jenkins', models.CharField(default='https://pit-stg-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/view/Carbon/view/POC/job/MPQE-Runner/14/', max_length=500)),
                ('report', models.CharField(default='http://report', max_length=500)),
                ('run_step', models.CharField(choices=[('INITIALIZING', 'Initializing'), ('PROVISIONING', 'Provisioning'), ('ORCHESTRATION', 'Orchestration'), ('EXECUTION', 'Execution'), ('REPORTING', 'Reporting'), ('COMPLETE', 'Complete')], default='INITIALIZING', max_length=13)),
                ('run_status', models.CharField(choices=[('RUNNING', 'Running'), ('COMPLETE', 'Complete'), ('ERROR', 'Error'), ('ABORT', 'Abort')], default='RUNNING', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_name', models.CharField(default='default', max_length=100, unique=True)),
                ('solution_description', models.TextField(default='description')),
                ('solution_version', models.CharField(default='1.0', max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('carbon_service_checks', models.TextField(default='dep_check:\n  - ci-rhos\n  - zabbix-sysops\n  - brew\n  - covscan\n  - polarion\n  - rpmdiff\n  - umb\n  - errata\n  - rdo-cloud\n  - gerrit:gerrit.host.prod.eng.bos.redhat.com\n')),
                ('carbon_provision', models.TextField(default='provision:\n  - name: test_machine_01\n    role: hypervisor\n    description: "bare metal server to host OCP_CNS test environment"\n    provider: beaker\n    credential: beaker\n    bkr_jobgroup: ci-ops-pit\n    bkr_arch: x86_64\n    bkr_tag: "RTT_ACCEPTED"\n    bkr_whiteboard: Carbon bare metal server to host OCP_CNS test environment (Internal) - SJM\n    bkr_distro: RHEL-7.4\n    bkr_variant: Server\n    bkr_host_requires_options: ["arch=x86_64", "memory>=65000", "processors>=400"]\n    bkr_key_values: ["DISKSPACE>=100000", "HVM=1"]\n    bkr_taskparam: [ "RESERVETIME=345600" ]\n    ansible_params:\n      ansible_user: root\n      ansible_ssh_private_key_file: keys/carbon\n\n')),
                ('carbon_orchestration', models.TextField(default='#orchestrate:\n\n# system configuration\n# product(s) install\n# product(s) configuration\n# test setup\n\norchestrate:\n  - name: ansible/ssh_connect.yml\n    description: "setup ssh keys for key based authentication to hypervisor"\n    orchestrator: ansible\n    hosts: localhost\n    ansible_options:\n      extra_vars:\n        username: root\n        password: ci-ops-pit\n    ansible_galaxy_options:\n      roles:\n        - rywillia.ssh-copy-id\n\n  - name: ansible/find_nic.yml\n    description: "find the active network interface card on the hypervisor"\n    orchestrator: ansible\n    hosts: hypervisor\n\n  - name: ansible/master.yml\n    description: "install and configure OCP and CNS"\n    orchestrator: ansible\n    hosts: hypervisor\n\n')),
                ('testtype', models.CharField(choices=[('INTEROP', 'Interop'), ('SCENARIO', 'Scenario'), ('SYSTEM-LOAD', 'System-Load'), ('SYSTEM-RELIABILITY', 'System-Reliability'), ('SYSTEM-STRESS', 'System-Stress'), ('SYSTEM-LONGEVITY', 'System-Longevity')], default='INTEROP', max_length=18)),
                ('carbon_execution', models.TextField(default='execute:\n  - name: OCP System Test\n    description: "Load Tests"\n    function: STR\n    type: non-functional\n    objective: load\n    ansible_options:\n      extra_vars:\n        str_key: rhhi_key.key\n        str_profile: /rhhi_profile.yml \n        username: root\n        password: password\n\n')),
                ('carbon_report', models.TextField(default='report:\n  - name: Report Portal\n    description: "Dashboard"\n    ansible_options:\n      extra_vars:\n        username: root\n        password: password\n')),
                ('carbon_cfg', models.TextField(default='# carbon config file\n# ==================\n# default settings\n\n[defaults]\nlog_level=debug\ndata_folder=/var/local/carbon\nworkspace=.\ninternal=True\ndep_check_endpoint=http://semaphore.op.redhat.com/api/v1\n\n# credentials settings\n[credentials:beaker]\nkeytab=<keytab>\nkeytab_principal=<keytab_principal>\nusername=<username>\npassword=<password>\n\n[credentials:openstack]\nauth_url=<auth_url>\ntenant_name=<tenant_name>\nusername=<username>\npassword=<password>\n\n')),
                ('solution_repo', models.CharField(blank=True, default='https://gitlab.cee.redhat.com/PIT/CSS_OCP_CNS.git', max_length=1000, null=True)),
                ('solution_link', models.CharField(blank=True, default='https://docs.engineering.redhat.com/display/MPQE/MPQE+Home', max_length=1000, null=True)),
                ('jira_link', models.CharField(blank=True, default='https://projects.engineering.redhat.com/secure/Dashboard.jspa', max_length=1000, null=True)),
                ('defect_link', models.CharField(blank=True, default='https://bugzilla.redhat.com/', max_length=1000, null=True)),
                ('tcms_link', models.CharField(blank=True, default='https://polarion.engineering.redhat.com/polarion/', max_length=1000, null=True)),
            ],
            options={
                'ordering': ('solution_name', 'solution_version'),
            },
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack_name', models.CharField(default='default', max_length=100, unique=True)),
                ('products', models.ManyToManyField(to='dashboard.Product')),
            ],
            options={
                'ordering': ('stack_name',),
            },
        ),
        migrations.AddField(
            model_name='solution',
            name='product_stack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Stack'),
        ),
        migrations.AddField(
            model_name='run',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Solution'),
        ),
        migrations.AddField(
            model_name='run',
            name='tester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
