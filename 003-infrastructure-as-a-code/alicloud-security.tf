resource "alicloud_security_group" "group_default" {
  name        = "default-group"
  description = "default-group all instances should use"
  vpc_id      = alicloud_vpc.vpc_default.id
}

resource "alicloud_security_group_rule" "allow_ssh" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "22/22"
  priority          = 1
  security_group_id = alicloud_security_group.group_default.id
  cidr_ip           = "0.0.0.0/0"
}
resource "alicloud_security_group_rule" "allow_webapi" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "3000/3000"
  priority          = 1
  security_group_id = alicloud_security_group.group_default.id
  cidr_ip           = "0.0.0.0/0"
}
resource "alicloud_security_group_rule" "allow_ping" {
  type              = "ingress"
  ip_protocol       = "icmp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "0/65535"
  priority          = 1
  security_group_id = alicloud_security_group.group_default.id
  cidr_ip           = "0.0.0.0/0"
}
