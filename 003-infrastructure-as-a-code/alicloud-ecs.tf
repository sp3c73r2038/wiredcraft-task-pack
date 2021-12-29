# server webapi
resource "alicloud_instance" "webapi" {
  # cn-shanghai
  availability_zone = "cn-shanghai-g"
  security_groups   = [alicloud_security_group.group_default.id]
  host_name         = "webapi"

  instance_charge_type       = "PostPaid"

  # series III
  instance_type              = "ecs.t5-lc1m1.small"
  system_disk_category       = "cloud_ssd"
  image_id                   = "debian_9_09_64_20G_alibase_20190702.vhd"
  instance_name              = "webapi"
  vswitch_id                 = alicloud_vswitch.vswitch_default.id
  internet_max_bandwidth_out = 100
}

resource "alicloud_key_pair_attachment" "webapi_sshkey" {
  key_pair_name = alicloud_key_pair.default_key.id
  instance_ids  = [alicloud_instance.webapi.id]
}

output "webapi_ip" {
  value = alicloud_instance.webapi.public_ip
}

# server database
resource "alicloud_instance" "database" {
  # cn-shanghai
  availability_zone = "cn-shanghai-g"
  security_groups   = [alicloud_security_group.group_default.id]
  host_name         = "database"

  instance_charge_type       = "PostPaid"

  # series III
  instance_type              = "ecs.t5-lc1m1.small"
  system_disk_category       = "cloud_ssd"
  image_id                   = "debian_9_09_64_20G_alibase_20190702.vhd"
  instance_name              = "database"
  vswitch_id                 = alicloud_vswitch.vswitch_default.id
  internet_max_bandwidth_out = 100
}

resource "alicloud_key_pair_attachment" "database_sshkey" {
  key_pair_name = alicloud_key_pair.default_key.id
  instance_ids  = [alicloud_instance.database.id]
}

output "database_ip" {
  value = alicloud_instance.database.public_ip
}
