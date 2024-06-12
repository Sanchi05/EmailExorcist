import imaplib
from itertools import chain
import email
from email import policy
import re
import constants as const


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

#Defining variables
urls = []
email_message_list = []
#defining UID and Criteria incase we need to restrict the mail search
max_UID = 0
criteria = {}

def create_a_string(crt,max_uid): 
    list_uid = [('UID', '%d:*' % (max_uid+1))]
    string = list(map(lambda item: (item[0], '"'+str(item[1])+'"'), criteria.items()))
    fin_string = string + list_uid
    fin_string_search = '(%s)' % ' '.join(chain(*fin_string))
    return fin_string_search

#definining a search string
def string_to_search(max_uid,criteria_h):
    final_string = create_a_string(criteria_h,max_uid)
    return final_string

final_string_to_search = string_to_search(max_UID,criteria)
# print(final_string_to_search)
#searching for string
matched_mails, data = imap_login.uid('SEARCH',None,final_string_to_search)
#data is a string of UIDs
int_uid = [int(id) for id in data[0].split()]
#checking if the list is empty or not and then selecting the maximum uid present in the list
if (len(int_uid) != 0):
    max_UID = max(int_uid)
    #print(max_UID)

imap_login.logout()

#Function to extracting required attributes from the email
def get_attributes(attrName,email_msg):
    try:
        value = email_msg[attrName]
        if len(value) != 0 :
            return value
        else :
            return "Maybe check your attrName string or email msg!:("
    except Exception as e :
        print ("Error occured! Here's the error:(", e)

#Function to find URLs from the emails
def finding_urls(text):
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9. \-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`! ()\[\]{};:'\".,<>? «»“”'']))"
    return re.findall(url_pattern, text)

def re_gex_find(pattrn,text):
    return re.search(pattrn, text)

#Creating an email dictionary object
def email_details(email_msg_, list_of_urls_extracted,uid):
    empty_email_dict = dict()
    received_headers = []
    empty_email_dict[const.UID] = uid 
    message_Id = get_attributes("Message-ID", email_msg_)
    email_from = get_attributes("From",email_msg_)
    email_subject = get_attributes("Subject", email_msg_)
    empty_email_dict["Message-ID"] = message_Id
    empty_email_dict["Email-From"] = email_from
    empty_email_dict["Email-Subject"] = email_subject
    for header in email_msg_.get_all('Received'):
        is_from_recived = re_gex_find(r"^(\bfrom\b)(.*)", header)
        if is_from_recived :
            received_headers.append(header)
    if len(received_headers) != 0:
        empty_email_dict["Received"] = received_headers
    else :
        empty_email_dict["Received"] = "No received from headers available"
    empty_email_dict[const.FOUND_URLS] = list_of_urls_extracted
    # print(empty_email_dict)
    return empty_email_dict


# Extracting URLs
def extract_urls_from_email(email_message,uid):
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                if (part.get_content_maintype() == 'text'):
                    email_body = part.get_payload(decode=True).decode("utf-8")
                    extracted_urls = finding_urls(email_body,)
            for each_url in extracted_urls:
                for url in each_url:
                    if (len(url) != 0):
                        urls.append(url)
            # for url_item in urls:
            #     print("URL: ", url_item) Not needed right now. 
            #     print('\n')
        email_details(email_message,urls,uid)
    except Exception as e:
        print("Error occured while trying to check if the email is multipart. Error: ",e)


#Logging in again
i = 0 
while i < 1 : 
    mail_login = imaplib.IMAP4_SSL(imap_ssl_host)
    mail_login.login(un,appPassword)
    mail_login.select('INBOX')
    tmp_new, mail_data = mail_login.search(None, 'ALL')
    #print(tmp_new)
    i+= 1
    #Looking for mails having UIDs more than the existing UID
    required_tmp, required_data = mail_login.uid('SEARCH',None,final_string_to_search)
    uids_list = [int(ids) for ids in required_data[0].split()]
    # print("Max uid=",max_UID)
    # print(uids_list[len(uids_list)-1])
    for u_id in uids_list:
        if u_id >= max_UID:
            for id in range(max_UID-4,max_UID+1):
                fetched_result, fetched_data = mail_login.uid("FETCH",str(id), '(RFC822)')
                if fetched_result == "OK":
                    email_message = email.message_from_bytes(fetched_data[0][1],policy=policy.default)
                    #email_message_list.append(email_message.as_string()) Keep this and not the next line
                    email_message_list.append(email_message)
                    # print(email_message)
                    # print("======================================================")
                    extract_urls_from_email(email_message,id) 






    

    








