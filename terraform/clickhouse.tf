resource "digitalocean_droplet" "clickhouse_node" {
  count              = 4
  image              = "${var.ubuntu}"
  ssh_keys           = "${var.ssh_keys}"
  size               = "${var.size_16g}"
  region             = "${var.region}"
  name               = "clickhouse-${count.index}"
  private_networking = true
}
