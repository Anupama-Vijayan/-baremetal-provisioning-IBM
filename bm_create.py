import yaml
import subprocess
import json
from os.path import exists
import sys
import SoftLayer
from SoftLayer.managers.ordering import OrderingManager

class Quote():
  def __init__(self, classic_username, classic_api_key):
    self.client = SoftLayer.create_client_from_env(username=classic_username, api_key=classic_api_key)
    self.mgr = OrderingManager(self.client)
    debugger = SoftLayer.DebugTransport(self.client.transport)
    self.client.transport = debugger

def create(config_name, index, verify, vlan, subnet, sshKeyIds):
  if exists('config.yaml'):
    with open('config.yaml', 'r') as file:
      configuration = yaml.safe_load(file)[config_name]
  else:
    sys.exit("ERROR: configuration yaml file `config.yaml` is missing.")

  ic_cmd= ["ibmcloud","sl","order","place"]

  args_arr = []
  order_items_arr = []
  options_arr = ["--complex-type", "SoftLayer_Container_Product_Order_Hardware_Server"]

  if verify:
    options_arr.append("--verify")

  extras_opts = ["--extras", {}]
  extras_opts[1]["hardware"] = []
  extras_opts[1]["hardware"].append({})
  extras_opts[1]["sshKeys"] = []
  extras_opts[1]["sshKeys"].append({})

  args_arr.append(configuration["package-keyname"])
  args_arr.append(configuration["location"])

  for k,v in configuration.items():
    if k=="package-keyname" or k == "location":
      continue
    if k=="billing":
      options_arr.extend(["--billing",v])
      continue
    if k=="preset":
      options_arr.extend(["--preset",v])
      continue
    if k=="hostname":
      extras_opts[1]["hardware"][0]["hostname"] = v  + "-" + str(index)
      continue
    if k=="domain":
      extras_opts[1]["hardware"][0]["domain"] = v
      continue
    order_items_arr.append(v)

  ic_cmd.extend(args_arr)
  ic_cmd.append(",".join(order_items_arr))
  ic_cmd.extend(options_arr)
  if vlan is not None or subnet is not None:
    extras_opts[1]["hardware"][0]["primaryBackendNetworkComponent"]= {"networkVlan": {}}
    if vlan is not None:
      extras_opts[1]["hardware"][0]["primaryBackendNetworkComponent"]["networkVlan"]= {"id":int(vlan)}
    if subnet is not None:
      extras_opts[1]["hardware"][0]["primaryBackendNetworkComponent"]["networkVlan"]["primarySubnet"]= {"id": int(subnet)}
  if sshKeyIds is not None:
    extras_opts[1]["sshKeys"][0]["sshKeyIds"] = sshKeyIds
  ic_cmd.append(extras_opts[0])
  ic_cmd.append(json.dumps(extras_opts[1]))

  status = subprocess.run(ic_cmd)
  if status.returncode == 0:
    if verify:
      print ("Name:", configuration["hostname"] + "-" + str(index), "\nVerify request to create BM server")
    else:
      print("Name:", configuration["hostname"] + "-" + str(index), "\nSubmitted request to create BM server")
  else:
    print("Error: Failed to order. Command used:", " ".join(ic_cmd))

def order_quote(config_name, index, verify, vlan, subnet, sshKeyIds, classic_username, classic_api_key):
  if exists('config.yaml'):
    with open('config.yaml', 'r') as file:
      configuration = yaml.safe_load(file)[config_name]
  else:
    sys.exit("ERROR: configuration yaml file `config.yaml` is missing.")\
  
  quote_id = config_name[1:8]

  quote = Quote(classic_username, classic_api_key)
  extras = {}
  extras["hardware"] = []
  extras["hardware"].append({})
  extras["sshKeys"] = []
  extras["sshKeys"].append({})

  extras["hardware"][0]["hostname"] = configuration["hostname"] + "-" + str(index)
  extras["hardware"][0]["domain"] = configuration["domain"]
  
  if vlan is not None or subnet is not None:
    extras["hardware"][0]["primaryBackendNetworkComponent"]= {"networkVlan": {}}
    if vlan is not None:
      extras["hardware"][0]["primaryBackendNetworkComponent"]["networkVlan"]= {"id":int(vlan)}
    if subnet is not None:
      extras["hardware"][0]["primaryBackendNetworkComponent"]["networkVlan"]["primarySubnet"]= {"id": int(subnet)}
  if sshKeyIds is not None:
    extras["sshKeys"][0]["sshKeyIds"] = sshKeyIds
  
  if verify:
    order_return = quote.mgr.verify_quote(quote_id, extras)
  else:
    order_return = quote.mgr.order_quote(quote_id, extras)