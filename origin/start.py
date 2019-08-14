import urllib.request
from bs4 import BeautifulSoup

link="https://docs.google.com/forms/d/1keBiImwMyXaXFtK93AQ6VKWo5U2NegDF3I_ZUYLKVNg/viewform"
linkarr=link.split('/')
print(linkarr[6])
page=urllib.request.urlopen(link)
soup=BeautifulSoup(page, "html.parser")
rand=[]

######    TITLE:
#print(soup.find_all("div", {"class": "freebirdFormviewerViewHeaderTitle exportFormTitle freebirdCustomFont"}))
s = soup.find("div", {"class": "freebirdFormviewerViewHeaderTitle exportFormTitle freebirdCustomFont"})
title = s.get_text(separator="\n")
print(title)


final_ans=dict()

def input_entries():
    #print(soup.find_all("div", {"class": "freebirdFormviewerViewItemsItemItemTitle exportItemTitle freebirdCustomFont"}))
    questions = soup.find_all("div", {"class": "freebirdFormviewerViewItemsItemItem"})
    
    for q in questions[0:]:
        question_list = []
        result = q.get_text(separator="\n")
        question_list.append(result)
        print(result)
        attributes = q.find_all("input")
        user_ans=input("Enter your choice: ")
        #print(attributes)
        for attribute in attributes:
            try:
                entry_token=str(attribute.attrs['name'])
                if(entry_token[-1].isdigit()):
                    token=str(attribute.attrs['name'])
                    #print(attribute.attrs['name'])
                    break
            except:
                print("")
        if user_ans.startswith('!random'):
            rand.append(result.split('\n'))
        final_ans[token]=user_ans
        print()
    #print(question_list)

    print(final_ans)
