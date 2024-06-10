import imaplib
from itertools import chain
import email
import base64
import os
import re


imap_ssl_host = "imap.gmail.com"
imap_ssl_port = 993
un = "sanchipatel05@gmail.com"
passwd = "9825129208"
appPassword = "maxn kspq cqmx eimr"

#login into account
imap_login = imaplib.IMAP4_SSL(imap_ssl_host)
imap_login.login(un,appPassword)
imap_login.select('INBOX')
tmp, data = imap_login.search(None, 'ALL')

#defining UID and Criteria incase we need to restrict the mail search
max_UID = 0
criteria = {}

def create_a_string(crt,max_uid): 
    # print(crt.items())
    list_uid = [('UID', '%d:*' % (max_uid+1))]
    # print("itemm==",item)
    #string = item[0] + " '" + str(item[1]) + "' "
    string = list(map(lambda item: (item[0], '"'+str(item[1])+'"'), criteria.items()))
    # print(string + list_uid)
    fin_string = string + list_uid
    fin_string_search = '(%s)' % ' '.join(chain(*fin_string))
    # print(fin_string_search)
    return fin_string_search

#definining a search string
def string_to_search(max_uid,criteria_h):
    final_string = create_a_string(criteria_h,max_uid)
    return final_string

final_string_to_search = string_to_search(max_UID,criteria)
print(final_string_to_search)

#searching for string
matched_mails, data = imap_login.uid('SEARCH',None,final_string_to_search)
#print(data)
#print(len(data),type(data))
#data is a string of UIDs
int_uid = [int(id) for id in data[0].split()]
#print(int_uid)
#checking if the list is empty or not and then selecting the 
#maximum uid present in the list
if (len(int_uid) != 0):
    max_UID = max(int_uid)
    print(max_UID)

imap_login.logout()

#logging in again
i = 0 
while i < 1 : 
    mail_login = imaplib.IMAP4_SSL(imap_ssl_host)
    mail_login.login(un,appPassword)
    mail_login.select('INBOX')
    tmp_new, mail_data = mail_login.search(None, 'ALL')
    print(tmp_new)
    i+= 1
    #Looking for mails having UIDs more than the existing UID
    required_tmp, required_data = mail_login.uid('SEARCH',None,final_string_to_search)
    uids_list = [int(ids) for ids in required_data[0].split()]
    print("Max uid=",max_UID)
    print(uids_list[len(uids_list)-1])
    for u_id in uids_list:
        if u_id >= max_UID:
            fetched_tmp, fetched_data = mail_login.uid("FETCH",str(u_id), '(RFC822)')
            print(fetched_data)
    print(len(uids_list))










