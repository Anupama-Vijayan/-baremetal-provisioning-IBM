import helper
import subprocess
import json

def delete(BM_ID, users):
  user_dict_array = []
  cmd_array =[]

  usersArray = helper.clean_users_Array(users)
  # print(usersArray)

  user_details = helper.get_user_id_list(BM_ID)

  for user_detail in user_details:
    if user_detail["user"]["email"].lower() in usersArray:
      print("Deleting user **", user_detail["user"]["firstName"], user_detail["user"]["lastName"], "(", user_detail["user"]["email"], ")","** from receiving notifications for BM",BM_ID)
      user_dict = {"id":user_detail["id"],"hardwareId":BM_ID}
      user_dict_array.append(user_dict)
  cmd_array.append(user_dict_array)
  delete_user_bm(cmd_array, user_dict_array)

def delete_user_bm(cmd_array, user_dict_array):
  command_params =  json.dumps(cmd_array)
  command = ["ibmcloud","sl","call-api","SoftLayer_User_Customer_Notification_Hardware","deleteObjects", "--parameters", command_params]
  status = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
  if status.returncode == 0 and len(user_dict_array) > 0:
    print("\nSuccessfully deleted users.")
  else:
    print("\nError:",status.stderr.decode('utf-8'), "\n Failed Command:", " ".join(command))
