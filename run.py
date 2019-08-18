import http.client
import urllib.request
import random
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, redirect, url_for
from faker import Faker
fake=Faker()
fake_IN=Faker('hi_IN')

app = Flask(__name__)
link_short=str()
num=int()
final_ans=dict()
form_entry=list()
rand=list()
question_list=list()

@app.route('/',  methods=["GET","POST"])
def index():
    global link_short, num, final_ans, form_entry, rand, question_list
    if request.method=="POST":
        link = request.form['link']
        num = request.form['num']
        linkarr = link.split('/')
        link_short = linkarr[6]
        page=urllib.request.urlopen(link)
        soup=BeautifulSoup(page, "html.parser")
        rand=[]
        s = soup.find("div", {"class": "freebirdFormviewerViewHeaderTitle exportFormTitle freebirdCustomFont"})
        title = s.get_text(separator="\n")
        
        
        def input_entries():
            questions = soup.find_all("div", {"class": "freebirdFormviewerViewItemsItemItem"})
            
            for q in questions[0:]:
                
                result = q.get_text(separator="\n")
                question_list.append(result)
                
                attributes = q.find_all("input")
                #user_ans=input("Enter your choice: ")
                
                for attribute in attributes:
                    try:
                        entry_token=str(attribute.attrs['name'])
                        if(entry_token[-1].isdigit()):
                            token=str(attribute.attrs['name'])
                            form_entry.append(token)
                            break
                    except:
                        print("")
                
                # if user_ans.startswith('!random'):
                #     rand.append(result.split('\n'))
                #final_ans[token]=user_ans
                
        input_entries()
        question_length = len(question_list)

        return render_template("sent.html",**locals(), question_list = question_list)
    else:
        return render_template("index.html", **locals())

@app.route('/send',  methods=["GET","POST"])
def send():
    global link_short ,num, form_entry, rand, question_list
    if request.method=="POST":
        form_entry_data = request.form.getlist('user_ans')
        print(form_entry)
        print(form_entry_data)
        print(num)
        def post(link,num):
            headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            'postman-token': "f7281180-f919-b589-709a-a77457e89d08"
            }

            for x in range(int(num)):
                conn = http.client.HTTPSConnection("docs.google.com")
                rand_ctr=0
                payload="------WebKitFormBoundary7MA4YWxkTrZu0gW"
                for i in range(len(form_entry)):
                    #print("ans= "+str(faker_input((form_entry_data[i])[6:])))
                    if(form_entry_data[i].startswith('!cgpa')):
                        payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(random.randrange(8,10,1))+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
                    elif(form_entry_data[i].startswith('!fake.')):
                        payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(faker_input((form_entry_data[i])[6:]))+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
                    elif(form_entry_data[i]=='!random'):
                        rand.append(question_list[i].split('\n'))
                        #print(rand)
                        #print("RANDOM START")
                        #print(str(rand[rand_ctr][random.randrange(1,len(rand[rand_ctr]),1)]))
                        #print("RANDOM END")
                        payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(rand[rand_ctr][random.randrange(1,len(rand[rand_ctr]),1)])+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
                        rand_ctr=rand_ctr+1
                    else:
                        payload+="\r\nContent-Disposition: form-data; name=\""+str(form_entry[i])+"\"\r\n\r\n"+str(form_entry_data[i])+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW"
                payload+="--"
                conn.request("POST", "/forms/u/0/d/e/"+link_short+"/formResponse", payload, headers)
                #res = conn.getresponse()
                print('.')
                #data = res.read()

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
        post(link_short,num)
        return render_template("index.html",**locals())
    else:
        return render_template("index.html",**locals())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='80')
