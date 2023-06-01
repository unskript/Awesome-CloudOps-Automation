"""This file implements Text User Interface for Credentials."""
#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import os
import json
import logging
import npyscreen


# CONSTANTS USED IN THIS SCRIPT
CONNECTOR_LIST = [
    'AWS', 
    'GCP', 
    'Kubernetes', 
    'ElasticSearch', 
    'Grafana', 
    'Redis', 
    'Jenkins', 
    'Github', 
    'Netbox', 
    'Nomad', 
    'ChatGPT', 
    'Jira', 
    'Kafka', 
    'MongoDB', 
    'MySQL', 
    'PostgreSQL', 
    'REST', 
    'Slack', 
    'SSH', 
    'Salesforce'
]

# Here we create a CONNECTOR GRID of (list_connector)/3 x 3 matrix
# We use the CONNECTOR_LIST above as the list and append the credential
# Text to each of the grid elements.
CONNECTOR_GRID = {}
num_rows = int(len(CONNECTOR_LIST) / 3)
num_columns = 3
_idx = 0
for row in range(num_rows):
    CONNECTOR_GRID[row] = {}
    for col in range(num_columns):
        CONNECTOR_GRID[row][col] = CONNECTOR_LIST[_idx]
        _idx += 1

# This variable is used to hold the Credential directory
# Where all the creds are saved
CREDS_DIR = os.environ.get('HOME') + "/.local/share/jupyter/metadata/credential-save/"

def read_existing_creds(creds_file: str) -> dict:
    """read_existing_creds This is a utility function that simply
       reads the given credential file, extracts the connector data 
       off of it and returns it back as a dict.

       :type creds_file: string
       :param creds_file: Credential File Name with the full path

       :rtype: dict. The connectorData of the given credential
    """
    retval = {}
    if os.path.exists(creds_file) is False:
        return retval 
    
    try:
        with open(creds_file, 'r', encoding='utf-8') as f:
            contents = json.loads(f.read())
        retval = contents.get('metadata')
    except Exception as e:
        raise e
    
    return json.loads(retval.get('connectorData'))


# This class is a custom class of npyscreen.Textfield. The only change here is
# This class does a type checking and ensures that the field that is entered is
# Integer only. 
class IntegerTextfield(npyscreen.Textfield):
    def when_value_edited(self):
        try:
            int(self.value)
        except ValueError:
            self.value = ""

# This class is a custom class of npyscreen.GridColTitles. The only difference
# is that we override the `Esc` key, key number 10. and when pressed we just call
# the Parent's change_forms so it goes to the previous screen. Essential this
# class implements Going back to Main screen on `Esc`
class CredsGrid(npyscreen.GridColTitles):
    def handle_input(self, key):
        if key == 10:
            selected_row = self.edit_cell[0]
            selected_column = self.edit_cell[1]
            try:
                name = CONNECTOR_GRID[selected_row][selected_column]
            except ValueError:
                name = 'MAIN'

            self.parent.change_forms(name)
        return super().handle_input(key)


