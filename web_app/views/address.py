import http.client

conn = http.client.HTTPSConnection("global-address.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "SIGN-UP-FOR-KEY",
    'X-RapidAPI-Host': "global-address.p.rapidapi.com"
}

conn.request("GET", "/V3/WEB/GlobalAddress/doGlobalAddress?ctry=DEU&format=json&a1=Gie%C3%9Fener%20Str.%2030&DeliveryLines=Off&a2=Frankfurt%20am%20Main&postal=60435", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))