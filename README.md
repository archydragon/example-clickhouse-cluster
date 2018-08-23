# example-clickhouse-cluster

Temporary result of the experiments with automatic setting up Clickhouse cluster
with Terraform and Ansible.

If you found this by accident, feel free to use as a "template" for more
real-world deployments. But mind the comments. Also, you could find some useful
stuff in [garbage.txt](garbage.txt).

Disclaimer: I don't position myself as an expert of any used technology
so if you find anything wrong, feel free to ping me back in issues/PRs.

### How to use, shortly

Of course, you'll need [Terraform](https://www.terraform.io/) and [Ansible](https://www.ansible.com/)
to set it up. Only [DigitalOcean](https://www.digitalocean.com/) as VPS provider
is supported.

```bash
export DIGITALOCEAN_TOKEN="your-do-hex-token"
cd terraform
terraform plan # to ensure that everything is gonna be ok
terraform apply
cd ..
export TF_STATE="terraform/terraform.tfstate"
python inventory.py > inventory.json
# hereby default, Ansible expects that you have your private SSH key under rsa_key.pem
ansible-playbook playbooks/deploy_zk.yml
ansible-playbook playbooks/deploy_clickhouse.yml
```

### Necessary explainations

`inventory.json` and `terraform/terraform.tfstate` file are just stored as
examples, don't try to access those nodes, they're dead for ages, huh.

#### Terraform sources

You'll need to update DO SSH key ID in `vars.tf` to be actually able to deploy
things with Ansible. If you are not happy with predefined DO datacenter ID and
images, feel free to change them.

In `zk.tf` and `clickhouse.tf` files the only thing which could be really
interesting, is the number of machines for each application. After initial creation
and deployment are done, you can modify those files, re-run `terraform apply`,
re-run Ansible deployment playbooks and get grown (or shrinked) cluster.

#### inventory.py

Ansible supports dynamic inventory sources which could be useful for generating
inventories from Terraform state files. There is [terraform-inventory](https://github.com/adammck/terraform-inventory)
project with basic functionality but it didn't work here just because I needed
to know IDs of generated machines (for ZK and Clickhouse configurations). I was
too lazy to implement "proper" dynamic inventory application which can be passed
as a parameter to Ansible, so I did `inventory.py` generator from scratch. It is
very simple, really. Go through its code, and find an example of generated inventory
under `inventory.json`. Yes, only DO Terraform state resource attributes are
supported.

#### Ansible playbooks

Rely on host variables provided by inventory generator mentioned above. Aside of
that, they're pretty simple aswell. Zookeeper is configured to use only internal
network addresses, Clickhouse is barely configured at all.