# This is the Main class where we initialize all the other screens.
# The first screen should be called as MAIN per the library requirement
# The subsequent screens are named similar to what the CONNECTOR_LIST 
# is defined above.  
# This class implements onCleanExit(), on_cancel() and change_form() 
# methods
class CredsApp(npyscreen.NPSAppManaged):
    def onStart(self):
        # The first form need to be name MAIN as per the library requirement
        self.ui = {}
        self.ui['MAIN'] = self.addForm("MAIN", MainScreen, name="Connectors", color="IMPORTANT", align="^")
        self.ui['AWS'] = self.addForm("AWS", AWSCreds, name='AWS Connector', color="IMPORTANT",)
        self.ui['GCP'] = self.addForm("GCP", GCPCreds, name='GCP Connector', color="IMPORTANT",)
        self.ui['Kubernetes'] = self.addForm("Kubernetes", K8SCreds, name='Kubernetes Connector', color="IMPORTANT",)
        self.ui['ElasticSearch'] = self.addForm("ElasticSearch", ElasticSearchCreds, name='ElasticSearch Connector', color="IMPORTANT",)
        self.ui['Grafana'] = self.addForm("Grafana", GrafanaCreds, name='Grafana Connector', color="IMPORTANT",)
        self.ui['Redis'] = self.addForm("Redis", RedisCreds, name='Redis Connector', color="IMPORTANT",)
        self.ui['Jenkins'] = self.addForm("Jenkins", JenkinsCreds, name='Jenkins Connector', color="IMPORTANT",)
        self.ui['Github'] = self.addForm("Github", GithubCreds, name='Github Connector', color="IMPORTANT",)
        self.ui['Netbox'] = self.addForm("Netbox", NetboxCreds, name='Netbox Connector', color="IMPORTANT",)
        self.ui['Nomad'] = self.addForm("Nomad", NomadCreds, name='Nomad Connector', color="IMPORTANT",)
        self.ui['ChatGPT'] = self.addForm("ChatGPT", ChatGPTCreds, name='ChatGPT Connector', color="IMPORTANT",)
        self.ui['Jira'] = self.addForm("Jira", JiraCreds, name='Jira Connector', color="IMPORTANT",)
        self.ui['Kafka'] = self.addForm("Kafka", KafkaCreds, name='Kafka Connector', color="IMPORTANT",)
        self.ui['MongoDB'] = self.addForm("MongoDB", MongoCreds, name='MongoDB Connector', color="IMPORTANT",)
        self.ui['MySQL'] = self.addForm("MySQL", MySQLCreds, name='MySQL Connector', color="IMPORTANT",)
        self.ui['PostgreSQL'] = self.addForm("PostgreSQL", PostgresCreds, name='PostgreSQL Connector', color="IMPORTANT",)
        self.ui['REST'] = self.addForm("REST", RestCreds, name='REST Connector', color="IMPORTANT",)
        self.ui['Slack'] = self.addForm("Slack", SlackCreds, name='Slack Connector', color="IMPORTANT",)
        self.ui['SSH'] = self.addForm("SSH", SSHCreds, name='SSH Connector', color="IMPORTANT",)
        self.ui['Salesforce'] = self.addForm("Salesforce", SalesforceCreds, name='Salesforce Connector', color="IMPORTANT",)
    

    def onCleanExit(self):
        npyscreen.notify_wait("Syncing Data back to disk!")

    def on_cancel(self,t):
        npyscreen.notify_wait("Bye!")
        self.switchForm(None)
                
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


# This is a custom class that inherits from npyscreen.ActionForm. This is
# more like an abstract class which is being inheritted by all the connector
# class. This class defines the basic class structure and implements the
# change_forms() method that is being used by all the other subclasses below

class CredsForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleFixedText, name = "Press Esc to go back to connectors page", align="^")
        self.add_handlers({"^T": self.change_forms})
        self.add_handlers({"^Q": self.custom_quit})

    def custom_quit(self, a):
        self.on_ok()

    def on_cancel(self):
        self.parentApp.resetHistory()
        self.parentApp.change_form('MAIN')

    def on_ok(self):
        self.parentApp.switchForm(None)

    def change_forms(self, *args, **keywords):
        n = self.name.replace('Connector', '').strip()
        name = ''
        if n in CONNECTOR_LIST:
            idx = CONNECTOR_LIST.index(n) + 1
            if idx >= len(CONNECTOR_LIST):
                name = "MAIN"
                idx = 0
            else:
                name = CONNECTOR_LIST[idx]
        self.parentApp.change_forms(name)

# This class implements the GRID for the main screen. GRID contains elements from CONNECTOR_GRID
# matrix. This class inherits from npyscreen.FromBaseNew and implements methods exit_application
# on_cancel and change_forms. 
class MainScreen(npyscreen.FormBaseNew):
    def create(self):
        self.show_cancel_button = False 
        self.add(npyscreen.TitleFixedText, name="* Select Connector to edit or ^Q to quit *")
        self.add(CredsGrid,
                 values=[[CONNECTOR_GRID[row][col] for col in range(num_columns)] for row in range(num_rows)])
        self.add_handlers({"^Q": self.parentApp.on_cancel})
        self.add_handlers({"27": self.parentApp.on_cancel})

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application

    
    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False 

    def on_cancel(self):
        self.parentApp.resetHistory()
        self.parentApp.on_cancel()

    def change_forms(self, name):
        self.parentApp.change_form(name)

