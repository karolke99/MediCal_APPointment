####################################
# Openstack provider config
####################################

variable "openstack_user" {
    description = "Openstack user name"
    type        = string
}

variable "openstack_password" {
    description = "Openstack user password"
    sensitive   = true
    type        = string
}

variable "openstack_tenant_id" {
    description = "Openstack project id"
    type        = string
}

variable "openstack_auth_url" {
    description = "Openstack region authentication endpoint"
    type        = string
}

variable "openstack_region" {
    description = "Openstack region name"
    type        = string
}

variable "openstack_user_domain_name" {
    description = "Openstack user domain name"
    type        = string
}


####################################
# Infrastructure config
####################################

variable "app_name" {
    description = "App name"
    default     = "app"
    type        = string
}



variable "subnet_cidr" {
    description = "Subnet CIDR address."
    default     = "192.168.0.0/24"
    type        = string
}

variable "vm_name" {
    description = "VM name"
    default     = "app"
    type        = string
}

variable "availability_zone" {
    description = "VM availability zone"
}

variable "vm_count" {
    description = "Number of vms to create"
    type        = number
}

variable "ssh_key_name" {
    description = "SSH public key to use for vm in cloud-init"
    type        = string
}

variable "vm_flavor_name" {
    description = "VM flavor name"
    type        = string
    default     = "C2R4"
}

variable "vm_volume_size" {
    description = "Size of boot volume for VM in GiB"
    type        = number
    default     = 20
}

variable "http_protocol_port" {
    description = "App port"
    type        = number
}