import os
import sys
import json

if os.environ.get('TF_STATE'):
    env_state = os.environ.get('TF_STATE')
else:
    env_state = "terraform.tfstate"

state_file = os.path.join(os.getcwd(), env_state)

with open(state_file) as f:
    state_src = json.load(f)
resources = state_src['modules'][0]['resources']

groups = {}
for res_id, res in resources.iteritems():
    if res['type'] == 'digitalocean_droplet':
        # Terraform uses names like "digitalocean_droplet.clickhouse_node.3" for resources,
        # so we need to build node groups based on those variables.
        splitted = res_id.split('.')
        group = splitted[1]
        if len(splitted) > 2:
            item = splitted[2]
        else:
            item = None
        node_data = {
            'internal_ip': res['primary']['attributes']['ipv4_address_private'],
            'hostname': res['primary']['attributes']['name'],
        }
        # Specify ID only if there is more than one resource in group
        if item:
            node_data['item_id'] = item
        group_data = groups.get(group, {'hosts': {}})
        ip = res['primary']['attributes']['ipv4_address']
        group_data['hosts'][ip] = node_data
        groups[group] = group_data

for group, group_details in groups.iteritems():
    # Ubuntu 16.04 image from DO doesn't have Python 2 interpreter included, so to make
    # Ansible working we need to use Python 3 binary for all nodes.
    # It can be actually included to `node_data` variable in the cycle above (while
    # processing inventory, Ansible merges all global and host variables to a single
    # dictionary) but I kept it separated for slightly more human readable inventory.json
    groups[group]['vars'] = {
        'ansible_python_interpreter': '/usr/bin/python3'
    }

print(json.dumps(groups, indent=4, sort_keys=True))
