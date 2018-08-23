variable "ssh_keys" {
  description = "SSH keys to add to servers"
  default     = [22385804] # 'dataops'
}

variable "region" {
  description = "DO datacenter to use"
  default     = "fra1"
}


# not much to modify below

variable "ubuntu" {
  description = "Ubuntu Xenial image used for all VMs"
  default     = "ubuntu-16-04-x64"
}

variable "size_2g" {
  description = "DO VM with 2GB of RAM"
  default     = "s-2vcpu-2gb"
}

variable "size_16g" {
  description = "DO VM with 16GB of RAM"
  default     = "s-6vcpu-16gb"
}
