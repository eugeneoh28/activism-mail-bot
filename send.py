
from __future__ import print_function
#!/usr/bin/env python3
from getpass import getpass
from email.message import EmailMessage
from email.mime.text import MIMEText
import googleapiclient
import google_auth_oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pickle
import os.path
import messages, recipients, smtplib, ssl, time

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8")
  }

def send_message(service, user_id, message):
  try:
    message = service.users().messages().send(userId=user_id, body=message).execute()
    print('Message Id: %s' % message['id'])
    print ('Message: %s' % message)
    return message
  except Exception as e:
    print('An error occurred: %s' % e)
    return None

def print_email(destination, subject, body):
  print('To: %s' % destination)
  print('Subject: %s' % subject)
  print('Body: %s' % body)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def main():
   
    print("""Welcome to the activism email bot! This bot sends emails to 119 elected officials
    accross the U.S. calling for action from our elected officials. (template from nomoreracistcops.github.io)
    Credits for this app to go https://github.com/alandgton/activism-mail-bot.\n""")

    print("""When you press enter, a browser window will launch, asking you to give this app permission
    to send emails from your gmail account. (At the time of this writing, we have not gotten our app verified
    yet as it takes a couple days to do so and so you will need to click on the Advanced button to bypass 
    it on the webpage)\n""")
            
    print("""We promise we are not doing anything malicious with your email creds and we are using them only 
    for the purpose of sending emails to elected officials. You can check the source code in link above to 
    check if you would like.\n""")

    input("Press Enter to continue to begin!")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                resource_path('credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    print("\nNow that we've finished authenticating lets get started:\n")
    src_name = input("Type your name (first, last) and press enter: ")
    src_email = input("Type your email and press enter:")
    print("\nWhat would you like the subject (title) of your email to be?")
    subject = input("Type here and press enter (a random one will be generated if blank): ")

    recv = recipients.gen_recipients()
    while recv:
      recipient = recv.pop()
      dst_name = recipient[0]
      location = recipient[1]
      dst_email = recipient[2]
      subject = subject if subject else messages.gen_subject()
      body = messages.gen_body(src_name, dst_name, location)

      message = create_message(src_email, dst_email, subject, body)
      send_message(service, "me", message)
      
      print_email(dst_email, subject, body) # print if we get through without
      time.sleep(0.1)

if __name__ == '__main__':
    main()