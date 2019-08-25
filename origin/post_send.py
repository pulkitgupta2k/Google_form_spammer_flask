from start import final_ans, link, input_entries,rand, linkarr
import http.client
from faker import Faker
import random

fake=Faker()
fake_IN=Faker('hi_IN')

link1= linkarr[6]

def post(link,num,faker):
	form_entry=['']
	form_entry_data=['']
	

	if (faker==0):
		for key, value in final_ans.items():
			form_entry.append(key)
			form_entry_data.append(value)
		conn = http.client.HTTPSConnection("docs.google.com")
		

		headers = {
	    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
	    'cache-control': "no-cache",
	    'postman-token': "f7281180-f919-b589-709a-a77457e89d08"
	    }
		print("Sending")
		for x in range (num):
			rand_ctr=0
			payload="------WebKitFormBoundary7MA4YWxkTrZu0gW"
			for i in range(len(form_entry)):
				if(i==0):
					continue
				if(form_entry_data[i]=='!roll'):
					payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+"101703"+str(random.randrange(100,999,1))+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
				elif(form_entry_data[i]=='!num'):
					payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(float(random.randrange(8,10,1))/10)+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
				elif(form_entry_data[i].startswith('!fake.')):
					payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(faker_input((form_entry_data[i])[6:]))+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
				elif(form_entry_data[i]=='!random'):
					print(rand[rand_ctr])
					#print(str(rand[rand_ctr][random.randrange(1,len(rand[rand_ctr]),1)]))
					payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(rand[rand_ctr][random.randrange(1,len(rand[rand_ctr]),1)])+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
					rand_ctr=rand_ctr+1
					#print(rand[rand_ctr])
				else:
					payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(form_entry_data[i])+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
			payload+="--"
			conn.request("POST", "/forms/u/0/d/e/"+link1+"/formResponse", payload, headers)
			res = conn.getresponse()
			data = res.read()
			print('.')

		if(len(data)>100):
			print('Successful!')
		else:
			print('ERROR!!')
		
	
def faker_input(type):
	if(type=="name"):
		return fake.name()
	if(type=="number"):
		return fake.msisdn()
	if(type=="word"):
		return fake.word()
	if(type=="sentence"):
		return fake.sentence()
	if(type=="email"):
		return fake.email()
	else:
		return type
	


faker=0
num=10000
input_entries()
print(rand)
post(link,num,faker)
