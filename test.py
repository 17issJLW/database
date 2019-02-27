import requests
server = "http://127.0.0.1:8000"
# server = "http://211.159.186.47:8000"
header = {"Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6Ilx1N2JhMVx1NzQwNlx1NTQ1OCJ9.UoPLDkVwzLLHcX41dBfgIX0YCFFWf2TJ_4YUsFwpOmU"}
data = {"username":"team2","password":"team2","name":"team23"}
# data = {"username":"单杠","sex":"男","age_group":"9-10"}
# data = {"id":2}
r = requests.put(server+"/sport/team/5/",headers=header,data=data)
print(r.text)