# Some Design questions answered
# 1. Why not read the JSON Schema and create the UI reading it?
# A. Every connector has a unique UI requirement. Saving of every
#    connector is also little different. Even a generalized implementation
#    was attempted, we would need special case for each connector
#    which negates using a generic implementation to create UI reading schema file
#
# 2. Why File upload is not implemented for GCP and K8S Connector?
# A. File upload on a terminal means the file should be present locally
#    on the docker. Such credentials are stored on the Users Laptop not
#    on the docker. The next best thing in terms of UI is to present
#    a text field wherein user can just Copy-Paste the configuration.
#    Copy-Pasting eliminates the need for JSON/YAML file to be present
#    on the docker at the time of creating the credential.  
#
# 3. Why npyscreen was chosen? 
# A. ncurses is the lowest level that can be used for creating simple UI
#    however, to achieve a simple UI screen with Buttons and some Text lable
#    to a few tens of lines depending on the complexity. There are other
#    packages like tkinter, pytermgui, etc... among them, npyscreen seemed
#    like a nicer and well written package. About 1.5K stars on the Github
#    at the time of writing. As can be seen the actual UI element code
#    here is very minimum. 

# Following Classes define specific UI Element for each connector type.
# Every class inherits from CredsForm. Every class implements
# create() and on_ok() methods which are specific to the connector. 
# Any new connector that needs to be added should also implement a custom class

class AWSCreds(CredsForm):
    def create(self):
        super().create()
        self.add(npyscreen.TitleFixedText, name="Auth Schema", align="^", color="IMPORTANT", )
        self.access = self.add(npyscreen.TitleText, name="Access Key", align="^",)
        self.secret = self.add(npyscreen.TitlePassword, name="Secret Key", align="^")

        c_data = read_existing_creds(CREDS_DIR + 'awscreds.json')
        if c_data:
            if c_data.get('authentication'):
                if c_data.get('authentication').get('access_key'):
                    self.access.value = c_data.get('authentication').get('access_key')
                if c_data.get('authentication').get('secret_access_key'):
                    self.secret.value = c_data.get('authentication').get('secret_access_key')

    def on_ok(self):
        if self.access.value and self.secret.value:
            creds_file = CREDS_DIR + 'awscreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("AWS Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for AWS is Missing")

            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("AWS Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for AWS is Missing")
            d = {}
            d['authentication'] = {}
            d['authentication']['auth_type'] = "Access Key"
            d['authentication']['access_key'] = self.access.value  
            d['authentication']['secret_access_key'] = self.secret.value  
            contents['metadata']['connectorData'] = json.dumps(d) 

            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        
        super().on_ok()

class GCPCreds(CredsForm):
    def create(self):
        super().create()
        self.gcpjson = self.add(npyscreen.MultiLineEditableBoxed, values=[""],name="~ Paste your Credential JSON Below ~", align="^", color="IMPORTANT")
        
        c_data = read_existing_creds(CREDS_DIR + 'gcpcreds.json')
        if c_data:
            self.gcpjson.value = json.dumps(c_data)

    def on_ok(self):
        if self.gcpjson.values:
            creds_file = CREDS_DIR + 'gcpcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("GCP Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for GCP is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("GCP Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for GCP is Missing")
            contents['metadata']['connectorData'] = json.dumps(self.gcpjson.values)
    
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))

        super().on_ok()

class ElasticSearchCreds(CredsForm):
    def create(self):
        super().create()
        self.es_hostname = self.add(npyscreen.TitleText, name="Hostname", align="^", color="IMPORTANT",)
        self.es_username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self.es_password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self.es_apikey = self.add(npyscreen.TitlePassword, name="API Key", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'escreds.json')
        if c_data:
            if c_data.get('username'):
                self.es_username.value = c_data.get('username')
            if c_data.get('host'):
                self.es_hostname.value = c_data.get('host')
            if c_data.get('password'):
                self.es_password.value = c_data.get('password')
            if c_data.get('api_key'):
                self.es_apikey.value = c_data.get('api_key')

    def on_ok(self):
        if self.es_hostname and self.es_username and self.es_apikey and self.es_password:
            creds_file = CREDS_DIR + 'escreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Elastic Search Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for ES is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Elastic Search Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for ES is Missing")
            d = {}
            d['username'] = self.es_username.value
            d['password'] = self.es_password.value
            d['host'] = self.es_hostname.value
            d['api_key'] = self.es_apikey.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        
        super().on_ok()
             

