import subprocess
import json

def get_user_id_list(BM_ID):
  id = f"'[{BM_ID}]'"
  command = ["ibmcloud","sl","call-api","SoftLayer_User_Customer_Notification_Hardware","findByHardwareId", "--parameters", id]
  user_json = subprocess.run(" ".join(command), shell=True,stdout=subprocess.PIPE)
  user_details = json.loads(user_json.stdout.decode('utf-8'))
  return user_details

def get_account_user_list():
  command = ["ibmcloud","sl","user","list","--output", "JSON"]
  user_json = subprocess.run(command,stdout=subprocess.PIPE)
  return json.loads(user_json.stdout.decode('utf-8'))

def clean_users_Array(users):
  usersArray= users.split(",")
  for i in range(len(usersArray)):
    usersArray[i] = usersArray[i].lower().strip()
  return usersArray