def get_account_dictionary():
    """Return account dictionary
    format: name: email
    e.g. they are all my email accounts
    {"Jimmy's gmail": 'jimmy75792@gmail.com', 
                "Jimmy's outlook": 'cgo54@uclive.ac.nz'}
    """
    
def get_receiver_dictionary():
    """Simlilar as above"""
    
    
def get_mail_templates(account_name):
    """e.g. account name is "Jimmy's gmail"
       It should return a dictionary {"name of the template": "Content"}
    """
    
def delete_template(account_name, template_name):
    
    
def save_template(account_name, template_name, template_content, is_new):
    """If is a new template, the name exists, return false
       If is not a new template, override the template file, return true
    """
