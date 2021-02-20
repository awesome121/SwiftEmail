"""A program to send email         Jimmy              23/1/2019

   Support server: outlook, gmail, qq-email
   
   Note: Some email account can't login in because of security issue.
         If the system gives you a prompt that the server is refusing.
         You need to go to setting and change some security options. 
"""
from tkinter import *
from tkinter.ttk import *
from smtplib import SMTP
from email.mime.text import MIMEText
import smtplib
from time import asctime


class EmailGui:
    """To send email quicklier with a template"""
    global ACCOUNT_DICT, RECEIVER_DICT
    def __init__(self, window):
        """Initializer"""
        #Labels:
        self.prompt_label = Label(window, text='Welcome to use swift email system!')
        self.prompt_label.grid(row=0, column=0, columnspan=3)      
        
        self.account_label = Label(window, text='Account: ')
        self.account_label.grid(row=1, column=0)        
        
        self.password_label = Label(window, text='Password: ')
        self.password_label.grid(row=2, column=0)        
        
        self.address_label = Label(window, text='To: ')
        self.address_label.grid(row=4, column=0, sticky=E)
        
        self.subject_label = Label(window, text='Subject: ')
        self.subject_label.grid(row=5, column=0, sticky=E)
        
        self.content_label = Label(window, text='Content: ')
        self.content_label.grid(row=6, column=0)
        
        #Buttons:
        self.account_enter = Button(window, text='Log In', command=self.connection)
        self.account_enter.grid(row=3, column=1, columnspan=3, sticky=(E, W))
           
        self.content_submit = Button(window, text='Send', command=self.send)
        self.content_submit.grid(row=8, column=2)
        
        #Combobox:
        self.account_combo = Combobox(window, values=list(ACCOUNT_DICT.keys()))
        self.account_combo.grid(row=1, column=1, sticky=(E, W), columnspan=2)
        
        self.address_combo = Combobox(window, values=list(RECEIVER_DICT.keys()))
        self.address_combo.grid(row=4, column=1, sticky=(E, W))
        
        #Entry:

        self.password_entry = Entry(window, show='*')
        self.password_entry.grid(row=2, column=1, sticky=(E, W), columnspan=2)
                
        self.subject_entry = Entry(window)
        self.subject_entry.grid(row=5, column=1, sticky=(E, W))
        self.subject_entry.insert('1', '')
        
        #Text:
        self.content = Text(window, width=50, height=25)
        self.content.grid(row=7, column=1)
        #self.content.insert('1.0', 'Dear ' + '\n' * 10)
        #self.content.insert('10.0', 'Thank you\nJimmy')
        

    def connection(self):
        """A connection to email server"""
        if self.account_combo.get() == '' or self.password_entry.get() == '':
            self.prompt_label['text'] = 'Incorrect account information' 
            
        else:
            try:
                self.account = ACCOUNT_DICT[self.account_combo.get()]
            except KeyError:
                self.account = self.account_combo.get()
            try:
                host = self.account.split('@')[1] 
            except IndexError:
                self.prompt_label['text'] = 'Invilid address'
            else:
                if host[-5:-3] in ['ac']:
                    host = 'office365.com'
                password = self.password_entry.get()            
                time = asctime().split()[3]
                self.server = SMTP('smtp.' + host, 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                try:
                    self.server.login(self.account, password, initial_response_ok=True)
                except smtplib.SMTPAuthenticationError:
                    self.prompt_label['text'] = 'Invalid password    ' + '  Last Attempt: ' + time
                except smtplib.SMTPServerDisconnected:
                    self.prompt_label['text'] = 'Email server is refusing connection    ' + '  Last Attempt: ' + time                
                except:
                    self.prompt_label['text'] = 'Disconnected    ' + '  Time: ' + time
                else:
                    self.prompt_label['text'] = self.account +'       Connected    ' + 'Connection made on: ' + time
        
        
    def send(self):
        """Send message"""
        time = asctime().split()[3]
        try:
            address = RECEIVER_DICT[self.address_combo.get()]
        except KeyError:
            address = self.address_combo.get()  
        try:
            mail = MIMEText(self.content.get(0.0, 10.0))
            mail['Subject'] = self.subject_entry.get()
            print(mail.as_string())
            self.server.sendmail(self.account, address, mail.as_string())
        except:
            self.prompt_label['text'] = 'Fail to send     ' + 'Time: ' + time
        else:
            print(self.content.get(0.0, 25.0))
            self.prompt_label['text'] = 'Send to:  ' + address + '    Successfullly    ' + 'Time: ' + time

#================================================================================

def main():
    """Main function"""
    window = Tk()
    main_object = EmailGui(window)
    window.mainloop()
    
main()
