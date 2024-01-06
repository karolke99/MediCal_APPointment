####################################
# Openstack provider config
####################################

openstack_user              = ""
openstack_tenant_id         = ""
openstack_auth_url          = ""
openstack_region            = ""
openstack_user_domain_name  = ""


app_name                    = "medical_appointment"
http_protocol_port          = 8080

availability_zone           = "az1"


####################################
# Infrastructure config
####################################

subnet_cidr                 = "192.168.0.0/24"
vm_count                    = 2
ssh_key_name                = "my_key"
vm_flavor_name              = "C2R4"
vm_volume_size              = 20