# Baremetal provisioning in IBM Cloud

Resources on classic infrastructure are organized into packages of different kinds.
For creating any classic infrastructure, we need values for 2 parameters- _package type_ and _package keyname_

While creating a Baremetal resource the _Package type_ we use is `BARE_METAL_CPU`.
Using this _package type_ we can use the `ibmcloud sl` command ( mentioned in below sections) to list all the unique _package keynames_ available for `BARE_METAL CPU`.
For example _package keyname_ for "Dual Intel Xeon Processor Cascade Lake Scalable Family 4 Drives" is `DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES`

For a particular _package keyname_ e.g `DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES`, you can list all the required fields (categories) and optional fields(categories). The different values available for each of these fields (categories) for creating a BM of the selected _package keyname_ can be retreived using the `ibmcloud sl` commands ( mentioned in below sections)

Each category will provide different options to choose.
For example: `os` category will list different OS flavors available which can be installed for the BM.

All the data you get from above can be used to construct a `config.yaml` file (sample provided) with a **unique** config name. The app can be used to create multiple BMs with a single command using `--count` option.

You can get your `VLAN ID` or `SUBNET ID` which can be used when creating a BM by querying `ibmcloud sl` command ( mentioned in below sections) or from the VLAN details page of the IBM cloud account UI.

You can get your `SSH KEY IDs` which can be used when creating a BM by querying `ibmcloud sl` command ( mentioned in below sections) or from the VLAN details page of the IBM cloud account UI.

After provisioning the BM succesfully, you can use the script to list, add or remove users who can be notified on ping failure for a BM.

## Prerequisites

- Install all the python dependencies listed in requirements.txt

```
pip3 install -r requirements.txt
```

- Create a configuration file `config.yaml` and a secret file `credentials.yaml` in the project folder.

_config.yaml_ : This file will have all the configurations listed as in the given sample file.

_credentials.yaml_: This file will have your api key, which will be used to log in to your ibmcloud account. Use the sample file provided.

## To run it locally

Command:

```
python3 main.py create-bm --config-name <name-from-yaml> --count <int count> --last-index <last-index of previously provisioned BM> --vlan-id <vlan ID> --subnet-id <subnet ID> --ssh-keyIDs <ssh key IDs> --verify

python3 main.py list-users --hardwareID <hardwareID>

python3 main.py add-users --hardwareID <hardwareID> --users "<userEmailId1>,<userEmailId2>"

python3 main.py delete-users --hardwareID <hardwareID> --users "<userEmailId1>,<userEmailId2>"

python3 main.py order-quote --config-name <name-from-yaml> --count <int count> --last-index <last-index of previously provisioned BM> --vlan-id <vlan ID> --subnet-id <subnet ID> --ssh-keyIDs <ssh key IDs> --verify
```

- App description

```
python3 main.py -h
Successfully logged in to ibmcloud

usage: main.py [-h] {create-bm,list-users,add-users,delete-users} ...

IBM Cloud Engineering app to help with the ibmcloud baremetal server operations

positional arguments:
  {create-bm,list-users,add-users,delete-users}
    create-bm           Create Baremetal server
    list-users          List user/s who gets notified on ping failure for a BM
    add-users           Add user/s to be notified on ping failure for a BM
    delete-users        Delete user/s from being notified on ping failure for a BM
    order-quote         Order a quote for a Baremetal server using quote ID

optional arguments:
  -h, --help            show this help message and exit
```

## Provision Baremetal

```
❯ python3 main.py create-bm -h
Successfully logged in to ibmcloud

usage: main.py create-bm [-h] --config-name CONFIG_NAME [--vlan-id VLAN_ID] [--last-index LAST_INDEX] [--count COUNT]
                         [--verify]

optional arguments:
 -h, --help            show this help message and exit
  --config-name CONFIG_NAME
                        [Required] The (unique) name of the configuration listed in config.yaml
  --vlan-id VLAN_ID     VLAN ID
  --subnet-id SUBNET_ID
                        Subnet ID
  --ssh-keyIDs SSH_KEYIDS [SSH_KEYIDS ...]
                        SSH Key IDs
  --last-index LAST_INDEX
                        Index of the last BM created with this config. Default value = 0 ie, assuming no BMs with this config is created.
                        eg if last index = 0, hostname will be created starting from <hostname>-1 eg if last index = 2, hostname will be
                        created starting from <hostname>-3
  --count COUNT         The number of BMs of this config to be created. Default value = 1
  --verify              Flag denoting whether to verify the order, or not place it
```

**Example: Create a Baremetal server of configuration example_config**

