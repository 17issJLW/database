import requests
server = "http://127.0.0.1:8000"
# server = "http://211.159.186.47"
# header = {"Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoidGVhbSIsInVzZXJuYW1lIjoidGVhbTIiLCJuYW1lIjoidGVhbTIzIn0.9Ihzn6QtpDMBPyeC_x2FaCApk1dOHzxsZYTN0pbYHSc"}
# data = {"username":"team2","password":"team2","name":"type"}
header = {"Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6Ilx1N2JhMVx1NzQwNlx1NTQ1OCJ9.UoPLDkVwzLLHcX41dBfgIX0YCFFWf2TJ_4YUsFwpOmU"}
data = {"name":"单杠","sex":"男","age_group":"9-10"}
# data = {"num":3,"competition":2}
# data = {"group":1}
r = requests.put(server+"/sport/sign_up/3/",headers=header,data=data)
print(r.text)