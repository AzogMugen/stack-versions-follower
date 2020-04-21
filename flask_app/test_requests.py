import requests

url = 'http://127.0.0.1:5000/create'
headers = {'Content-Type': "application/json", 'Accept': "application/json"}

print('=============')
print('Good requests')
print('=============')
good = [
    '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version":"1.0.0-RC1"}',
    '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version":"1.0.1-beta+12sa5s4d4ze"}',
    '{"env": "dev", "name":"Second app","url":"https://other.url.com:1337","version":"1.0.2"}'
]

for payload in good:
    res = requests.post(url, data=payload, headers=headers,)
    if res.status_code == 200:
        print("Expected response 200, recieved "+str(res.status_code)+" : OK")
    else:
        print("Unexpected response, should be 200, is " + str(res.status_code))
        print("Payload : \n" + payload)



print('============')
print('Bad requests')
print('============')
bad = [
  '{"e$nv": "dev", "name":"Test app","url":"https://url.of.test.com","version" : "1.0.3"}',
  '{"env.": "dev", "name":"Test app","url":"https://url.of.test.com","version" : "1.0.3"}',
  '{"env": "<dev>", "name":"Test app","url":"https://url.of.test.com","version" : "1.0.3"}',
  '{"env": "dev", "name":"Test app<","url":"https://url.of.test.com","version" : "1.0.3"}',
  '{"env": "dev", "name":"Test app","url":"https://url.of.test.com>","version" : "1.0.3"}',
  '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version" : ">1.0.3"}',
  '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version" : "1.0.3 "}',
  '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version" : "-1.0.3"}',
  '{"env": "dev", "name":"Test app","url":"https://url.of.test.com","version" : "1.0.3:"}'
]

for payload in bad:
    res = requests.post(url, data=payload, headers=headers,)
    if res.status_code == 400:
        print("Expected response 400, recieved "+str(res.status_code)+" : OK")
        print(res.content)
    else:
        print("Unexpected response, should be 400, is " + str(res.status_code))
        print("Payload : \n" + payload)
        print(res.content)