Following command will create a BM server of name using the configurations for `example_config` listed in the config.yaml file. Since the count is 2, this will create 2 BM servers with prefix `host-name` appended with the numbers starting from the last-index value 4, ie new names end with `5` and `6` as shown in example below.

```
python3 main.py create-bm --config-name example_config --vlan-id 1234 --subnet-id 4567 --count 2 --last-index 4

Successfully logged in to ibmcloud
####################################################
This action will incur charges on your account. Continue?> yes

ID        123455
Created   2022-02-15T20:21:00Z
Status    PENDING_AUTO_APPROVAL
Name: bm-8260-192-5
Submitted request to create BM server
####################################################
This action will incur charges on your account. Continue?> yes

ID        123456
Created   2022-02-15T20:21:00Z
Status    PENDING_AUTO_APPROVAL
Name: bm-8260-192-6
Submitted request to create BM server
####################################################
```

_Note 1:_
You can provide both VLAN ID and SUBNET ID or either of them as required.

```
python3 main.py create-bm --config-name example_config --vlan-id 1234 --subnet-id 4567
```

or

```
python3 main.py create-bm --config-name example_config --subnet-id 4567
```

or

```
python3 main.py create-bm --config-name example_config --vlan-id 1234
```

_Note 2:_
You can provide SSH Key IDs

```
python3 main.py create-bm --config-name example_config --ssh-keyIDs 1234567 4567890 3456789
```

_Note 3:_
If not specified, default value for count is 1 and default value for last-index is 0. `--count` and `-last-index` are not mandatory options.

```
python3 main.py create-bm --config-name example_config
```

Following example will create 2 BMs starting with the default last-index=0 as `bm-example_config-1` and `bm-example_config-2`

```
python3 main.py create-bm --config-name example_config --count 2
```

Following example will create `bm-example_config-3` as default count= 1

```
python3 main.py create-bm --config-name example_config --last-index 2
```

You can verify the config values before placing the order by using `--verify` flag

```
python3 main.py create-bm --config-name example_config --verify
```

or

```
python3 main.py create-bm --config-name example_config --count 2 --last-index 4 --verify
```

## List users

```
❯ python3 main.py list-users -h
Successfully logged in to ibmcloud

usage: main.py list-users [-h] --hardwareID HARDWAREID

optional arguments:
  -h, --help            show this help message and exit
  --hardwareID HARDWAREID
                        [Required] The (unique) hardware ID of the Baremetal server
```

**Example to list users**

```
python3 main.py list-users --hardwareID <hardwareID>

```

## Add users

```
❯ python3 main.py add-users -h
Successfully logged in to ibmcloud

usage: main.py add-users [-h] --hardwareID HARDWAREID --users USERS

optional arguments:
  -h, --help            show this help message and exit
  --hardwareID HARDWAREID
                        [Required] The (unique) hardware ID of the Baremetal server
  --users USERS         List of user email ids (as in your ibm cloud account) to receive the notification . The user email ids
                        should be comma separated. eg: --users "abc@gmail.com,cdb@ibm.com"
```

**Example to add users**

```
python3 main.py add-users --hardwareID <hardwareID> --users "abcd@ibm.com"

python3 main.py add-users --hardwareID <hardwareID> --users "abcd@ibm.com,bcde@gmail.com"
```

\*Note:

- If any of the users in the list of comma separated users are already added to the BM's notification list, the ibmcloud CLI/API fails to add all the given users.
- The `hardwareID` can be found via the Overview page of the device in IBM Cloud UI or you can use `ibmcloud sl hardware list` to get a list of all the hardware servers in your account and their details.
- The email id for the users can be found here: https://cloud.ibm.com/user

## Remove users

```
❯ python3 main.py delete-users -h
Successfully logged in to ibmcloud

usage: main.py delete-users [-h] --hardwareID HARDWAREID --users USERS

optional arguments:
  -h, --help            show this help message and exit
  --hardwareID HARDWAREID
                        [Required] The (unique) hardware ID of the Baremetal server
  --users USERS         List of user email ids (as in your ibm cloud account) to be removed from receiving notifications . The
                        user email ids should be comma separated. eg: --users "abc@gmail.com,cdb@ibm.com"
```

**Example to remove users**

```
python3 main.py delete-users --hardwareID <hardwareID> --users "abcd@ibm.com"

python3 main.py delete-users --hardwareID <hardwareID> --users "abcd@ibm.com,bcde@gmail.com"
```

\*Note:

