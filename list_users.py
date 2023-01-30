import helper

def list(BM_ID):
  user_details = helper.get_user_id_list(BM_ID)
  print("List of users added to the BM:", BM_ID)
  for user_detail in user_details:
    print(user_detail["user"]["firstName"], user_detail["user"]["lastName"], "(", user_detail["user"]["email"], ")")



