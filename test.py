import requests
server = "http://127.0.0.1:8000"
header = {"Token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIiwibmFtZSI6Ilx1N2JhMVx1NzQwNlx1NTQ1OCJ9.UoPLDkVwzLLHcX41dBfgIX0YCFFWf2TJ_4YUsFwpOmU"}
data = {"username":"team2","password":"team2","name":"team2"}

r = requests.post(server+"/sport/team/",headers=header,data=data)
print(r.text)