- The `hardwareID` can be found via the Overview page of the device in IBM Cloud UI or you can use `ibmcloud sl hardware list` to get a list of all the hardware servers in your account and their details.
- The email id for the users can be found here: https://cloud.ibm.com/user

## Order Quote

```
❯ python3 main.py order-quote -h
Successfully logged in to ibmcloud

python3 main.py order-quote --config-name <name-from-yaml> --count <int count> --last-index <last-index of previously provisioned BM> --vlan-id <vlan ID> --subnet-id <subnet ID> --ssh-keyIDs <ssh key IDs> --verify
                           [--verify]

optional arguments:
  -h, --help            show this help message and exit
  --config-name CONFIG_NAME
                        [Required] The (unique) name of the configuration listed in config.yaml
  --vlan-id VLAN_ID     VLAN ID
  --subnet-id SUBNET_ID
                        Subnet ID
  --ssh-keyIDs SSH_KEYIDS [SSH_KEYIDS ...]
                        Subnet ID
  --last-index LAST_INDEX
                        Index of the last BM created with this config. Default value = 0 ie, assuming no BMs with this config is created.
                        eg if last index = 0, hostname will be created starting from <hostname>-1 eg if last index = 2, hostname will be
                        created starting from <hostname>-3
  --count COUNT         The number of BMs of this config to be created. Default value = 1
  --verify              Flag denoting whether to verify the order, or not place it
```

**Example to order quote**

_Note:_
You can provide both VLAN ID and SUBNET ID or either of them as required.

```
python3 main.py order-quote --config-name example_config --vlan-id 1234 --subnet-id 4567
```

or

```
python3 main.py order-quote --config-name example_config --subnet-id 4567
```

or

```
python3 main.py order-quote --config-name example_config --vlan-id 1234
```

_Note 2:_
If not specified, default value for count is 1 and default value for last-index is 0. `--count` and `-last-index` are not mandatory options.

```
python3 main.py order-quote --config-name example_config
```

Following example will create 2 BMs starting with the default last-index=0 as `bm-example_config-1` and `bm-example_config-2`

```
python3 main.py order-quote --config-name example_config --count 2
```

Following example will create `bm-example_config-3` as default count= 1

```
python3 main.py order-quote --config-name example_config --last-index 2
```

You can verify the config values before placing the order by using `--verify` flag

```
python3 main.py order-quote --config-name example_config --verify
```

## Softlayer CLI commands

1. Lists the package keynames.

```
ibmcloud sl order package-list --package-type BARE_METAL_CPU
```

eg:

```
id: 1105
name: Dual Intel Xeon Processor Cascade Lake Scalable Family (4 Drives)
keyName: DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES
type: BARE_METAL_CPU
```

Here the package keyname for _Dual Intel Xeon Processor Cascade Lake Scalable Family (4 Drives)_ is `DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES`

2. Lists the locations where this package keyname is available.

```
ibmcloud sl order package-locations DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES
```

eg:

```
id: 2178495
dc: sjc04
description: SJC04 - San Jose
keyName: SANJOSE04
```

Here the location keyname for _DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES_ is `SANJOSE04`

3. Lists all the required fields to be set to provision a baremetal of type _DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES_

```
ibmcloud sl order category-list DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES --required
```

4. Lists all the fields that are available while provisioning a baremetal of type _DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES_

```
ibmcloud sl order category-list DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES
```

5. Lists all the available options for package name _DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES_ for each of the order items like server, os, bandwidth etc.

```
ibmcloud sl order item-list DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES
```

**Note:**

To list all available options for a category code use the `--category` filter.
For example, to get the keyname for Operating System `OS _Windows Server 2022 Standard Edition (64 bit)` use the below command to list all available os flavors for package name _DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES_

```
ibmcloud sl order item-list DUAL_INTEL_XEON_PROCESSOR_CASCADE_LAKE_SCALABLE_FAMILY_4_DRIVES --category os
```

From the output look for _description_: `Windows Server 2022 Standard Edition (64 bit)` and the _keyname_ to be used while ordering the BM is `OS_WINDOWS_2022_FULL_STD_64_BIT`

6. Lists all the hardware servers. You can get the hardware ID from here.

```
ibmcloud sl hardware list
```

7. Deletes the hardware server with the id _ID_

```
ibmcloud sl hardware cancel <ID>
```

8. To retrieve the _VLAN ID_

```
ibmcloud sl vlan list | grep <unique name or number of your VLAN>
```

8. To retrieve the _SUBNET ID_

```
ibmcloud sl subnet list
```

9. To retrieve the _SSH Key IDs_

```
ibmcloud sl security sshkey-list
```
