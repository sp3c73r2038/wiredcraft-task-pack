resource "alicloud_key_pair" "default_key" {
  key_pair_name   = "default-key"
  public_key = var.ssh_public_key
}
