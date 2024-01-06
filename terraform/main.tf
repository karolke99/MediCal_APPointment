provider "openstack" {
    auth_url            = var.openstack_auth_url
    user_name           = var.openstack_user
    password            = var.openstack_password
    region              = var.openstack_region
    user_domain_name    = var.openstack_user_domain_name
    tenant_id           = var.openstack_tenant_id

    use_octavia         = true
}

resource "openstack_networking_network_v2" "net" {
    name            = var.app_name
    admin_state_up  = true
}

resource "openstack_networking_subnet_v2" "subnet" {
    name        = "${ var.app_name }_subnet"
    network_id  = "${openstack_networking_network_v2.net.id}"
    cidr        = var.subnet_cidr
    ip_version  = 4
}

resource "openstack_networking_router_v2" "router" {
    name                = "${ var.app_name }_router"
    admin_state_up      = true
    external_network_id = "2b56e154-7dfc-4c2c-9373-1ef768f5adbb"
}

resource "openstack_networking_router_interface_v2" "router_internal_interface" {
    router_id = "${openstack_networking_router_v2.router.id}"
    subnet_id = "${openstack_networking_subnet_v2.subnet.id}"
}

resource "openstack_networking_secgroup_v2" "sg" {
    name            = var.app_name
    description     = "${var.app_name}_sec_group"
}

resource "openstack_compute_instance_v2" "app" {
    count               = var.vm_count
    name                = "${ var.app_name }_${count.index}"
    flavor_name         = var.vm_flavor_name
    key_pair            = var.ssh_key_name

    security_groups     = ["${openstack_networking_secgroup_v2.sg.name}"]
    availability_zone   = var.availability_zone

    block_device {
        uuid                    = "210c47a5-e354-447c-8793-dfc1a1c6dbe9"
        source_type             = "image"
        volume_size          = var.vm_volume_size
        boot_index              = 0
        destination_type        = "volume"
        delete_on_termination   = true
    }

    network {
        name = "${openstack_networking_network_v2.net.name}"
    }

    depends_on = [openstack_networking_subnet_v2.subnet]
}

resource "openstack_lb_loadbalancer_v2" "load_balancer"{
  vip_subnet_id  = "${openstack_networking_subnet_v2.subnet.id}"
  name           = "${ var.app_name }_lb"
}

resource "openstack_lb_listener_v2" "listener" {
  name              = "${ var.app_name }_listener"
  loadbalancer_id   = "${openstack_lb_loadbalancer_v2.load_balancer.id}"
  protocol          = "HTTP"
  protocol_port     = var.http_protocol_port
}

resource "openstack_lb_pool_v2" "pool" {
  listener_id = "${openstack_lb_listener_v2.listener.id}"
  name        = "${ var.app_name }_pool"
  lb_method   = "ROUND_ROBIN"
  protocol    = "HTTP"
}

resource "openstack_lb_monitor_v2" "health_monitor" {
  pool_id     = "${openstack_lb_pool_v2.pool.id}"
  type        = "HTTP"
  delay       = 5
  max_retries = 3
  timeout     = 5
}

resource "openstack_lb_member_v2" "members" {
  count         = var.vm_count
  pool_id       = "${openstack_lb_pool_v2.pool.id}"
  subnet_id     = "${openstack_networking_subnet_v2.subnet.id}"
  protocol_port = var.http_protocol_port
  address       = "${openstack_compute_instance_v2.app[count.index].access_ip_v4}"
}

resource "openstack_compute_floatingip_v2" "lb_floating_ip" {
  pool  = "internal_ip_02"
}

resource "openstack_networking_floatingip_associate_v2" "lb_fip_attach" {
  floating_ip = "${openstack_compute_floatingip_v2.lb_floating_ip.address}"
  port_id     = "${openstack_lb_loadbalancer_v2.load_balancer.vip_port_id}"
}
