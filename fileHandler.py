import os

def get_account_dictionary():
    """Return account dictionary
    format: name: email
    e.g. they are all my email accounts
    {"Jimmy's gmail": 'jimmy75792@gmail.com', 
                "Jimmy's outlook": 'cgo54@uclive.ac.nz'}
    """
    return(get_email_entity_information("Users/accounts.csv"))
    
def get_receiver_dictionary():
    """Simlilar as above"""
    return(get_email_entity_information("Users/receivers.csv"))

def get_email_entity_information(csv_directory):
    """Returns a dictionary where the key is a string representing the email name and the value is a string representing the email address
    """
    entities = {}
    file = open(csv_directory,"r")
    for line in file.readlines():
        print(line)
        entry = delete_substrings_in_array(line,["\n","\t","\\"])
        entry = entry.split(",")
        if len(entry) > 1:
            entities[entry[0]] = entry[1]
    file.close()
    return entities

def delete_substrings_in_array(string,replace_):
    for element in replace_:
        string = string.replace(element, "")
    return string
    
def get_mail_templates(account_name):
    """e.g. account name is "Jimmy's gmail"
       It should return a dictionary {"name of the template": "Content"}
    """
    account_dir = "Templates/"+account_name
    templates = {}
    directory_names = os.listdir(account_dir)
    for directory in directory_names:
        file = open(account_dir+"/"+directory,"r")
        templates[directory.split(".")[0]] = file.read()
        file.close()
    return templates
    
def delete_template(account_name, template_name):
    """ Deletes the template specified (template_name) within the account_name's files. True if successful. If the file is not found, return false
    """
    try:
        os.remove("Templates/"+account_name+"/"+template_name+".txt")
    except:
        return False
    return True
    
    
def save_template(account_name, template_name, template_content, is_new):
    """If is a new template, the name exists, return false
       If is not a new template, override the template file, return true
    """
    directory = "Templates/"+account_name+"/"+template_name+".txt"
    if is_new and os.path.exists("Templates/"+account_name+"/"+template_name+".txt"): return False
    file = open(directory,"w")
    file.write(template_content)
    file.close()
    return True