class GrafanaCreds(CredsForm):
    def create(self):
        super().create()
        self._apikey = self.add(npyscreen.TitlePassword, name="API Key", align="^", color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self._hostname = self.add(npyscreen.TitleText, name="Hostname", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'grafanacreds.json')
        if c_data:
            if c_data.get('api_key'):
                self._apikey.value = c_data.get('api_key')
            if c_data.get('username'):
                self._username.value = c_data.get('username')
            if c_data.get('password'):
                self._password.value = c_data.get('password')
            if c_data.get('host'):
                self._hostname.value = c_data.get('host')

    def on_ok(self):
        if self._hostname and self._username and self._apikey and self._password:
            creds_file = CREDS_DIR + 'grafanacreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Grafana Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Grafana is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Grafana Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Grafana is Missing")
            d = {}
            d['api_key'] = self._apikey.value
            d['username'] = self._username.value
            d['password'] = self._password.value
            d['host'] = self._hostname.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class RedisCreds(CredsForm):
    def create(self):
        super().create()
        self.add(npyscreen.TitleFixedText, name="DB", align="^", color="IMPORTANT",)
        self._db = self.add(IntegerTextfield, name="DB", align="^",  color="IMPORTANT",)
        self._hostname = self.add(npyscreen.TitleText, name="Hostname", align="^", color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Port", align="^", color="IMPORTANT")
        self._port = self.add(IntegerTextfield, name="Port", value="6379", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Use SSL", args="^", color="IMPORTANT",)
        self._use_ssl = self.add(npyscreen.ComboBox, name="Use SSL", values=[True, False], scroll_exit=True, color='IMPORTANT',)

        c_data = read_existing_creds(CREDS_DIR + 'rediscreds.json')
        if c_data:
            if c_data.get('db'):
                self._db.value = c_data.get('db')
            if c_data.get('username'):
                self._username.value = c_data.get('username')
            if c_data.get('password'):
                self._password.value = c_data.get('password')
            if c_data.get('host'):
                self._hostname.value = c_data.get('host')
            if c_data.get('use_ssl'):
                self._hostname.value = c_data.get('use_ssl')
            if c_data.get('port'):
                self._port.value = c_data.get('port')
    
    def on_ok(self):
        if self._hostname and self._username and self._db and self._password:
            creds_file = CREDS_DIR + 'rediscreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Redis Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Redis is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Redis Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Redis is Missing")
            d = {}
            d['db'] = self._db.value
            d['username'] = self._username.value
            d['password'] = self._password.value
            d['host'] = self._hostname.value
            d['use_ssl'] = self._use_ssl.values[self._use_ssl.value]
            d['port'] = self._port.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class JenkinsCreds(CredsForm):
    def create(self):
        super().create()
        self._url = self.add(npyscreen.TitleText, name="Jenkins URL", align="^", type=int, color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'jenkinscreds.json')
        if c_data:
            if c_data.get('username'):
                self._username.value = c_data.get('username')
            if c_data.get('password'):
                self._password.value = c_data.get('password')
            if c_data.get('url'):
                self._url.value = c_data.get('url')

    def on_ok(self):
        if self._url and self._username and self._password:
            creds_file = CREDS_DIR + 'jenkinscreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Jenkins Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Jenkins is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Jenkins Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Jenkins is Missing")
            d = {}
            d['username'] = self._username.value
            d['password'] = self._password.value
            d['url'] = self._url.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class GithubCreds(CredsForm):
    def create(self):
        super().create()
        self._token = self.add(npyscreen.TitlePassword, name="Access Token", align="^", color="IMPORTANT",)
        self._hostname = self.add(npyscreen.TitleText, name="Custom Hostname", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'githubcreds.json')
        if c_data:
            if c_data.get('hostname'):
                self._hostname.value = c_data.get('hostname')
            if c_data.get('token'):
                self._token.value = c_data.get('token')
    
    def on_ok(self):
        if self._token and self._hostname:
            creds_file = CREDS_DIR + 'githubcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Github Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Github is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Github Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Github is Missing")
            d = {}
            d['hostname'] = self._hostname.value
            d['token'] = self._token.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class NetboxCreds(CredsForm):
    def create(self):
        super().create()
        self._token = self.add(npyscreen.TitlePassword, name="Token", align="^", color="IMPORTANT",)
        self._host = self.add(npyscreen.TitleText, name="Hostname", align="^", color="IMPORTANT",)
        self._threading = self.add(npyscreen.TitleText, name="Threading", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'netboxcreds.json')
        if c_data:
            if c_data.get('token'):
                self._token.value = c_data.get('token')
            if c_data.get('host'):
                self._host.value = c_data.get('host')
            if c_data.get('threading'):
                self._threading.value = c_data.get('threading')
    
    def on_ok(self):
        if self._token and self._host and self._threading:
            creds_file = CREDS_DIR + 'netboxcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Netbox Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Netbox is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Netbox Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Netbox is Missing")
            d = {}
            d['token'] = self._token.value
            d['host'] = self._host.value
            d['threading'] = self._threading.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class NomadCreds(CredsForm):
    def create(self):
        super().create()
        self._timeout = self.add(npyscreen.TitleText, name="Timeout", align="^", color="IMPORTANT",)
        self._token = self.add(npyscreen.TitlePassword, name="Token", align="^", color="IMPORTANT",)
        self._host = self.add(npyscreen.TitleText, name="Host", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'nomadcreds.json')
        if c_data:
            if c_data.get('timeout'):
                self._timeout.value = c_data.get('timeout')
            if c_data.get('token'):
                self._token.value = c_data.get('token')
            if c_data.get('host'):
                self._host.value = c_data.get('host')
    
    def on_ok(self):
        if self._token and self._host and self._timeout:
            creds_file = CREDS_DIR + 'nomadcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Nomad Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Nomad is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Nomad Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Nomad is Missing")
            d = {}
            d['timeout'] = self._timeout.value
            d['token'] = self._token.value
            d['host'] = self._host.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class ChatGPTCreds(CredsForm):
    def create(self):
        super().create()
        self._organization = self.add(npyscreen.TitleText, name="Organization", align="^", color="IMPORTANT",)
        self._api_token = self.add(npyscreen.TitlePassword, name="API Token", align="^", color="IMPORTANT",)
    
        c_data = read_existing_creds(CREDS_DIR + 'chatgptcreds.json')
        if c_data:
            if c_data.get('organization'):
                self._organization.value = c_data.get('organization')
            if c_data.get('api_token'):
                self._api_token.value = c_data.get('api_token')

    def on_ok(self):
        if self._api_token.value and self._organization.value:
            creds_file = CREDS_DIR + 'chatgptcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("ChatGPT Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for ChatGPT is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("ChatGPT Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for ChatGPT is Missing")
            d = {}
            d['organization'] = self._organization.value
            d['api_token'] = self._api_token.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class JiraCreds(CredsForm):
    def create(self):
        super().create()
        self._url = self.add(npyscreen.TitleText, name="URL", align="^", color="IMPORTANT",)
        self._email = self.add(npyscreen.TitleText, name="Email", align="^", color="IMPORTANT",)
        self._api_token = self.add(npyscreen.TitlePassword, name="API Token", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'jiracreds.json')
        if c_data:
            if c_data.get('url'):
                self._url.value = c_data.get('url')
            if c_data.get('email'):
                self._email.value = c_data.get('email')
            if c_data.get('api_token'):
                self._api_token.value = c_data.get('api_token')
    
    def on_ok(self):
        if self._api_token.value and self._email.value and self._url.value:
            creds_file = CREDS_DIR + 'jiracreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Jira Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Jira is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Jira Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Jira is Missing")
            d = {}
            d['url'] = self._url.value
            d['email'] = self._email.value
            d['api_token'] = self._api_token.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()


class K8SCreds(CredsForm):
    def create(self):
        super().create()
        self._kubeconfig = self.add(npyscreen.MultiLineEditableBoxed, values=[""],name="~ Paste your Kube Configuration Below ~", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'k8screds.json')
        if c_data:
            self._kubeconfig.value = json.dumps(c_data)
    
    def on_ok(self):
        if self._kubeconfig.values:
            creds_file = CREDS_DIR + 'k8screds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("K8S Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for K8S is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("K8S Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for K8S is Missing")
            contents['metadata']['connectorData'] = json.dumps({"kubeconfig": self._kubeconfig.values})
    
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))

        super().on_ok()

class KafkaCreds(CredsForm):
    def create(self):
        super().create()
        self._sasl_username = self.add(npyscreen.TitleText, name="SASL Username", align="^", color="IMPORTANT",)
        self._sasl_password = self.add(npyscreen.TitlePassword, name="SASL Password", align="^", color="IMPORTANT",)
        self._broker = self.add(npyscreen.TitleText, name="Broker", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'kafkacreds.json')
        if c_data:
            if c_data.get('sasl_username'):
                self._sasl_username.value = c_data.get('sasl_username')
            if c_data.get('sasl_password'):
                self._sasl_password.value = c_data.get('sasl_password')
            if c_data.get('broker'):
                self._broker.value = c_data.get('broker')

    
    def on_ok(self):
        if self._sasl_password.value and self._sasl_username.value and self._broker.value:
            creds_file = CREDS_DIR + 'kafkacreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Kafka Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Kafka is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Kafka Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Kafka is Missing")
            d = {}
            d['sasl_username'] = self._sasl_username.value
            d['sasl_password'] = self._sasl_password.value
            d['broker'] = self._broker.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()


# We need to create over own Radio button here, reason
# being depending on the option selected, the other elements
# of the screen need to change. Example in case of
# Atlas, API key should be shown and not username and password.
class MongoSelectOneField(npyscreen.TitleSelectOne):
    def when_value_edited(self):
        if not self.value:
            return 
        
        v = int(self.value[0])
        if v == 0:
            self.parent.display_atlas_ui()
        elif v == 1:
            self.parent.display_auth_ui()
        else:
            raise AssertionError("Option value not recognized")

class MongoCreds(CredsForm):
    def create(self):
        super().create()
        self._host = self.add(npyscreen.TitleText, name="Host", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Port")
        self._port = self.add(IntegerTextfield, name="Port", value="27017", args="^", color="IMPORTANT",)
        self._schema = self.add(MongoSelectOneField,
                 values=["Atlas Schema", "Auth Schema"],
                 name="Pick One",
                 scroll_exit=True,
                 max_height=4)
        self._atlas_api_public_key = self.add(npyscreen.TitleText, name="Atlas API Public Key", args="^", color="IMPORTANT",)
        self._atlas_api_private_key = self.add(npyscreen.TitlePassword, name="Atlas API Private Key", args="^", color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", args="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", args="^", color="IMPORTANT",)
        self._atlas_api_private_key.hidden = True 
        self._atlas_api_public_key.hidden = True 
        self._username.hidden = True 
        self._password.hidden = True 

    def display_atlas_ui(self):
        self._atlas_api_private_key.hidden = False
        self._atlas_api_public_key.hidden = False 
        self._username.hidden = True 
        self._password.hidden = True 
        self._atlas_api_private_key.display()
        self._atlas_api_public_key.display()
        self._username.display()
        self._password.display()

    def display_auth_ui(self):
        self._atlas_api_private_key.hidden = True
        self._atlas_api_public_key.hidden = True 
        self._username.hidden = False 
        self._password.hidden = False 
        self._atlas_api_private_key.display()
        self._atlas_api_public_key.display()
        self._username.display()
        self._password.display()

    def on_ok(self):
        creds_file = CREDS_DIR + "mongodbcreds.json"
        with open(creds_file, 'r', encoding="utf-8") as f:
            contents = json.loads(f.read())
        d = {}
        if int(self._schema.value[0]) == 0:
            if self._atlas_api_public_key and self._atlas_api_private_key:
                d['port'] = self._port.value
                d['host'] = self._host.value 
                d['authentication'] = {}
                d['authentication']['auth_type'] = "Atlas Administrative API using HTTP Digest Authentication"
                d['authentication']['atlas_public_key'] = self._atlas_api_public_key.value
                d['authentication']['atlas_private_key'] = self._atlas_api_private_key.value

        elif int(self._schema.value[0]) == 1:
            if self._username and self._password:
                d['port'] = self._port.value
                d['host'] = self._host.value 
                d['authentication'] = {}
                d['authentication']['auth_type'] = "Basic Auth"
                d['authentication']['user_name'] = self._username.value 
                d['authentication']['password'] = self._password.value 
        else:
            raise AssertionError("Unknown Option, not able to save credential")
        if d:
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
                
        super().on_ok()

class MySQLCreds(CredsForm):
    def create(self):
        super().create()
        self._user = self.add(npyscreen.TitleText, name="User", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Port", align="^", color="IMPORTANT",)
        self._port = self.add(IntegerTextfield, name="Port", value="3306", align="^", color="IMPORTANT",)
        self._host = self.add(npyscreen.TitleText, name="Host", align="^", color="IMPORTANT",)
        self._dbname = self.add(npyscreen.TitleText, name="DB Name", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'mysqlcreds.json')
        if c_data:
            if c_data.get('User'):
                self._user.value = c_data.get('User')
            if c_data.get('Password'):
                self._password.value = c_data.get('Password')
            if c_data.get('Host'):
                self._host.value = c_data.get('Host')
            if c_data.get('DBName'):
                self._dbname.value = c_data.get('DBName')

    def on_ok(self):
        if self._password.value and self._user.value and self._port.value and self._host.value and self._dbname.value:
            creds_file = CREDS_DIR + 'mysqlcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("MySQL Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for MySQL is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("MySQL Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for MySQL is Missing")
            d = {}
            d['User'] = self._user.value
            d['Password'] = self._password.value
            d['Port'] = self._port.value 
            d['Host'] = self._host.value 
            d['DBName'] = self._dbname.value 
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()


class PostgresCreds(CredsForm):
    def create(self):
        super().create()
        self._user = self.add(npyscreen.TitleText, name="User", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Port", align="^", color="IMPORTANT",)
        self._port = self.add(IntegerTextfield, name="Port", align="^", value="5432", color="IMPORTANT",)
        self._host = self.add(npyscreen.TitleText, name="Host", align="^", color="IMPORTANT",)
        self._dbname = self.add(npyscreen.TitleText, name="DB Name", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'postgrescreds.json')
        if c_data:
            if c_data.get('User'):
                self._user.value = c_data.get('User')
            if c_data.get('Password'):
                self._password.value = c_data.get('Password')
            if c_data.get('Host'):
                self._host.value = c_data.get('Host')
            if c_data.get('DBName'):
                self._dbname.value = c_data.get('DBName')

    def on_ok(self):
        if self._password.value and self._user.value and self._port.value and self._host.value and self._dbname.value:
            creds_file = CREDS_DIR + 'postgrescreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("PostgreSQL Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for PostgreSQL is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("PostgreSQL Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for PostgreSQL is Missing")
            d = {}
            d['User'] = self._user.value
            d['Password'] = self._password.value
            d['Port'] = self._port.value 
            d['Host'] = self._host.value 
            d['DBName'] = self._dbname.value 
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class RestCreds(CredsForm):
    def create(self):
        super().create()
        self._url = self.add(npyscreen.TitleText, name="URL", align="^", color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self.add(npyscreen.TitleFixedText, name="Additional Headers", align="^", color="IMPORTANT",)
        self._key = self.add(npyscreen.TitleText, name="Key", align="^", color="IMPORTANT",)
        self._value = self.add(npyscreen.TitleText, name="Value", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'restcreds.json')
        if c_data:
            if c_data.get('username'):
                self._username.value = c_data.get('username')
            if c_data.get('password'):
                self._password.value = c_data.get('password')
            if c_data.get('base_url'):
                self._url.value = c_data.get('base_url')
            if c_data.get('headers'):
                #self._key.value = [x for x in c_data.get('headers').keys()][0]
                #self._value.value = [x for x in c_data.get('headers').values()][0]
                self._key.value = list(c_data.get('headers').keys())[0]
                self._value.value = list(c_data.get('headers').values())[0]

    def on_ok(self):
        if self._password.value and self._username.value and self._url.value:
            creds_file = CREDS_DIR + 'restcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("REST Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for REST is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("REST Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for REST is Missing")
            d = {}
            d['username'] = self._username.value
            d['password'] = self._password.value
            d['base_url'] = self._url.value 
            if self._key.value and self._key.value:
                d['headers'] = {}
                d['headers'][self._key.value] = self._value.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

class SlackCreds(CredsForm):
    def create(self):
        super().create()
        self._oauth_token = self.add(npyscreen.TitlePassword, name="OAuth Token", align="^", color="IMPORTANT",)
        c_data = read_existing_creds(CREDS_DIR + 'slackcreds.json')
        if c_data:
            if c_data.get('bot_user_oauth_token'):
                self._oauth_token.value = c_data.get('bot_user_oauth_token')

    def on_ok(self):
        if self._oauth_token.value:
            creds_file = CREDS_DIR + 'slackcreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("SLACK Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for SLACK is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("SLACK Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for SLACK is Missing")
            d = {}
            d['bot_user_oauth_token'] = self._oauth_token.value
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

# Similar to MongoDB creds, here we implement custom
# Radio button class to change the UI for PEM and basic Auth 
# types.

class SSHSelectOneField(npyscreen.TitleSelectOne):
    def when_value_edited(self):
        if not self.value:
            return
        try:
            v = int(self.value[0])
        except ValueError:
            v = 0
        if v == 0:
            self.parent.display_auth_ui()
        elif v == 1:
            self.parent.display_pem_ui()
        else:
            raise AssertionError("Option value not recognized")
        
class SSHCreds(CredsForm):
    def create(self):
        super().create()
        self.add(npyscreen.TitleFixedText, name="Port")
        self._port = self.add(IntegerTextfield, name="Port", value='22', args="^", color="IMPORTANT",)
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._schema = self.add(SSHSelectOneField,
                 values=["Basic Auth", "PEM File"],
                 name="Pick One",
                 scroll_exit=True,
                 max_height=2)
        self._pemfile = self.add(npyscreen.TitleText, name="~ Paste your PEM File Below ~", align="^", color="IMPORTANT")
        self._basic_auth = self.add(npyscreen.TitlePassword, name="Password", args="^", color="IMPORTANT",)
        self._pemfile.hidden = True
        self._basic_auth.hidden = True 

    def display_auth_ui(self):
        self._pemfile.hidden = True
        self._basic_auth.hidden = False 
        self._pemfile.display()
        self._basic_auth.display()
    
    def display_pem_ui(self):
        self._pemfile.hidden = False 
        self._basic_auth.hidden = True 
        self._pemfile.display()
        self._basic_auth.display()

    def on_ok(self):
        creds_file = CREDS_DIR + "sshcreds.json"
        with open(creds_file, 'r', encoding="utf-8") as f:
            contents = json.loads(f.read())
        d = {}
        if int(self._schema.value[0]) == 0:
            if self._username.value and self._port.value and self._basic_auth.value:
                d['port'] = self._port.value
                d['username'] = self._username.value 
                d['authentication'] = {}
                d['authentication']['auth_type'] = "Basic Auth"
                d['authentication']['password'] = self._basic_auth.value

        elif int(self._schema.value[0]) == 1:
            if self._username.value and self._pemfile.value and self._port.value:
                d['port'] = self._port.value
                d['username'] = self._username.value 
                d['authentication'] = {}
                d['authentication']['auth_type'] = "API Token"
                d['authentication']['private_key'] = json.dumps(self._pemfile.value) 
        else:
            raise AssertionError("Unknown Option, not able to save credential")
        if d:
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()


class SalesforceCreds(CredsForm):
    def create(self):
        super().create()
        self._username = self.add(npyscreen.TitleText, name="Username", align="^", color="IMPORTANT",)
        self._password = self.add(npyscreen.TitlePassword, name="Password", align="^", color="IMPORTANT",)
        self._security_token = self.add(npyscreen.TitlePassword, name="Security Token", align="^", color="IMPORTANT",)

        c_data = read_existing_creds(CREDS_DIR + 'salesforcecreds.json')
        if c_data:
            if c_data.get('Username'):
                self._username.value = c_data.get('Username')
            if c_data.get('Password'):
                self._password.value = c_data.get('Password')
            if c_data.get('Security_Token'):
                self._security_token.value = c_data.get('Security_Token')

    def on_ok(self):
        if self._password.value and self._username.value and self._security_token.value:
            creds_file = CREDS_DIR + 'salesforcecreds.json'
            if os.path.exists(creds_file) is False:
                npyscreen.notify("Salesforce Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Salesforce is Missing")
            with open(creds_file, 'r', encoding="utf-8") as f:
                contents = json.loads(f.read())
            if not contents:
                npyscreen.notify("Salesforce Credential File is Missing! Cannot proceed further. Contact support@unskript.com")
                raise AssertionError("Credential file for Salesforce is Missing")
            d = {}
            d['Username'] = self._username.value
            d['Password'] = self._password.value
            d['Security_Token'] = self._security_token.value 
            contents['metadata']['connectorData'] = json.dumps(d)
            with open(creds_file, 'w', encoding="utf-8") as f:
                f.write(json.dumps(contents, indent=2))
        super().on_ok()

# Dont implement credential class below this line.
# Lest wrap everything up into a single callable 
# function. We use this function when we import
# from the unskript-client.py. It can also
# be used as a standalone application too.

def main():
    creds_app = CredsApp()
    creds_app.run()


if __name__ == '__main__':
    main()
