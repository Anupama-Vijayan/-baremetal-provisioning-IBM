import json
import subprocess
import helper

def add(BM_ID, users):
  user_dict_array = []
  cmd_array =[]

  user_json = helper.get_account_user_list()
  usersArray = helper.clean_users_Array(users)

  for user in user_json:
    if user["email"].lower() in usersArray:
      print("Adding user **", user["displayName"],"(id:" ,user["id"],")** to receive notifications for BM",BM_ID)
      user_id = user["id"]
      user_dict = {"userId":user_id,"hardwareId":BM_ID}
      user_dict_array.append(user_dict)
  cmd_array.append(user_dict_array)
  add_user_bm(cmd_array, user_dict_array)

def add_user_bm(cmd_array, user_dict_array):
  command_params =  json.dumps(cmd_array)
  command = ["ibmcloud","sl","call-api","SoftLayer_User_Customer_Notification_Hardware","createObjects", "--parameters", command_params]
  status = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
  if status.returncode == 0 and len(user_dict_array) > 0:
    print("\nSuccessfully added users.")
  else:
    print("\nError:",status.stderr.decode('utf-8'), "\n Failed Command:", " ".join(command))

