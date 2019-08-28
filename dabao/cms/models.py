from django.db import models


# Create your models here.
class DockerImage(models.Model):
    def __str__(self):
        return self.image + ":" + self.tag

    image = models.CharField(max_length=200)
    tag = models.CharField(max_length=128, help_text="Comma seperated tags supported")
    downloaded = models.BooleanField(default=False)


class PivotalProduct(models.Model):
    def __str__(self):
        return self.product

    # Products as of 26 aug 2019
    PivotalProductList = sorted(['hazelcast-pcf', 'crunchy-postgresql', 'buildpack_suite', 'wso2-api-manager', 'vmware-nsx-t', 'service-backups-sdk', 'java-buildpack', 'nginx-buildpack', 'p-clamav-addon', 'pas-for-kubernetes', 'p-ipsec-addon', 'bitdefender-endpoint', 'zettaset-xcrypt', 'pcf-services-sdk', 'big-data', 'pivotal-openjdk', 'gpdb-data-copy', 'on-demand-services-sdk', 'pivotal-rabbitmq', 'blue-medora-nozzle', 'pcf-services', 'apm', 'tc-server-3x-core', 'credhub-service-broker', 'buildpacks', 'service-metrics-sdk', 'dynatrace-fullstack-addon', 'altoros-aws-s3', 'redis-enterprise-pack-service-broker', 'gcp-stackdriver-nozzle', 'redis-enterprise-pack', 'hazelcast-jet', 'tc-server-buildpack', 'a9s-logme', 'snyk-service-broker', 'forgerock', 'snyk', 'pivotal-spring-runtime', 'essential_pks', 'buildpack-extensions', 'minio-internal-blobstore', 'pivotal-mysql', 'greenplum-for-kubernetes', 'evolven-change-analytics', 'pivotal-cf', 'datastax-enterprise-service-broker', 're-tile-manager', 'p-new-relic', 'contrast-security-service-broker', 'pivotal-app-suite', 'pivotal-hd', 'tibco-businessworks', 'splunk-nozzle', 'pivotal-hdb', 'a9s-redis', 'p-cloudcache', 'ibm-websphere-liberty', 'p-metrics-forwarder', 'a9s-mysql', 'altoros-elasticsearch', 'p-mysql', 'a9s-mongodb', 'gcp-service-broker', 'snappydata-service', 'p-event-alerts', 'datadog-application-monitoring', 'stemcells-windows-server', 'new-relic-dotnet-buildpack', 'pivotal-postgres', 'cyberark-conjur', 'altoros-jenkins', 'pivotal-gpdb-backup-restore', 'control-tower', 'hwc-buildpack', 'pivotal-hdp', 'signal-sciences-service-broker', 'ecs-service-broker', 'ibm-mq-advanced', 'pivotal-tcserver', 'p-windows-runtime', 'p-scheduler', 'push-notification-service', 'nodejs-buildpack', 'reliability_view_pcf', 'yugabyte-db', 'pega', 'tc-server-4x-runtimes', 'tc-server-3x-templates', 'tc-server-4x-core', 'riverbed-appinternals', 'altoros-log-search', 'harbor-container-registry', 'a9s-rabbitmq', 'ruby-buildpack', 'black-duck-service-broker', 'staticfile-buildpack', 'python-buildpack', 'binary-buildpack', 'go-buildpack', 'r-buildpack', 'tc-server-4x-templates', 'php-buildpack', 'dotnet-core-buildpack', 'neo4j-enterprise', 'dynatrace', 'vormetric-transparent-encryption', 'platform-automation', 'pcfdev', 'nr-firehose-nozzle', 'heimdall-database-proxy', 'xcrypt-archive', 'p-dataflow', 'a9s-elasticsearch', 'apigee-edge-installer', 'azure-service-broker', 'altoros-cassandra', 'p-spring-cloud-services', 'pivotal_single_sign-on_service', 'minio', 'smb-volume-service', 'altoros-heartbeat', 'mongodb-enterprise-service', 'pagerduty-service-broker', 'p-compliance-scanner', 'pivotal-gemfire', 'appdynamics-analytics', 'p-redis', 'sumologic-nozzle', 'apigee-edge-for-pcf-service-broker', 'cloudbees-core', 'a9s-postgresql', 'synopsys-seeker', 'pcf-automation', 'minio-greenplum', 'datadog', 'boomi-data-services', 'solace-pubsub', 'aquasec', 'elastic-runtime', 'boomi-data-services-pks', 'stemcells', 'p-appdynamics', 'pivotal-gpdb', 'microsoft-azure-log-analytics-nozzle', 'p-healthwatch', 'pivotal-telemetry-collector', 'aws-services', 'tc-server-3x-runtimes', 'ops-manager', 'p-bosh-backup-and-restore', 'wavefront-nozzle', 'p-isolation-segment', 'pivotal-container-service', 'p-apache-http-server', 'stemcells-ubuntu-xenial', 'p-fim-addon', 'p-concourse', 'pivotal-function-service', 'instana-microservices-application-monitoring', 'twistlock', 'aerospike-ee-on-demand', 'pcf-app-autoscaler', 'appdynamics-platform', 'p-rabbitmq', 'pas-windows'])

    product = models.CharField(max_length=200, help_text=', '.join(PivotalProductList))
    downloaded = models.BooleanField(default=False)