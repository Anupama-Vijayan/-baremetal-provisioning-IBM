import argparse
import shutil
from numpy import array
import yaml
import subprocess
import bm_create
import list_users
import add_users
import delete_users

import sys
# sys.tracebacklimit = 0

def main(classic_username, classic_api_key, command_line=None):
    # app description
    parser = argparse.ArgumentParser(
        description='IBM Cloud Engineering app to help with the ibmcloud baremetal server operations'
    )
    subparsers = parser.add_subparsers(dest='command')

    # To create bm
    create_bm = subparsers.add_parser('create-bm', help='Create Baremetal server')

    create_bm.add_argument(
        '--config-name',
        required=True,
        help='[Required] The (unique) name of the configuration listed in config.yaml'
    )
    create_bm.add_argument(
        '--vlan-id',
        default=None,
        type = int,
        help='VLAN ID'
    )
    create_bm.add_argument(
        '--subnet-id',
        default=None,
        type = int,
        help='Subnet ID'
    )
    create_bm.add_argument(
        '--ssh-keyIDs',
        default=None,
        nargs="+",
        type = int,
        help='SSH Key IDs'
    )
    create_bm.add_argument(
        '--last-index',
        default = 0,
        type= int,
        help='''Index of the last BM created with this config.
                Default value = 0 ie, assuming no BMs with this config is created.
                eg if last index = 0, hostname will be created starting from <hostname>-1
                eg if last index = 2, hostname will be created starting from <hostname>-3'''
    )
    create_bm.add_argument(
        '--count', default= 1,type = int,
        help='The number of BMs of this config to be created. Default value = 1'
    )
    create_bm.add_argument(
        '--verify',
        action='store_true',
        help='Flag denoting whether to verify the order, or not place it'
    )
    # To list users who receive notifications for a bm
    users_list = subparsers.add_parser('list-users', help='List user/s who gets notified on ping failure for a BM')

    users_list.add_argument(
        '--hardwareID',
        required=True,
        help='[Required] The (unique) hardware ID of the Baremetal server'
    )

    # To add user/users to receive notifications for a bm
    users_add = subparsers.add_parser('add-users', help='Add user/s to be notified on ping failure for a BM')

    users_add.add_argument(
        '--hardwareID',
        required=True,
        help='[Required] The (unique) hardware ID of the Baremetal server'
    )
    users_add.add_argument(
        '--users',
        required=True,
        help='List of user email ids (as in your ibm cloud account) to receive the notification . \nThe user email ids should be comma separated. eg: --users "abc@gmail.com,cdb@ibm.com"'
    )

    # To delete user/users to receive notifications for a bm
    users_delete = subparsers.add_parser('delete-users', help='Delete user/s from being notified on ping failure for a BM')

    users_delete.add_argument(
        '--hardwareID',
        required=True,
        help='[Required] The (unique) hardware ID of the Baremetal server'
    )
    users_delete.add_argument(
        '--users',
        required=True,
        help='List of user email ids (as in your ibm cloud account) to be removed from receiving notifications. \nThe user email ids should be comma separated. eg: --users "abc@gmail.com,cdb@ibm.com"'
    )

    # To order a quote using a quote ID
    quote_order = subparsers.add_parser('order-quote', help='Order a quote for a Baremetal server using quote ID')

    quote_order.add_argument(
        '--config-name',
        required=True,
        help='[Required] The (unique) name of the configuration listed in config.yaml'
    )

    quote_order.add_argument(
        '--last-index',
        default = 0,
        type= int,
        help='''Index of the last BM created with this config.
                Default value = 0 ie, assuming no BMs with this config is created.
                eg if last index = 0, hostname will be created starting from <hostname>-1
                eg if last index = 2, hostname will be created starting from <hostname>-3'''
    )

    quote_order.add_argument(
        '--count', default= 1,type = int,
        help='The number of BMs of this config to be created. Default value = 1'
    )

    quote_order.add_argument(
        '--vlan-id',
        default=None,
        type = int,
        help='VLAN ID'
    )

    quote_order.add_argument(
        '--subnet-id',
        default=None,
        type = int,
        help='Subnet ID'
    )

    quote_order.add_argument(
        '--ssh-keyIDs',
        default=None,
        nargs="+",
        type = int,
        help='SSH Key IDs'
    )

    quote_order.add_argument(
        '--verify',
        action='store_true',
        help='Flag denoting whether to verify the order, or not place it'
    )

    # actions for all commands
    args = parser.parse_args(command_line)

    # for create bm
    if args.command == 'create-bm':
      counter = args.count
      start = args.last_index + 1
      vlan = args.vlan_id
      subnet = args.subnet_id
      sshkeys = args.ssh_keyIDs
      for i in range(start, start+counter):
        print("####################################################")
        bm_create.create(args.config_name,i, args.verify, vlan, subnet, sshkeys)
      print("####################################################")

    # to list users to receive notifications
    elif args.command == 'list-users':
      list_users.list(args.hardwareID)

    # to add users to receive notifications
    elif args.command == 'add-users':
      add_users.add(args.hardwareID, args.users)

    # to delete users to receive notifications
    elif args.command == 'delete-users':
      delete_users.delete(args.hardwareID, args.users)

    elif args.command == 'order-quote':
      counter = args.count
      start = args.last_index + 1
      vlan = args.vlan_id
      subnet = args.subnet_id
      sshkeys = args.ssh_keyIDs
      for i in range(start, start+counter):
        print("####################################################")
        bm_create.order_quote(args.config_name,i, args.verify, vlan, subnet, sshkeys, classic_username, classic_api_key)
      print("####################################################")
    else:
      sys.exit("Missing parameters. Use '-h' help option for details")

if __name__ == '__main__':

  if shutil.which('ibmcloud') is None :
    sys.exit("ERROR: Install ibmcloud cli")

  # ibm login
  with open('credentials.yaml', 'r') as f:
    doc = yaml.full_load(f)

  if "api-key" not in doc:
    raise Exception('API Key missing in credentials.yaml')
  if not doc["api-key"]:
    raise Exception('API Key value missing in credentials.yaml')

  login = subprocess.run(["ibmcloud", "login", "--apikey", doc["api-key"]], stdout=subprocess.PIPE)
  if login.returncode !=0:
    sys.exit("ERROR: Failed to login to ibmcloud. Check your api key.")
  print("Successfully logged in to ibmcloud\n")

  main(doc["classic-username"], doc["classic-api-key"])