import requests

data = {'Name': "svc_release_team_01@ea.com", 'Password': "H7^Ye%iidAutyntB5S(C"}
res = requests.post('https://eamc-ota.ad.ea.com/OTA/Account/LoginWithPassword', json=data, verify=False)
print(res.text)
