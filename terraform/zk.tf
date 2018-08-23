resource "digitalocean_droplet" "zk_node" {
  count              = 2
  image              = "${var.ubuntu}"
  ssh_keys           = "${var.ssh_keys}"
  size               = "${var.size_2g}"
  region             = "${var.region}"
  name               = "zk-node-${count.index}"
  private_networking = true
}
