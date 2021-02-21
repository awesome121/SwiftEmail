"""A program to send email         Changxing, Patrick            21/02/2021

   Support server: outlook, gmail, qq-email
   
   Note: Some email account can't login in because of security issue.
         If the system gives you a prompt that the server is refusing.
         You need to go to setting and change some security options. 
"""
from tkinter import *
from tkinter.ttk import *
import fileHandler 
from smtplib import SMTP
from email.mime.text import MIMEText
import smtplib
from time import asctime


class EmailGui:
    """To send email quicklier with a template"""
    def __init__(self, window):
        """Initializer"""
        self.window = window
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
        self.account_enter = Button(window, text='Log In', command=self.on_click_login)
        self.account_enter.grid(row=3, column=1, columnspan=3, sticky=(E, W))
        
        self.template_delete = Button(window, text='Delete', command=self.on_click_delete_template)
        self.template_delete.grid(row=8, column=0)        
        
        self.new_template = Button(window, text='New template', command=self.on_click_new_template)
        self.new_template.grid(row=6, column=2)
           
        self.content_submit = Button(window, text='Send', command=self.on_click_send)
        self.content_submit.grid(row=8, column=2)
        
        
        #Combobox:
        self.account_combo = Combobox(window, values=list(fileHandler.get_account_dictionary().keys()))
        self.account_combo.grid(row=1, column=1, sticky=(E, W), columnspan=2)
        
        self.address_combo = Combobox(window, values=list(fileHandler.get_receiver_dictionary().keys()))
        self.address_combo.grid(row=4, column=1, sticky=(E, W))
        
        self.template_combo = Combobox(window, values=list(fileHandler.get_mail_templates(self.account_combo.get()).keys()))
        self.template_combo.grid(row=7, column=0)
        self.template_combo.bind('<<ComboboxSelected>>', self.on_selected_template_combo)
        
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
        


    #======Component on listeners===========
    def on_click_login(self):
        """A connection to email server"""
        self.update_template_combobox() #change templates to this new account
        if self.account_combo.get() == '' or self.password_entry.get() == '':
            self.prompt_label['text'] = 'Incorrect account information' 
            
        else:
            try:
                self.account = fileHandler.get_account_dictionary()[self.account_combo.get()]
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
        
    def on_click_new_template(self):
        self.new_template.configure(text='Save', command=self.on_click_save_template)
        self.prompt_label['text'] = 'Please enter template name and content'
        self.content.delete(1.0, "end")
        self.content.insert(1.0, 'Template Name: ""\nTemplate Content: \n"\n\n\n"')
        
    def on_click_save_template(self):
        time = asctime().split()[3]
        template_name, template_content = process_text_for_template(self.content.get('1.0', 'end'))
        if template_name in fileHandler.get_mail_templates(self.account_combo.get()): # If it exists
            is_overriden = fileHandler.save_template(self.account_combo.get(), template_name, template_content)
        else:
            is_overriden = fileHandler.save_template(self.account_combo.get(), template_name, template_content)
        if is_overriden:
            self.prompt_label['text'] = 'Template Overriden at ' + time
        else:
            self.prompt_label['text'] = 'Template Saved at ' + time
        self.new_template.configure(text='New template', command=self.on_click_new_template)
        self.update_template_combobox()
        self.content.delete(1.0, 'end')
        
        
    def on_click_delete_template(self):
        time = asctime().split()[3]
        if self.new_template['text'] == 'Save':
            self.prompt_label['text'] = 'Please save the editing template first '
        else:
            was_found = fileHandler.delete_template(self.account_combo.get(), self.selected_combo_item)
            if was_found:
                self.prompt_label['text'] = 'Template Deleted at ' + time
            self.update_template_combobox()
        
    def on_selected_template_combo(self, event):
        self.update_template_combobox()
        self.selected_combo_item = event.widget.get()
        if self.new_template['text'] == 'Save':
            self.prompt_label['text'] = 'Please save the editing template first ' + time
        else:
            template_content = fileHandler.get_mail_templates(self.account_combo.get())[self.selected_combo_item]
            self.content.delete(1.0, 'end')
            self.content.insert(1.0, template_content)
    
        
    def on_click_send(self):
        """Send message"""
        time = asctime().split()[3]
        try:
            address = fileHandler.get_receiver_dictionary[self.address_combo.get()]
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
            
            
    #======Component on click listeners above===========
    
    
    
    def update_template_combobox(self):
        self.template_combo.configure(values=list(fileHandler.get_mail_templates(self.account_combo.get()).keys()))    
    

#================================================================================



def process_text_for_template(text):
    temp_name, temp_content = '', ''
    ln = text.split('"')
    return ln[1], '"'.join(ln[3:-1])


def main():
    """Main function"""
    window = Tk()
    main_object = EmailGui(window)
    window.mainloop()
    
main()
