resource "alicloud_vpc" "vpc_default" {
  vpc_name   = "vpc-default"
  cidr_block = "192.168.0.0/16"
}

resource "alicloud_vswitch" "vswitch_default" {
  vpc_id     = alicloud_vpc.vpc_default.id
  cidr_block = "192.168.233.0/24"
  zone_id    = "cn-shanghai-g"
}
