"""This file implements a wrapper over creds-ui"""
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
import sys
import json

#from creds_ui import main as ui
from argparse import ArgumentParser, REMAINDER

# CONSTANTS USED IN THIS FILE
STUB_FILE = "stub_creds.json"

# Note: Any change in credential_schema should also be followed by
# the corresponding change in creds-ui too.
credential_schemas = '''
[
    {
      "title": "AWSSchema",
      "type": "object",
      "properties": {
        "authentication": {
          "title": "Authentication",
          "discriminator": "auth_type",
          "anyOf": [
            {
              "$ref": "#/definitions/AccessKeySchema"
            }
          ]
        }
      },
      "required": [
        "authentication"
      ],
      "definitions": {
        "AccessKeySchema": {
          "title": "Access Key",
          "type": "object",
          "properties": {
            "auth_type": {
              "title": "Auth Type",
              "enum": [
                "Access Key"
              ],
              "type": "string"
            },
            "access_key": {
              "title": "Access Key",
              "description": "Access Key to use for authentication.",
              "type": "string"
            },
            "secret_access_key": {
              "title": "Secret Access Key",
              "description": "Secret Access Key to use for authentication.",
              "type": "string",
              "writeOnly": true,
              "format": "password"
            }
          },
          "required": [
            "auth_type",
            "access_key",
            "secret_access_key"
          ]
        }
      }
    },
    {
      "title": "GCPSchema",
      "type": "object",
      "properties": {
        "credentials": {
          "title": "Google Cloud Credentials JSON",
          "description": "Contents of the Google Cloud Credentials JSON file.",
          "type": "string"
        }
      },
      "required": [
        "credentials"
      ]
    },
    {
      "title": "ElasticSearchSchema",
      "type": "object",
      "properties": {
        "host": {
          "title": "Host Name",
          "description": "Elasticsearch Node URL. For eg: https://localhost:9200",
          "type": "string"
        },
        "username": {
          "title": "Username",
          "description": "Username for Basic Auth.",
          "default": "",
          "type": "string"
        },
        "password": {
          "title": "Password",
          "description": "Password for Basic Auth.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "api_key": {
          "title": "API Key",
          "description": "API Key based authentication.",
          "default": "",
          "type": "string"
        }
      },
      "required": [
        "host"
      ]
    },
    {
      "title": "GrafanaSchema",
      "type": "object",
      "properties": {
        "api_key": {
          "title": "API Token",
          "description": "API Token to authenticate to grafana.",
          "default": "",
          "type": "string"
        },
        "username": {
          "title": "Username",
          "description": "Username of the grafana user.",
          "default": "",
          "type": "string"
        },
        "password": {
          "title": "Password",
          "description": "Password to authenticate to grafana.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "host": {
          "title": "Hostname",
          "description": "Hostname of the grafana.",
          "type": "string"
        }
      },
      "required": [
        "host"
      ]
    },
    {
        "title": "RedisSchema",
        "type": "object",
        "properties": {
          "db": {
            "title": "Database",
            "description": "ID of the database to connect to.",
            "default": 0,
            "type": "integer"
          },
        "host": {
          "title": "Hostname",
          "description": "Hostname of the redis server.",
          "type": "string"
        },
        "username": {
          "title": "Username",
          "description": "Username to authenticate to redis.",
          "default": "",
          "type": "string"
        },
        "password": {
          "title": "Password",
          "description": "Password to authenticate to redis.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "port": {
          "title": "Port",
          "description": "Port on which redis server is listening.",
          "default": 6379,
          "type": "integer"
        },
        "use_ssl": {
          "title": "Use SSL",
          "description": "Use SSL for communicating to Redis host.",
          "default": false,
          "type": "boolean"
        }
      },
      "required": [
        "host"
      ]
    },
    {
      "title": "JenkinsSchema",
      "type": "object",
      "properties": {
        "url": {
          "title": "Jenkins url",
          "description": "Full Jenkins URL.",
          "type": "string"
        },
        "user_name": {
          "title": "Username",
          "description": "Username to authenticate with Jenkins.",
          "default": "",
          "type": "string"
        },
        "password": {
          "title": "Password",
          "description": "Password or API Token to authenticate with Jenkins.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        }
      },
      "required": [
        "url"
      ]
    },
    {
      "title": "GithubSchema",
      "type": "object",
      "properties": {
        "token": {
          "title": "Access token",
          "description": "Github Personal Access Token.",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "hostname": {
          "title": "Custom Hostname",
          "description": "Custom hostname for Github Enterprise Version.",
          "default": "",
          "type": "string"
        }
      },
      "required": [
        "token"
      ]
    },
    {
      "title": "NetboxSchema",
      "type": "object",
      "properties": {
        "host": {
          "title": "Netbox Host",
          "description": "Address of Netbox host",
          "type": "string"
        },
        "token": {
          "title": "Token",
          "description": "Token value to authenticate write requests.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "threading": {
          "title": "Threading",
          "description": "Enable for multithreaded calls like .filter() and .all() queries. To enable set to True ",
          "type": "boolean"
        }
      },
      "required": [
        "host"
      ]
    },
    {
      "title": "NomadSchema",
      "type": "object",
      "properties": {
        "host": {
          "title": "Nomad IP address",
          "description": "IP address of Nomad host",
          "type": "string"
        },
        "timeout": {
          "title": "Timeout(seconds)",
          "description": "Timeout in seconds to retry connection",
          "default": 5,
          "type": "integer"
        },
        "token": {
          "title": "Token",
          "description": "Token value to authenticate requests to the cluster when using namespace",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "verify_certs": {
          "title": "Verify certs",
          "description": "Verify server ssl certs. This can be set to true when working with private certs.",
          "type": "boolean"
        },
        "secure": {
          "title": "Secure",
          "description": "HTTPS enabled?",
          "type": "boolean"
        },
        "namespace": {
          "title": "Namespace",
          "description": "Name of Nomad Namespace. By default, the default namespace will be considered.",
          "type": "string"
        }
      },
      "required": [
        "host"
      ]
    },
    {
      "title": "ChatGPTSchema",
      "type": "object",
      "properties": {
        "organization": {
          "title": "Organization ID",
          "description": "Identifier for the organization which is sometimes used in API requests. Eg: org-s8OPLNKVjsDAjjdbfTuhqAc",
          "default": "",
          "type": "string"
        },
        "api_token": {
          "title": "API Token",
          "description": "API Token value to authenticate requests.",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        }
      },
      "required": [
        "api_token"
      ]
    },
    {
      "title": "OpsgenieSchema",
      "type": "object",
      "properties": {
          "api_token": {
            "title": "Api Token",
            "description": "Api token to authenticate Opsgenie: GenieKey",
            "type": "string",
            "writeOnly": true,
            "format": "password"
          }
      },
      "required": [
          "api_token"
      ]
    },
    {
      "title": "JiraSchema",
      "type": "object",
      "properties": {
        "url": {
          "title": "URL",
          "description": "URL of jira server.",
          "type": "string"
        },
        "email": {
          "title": "Email",
          "description": "Email to authenticate to jira.",
          "type": "string"
        },
        "api_token": {
          "title": "Api Token",
          "description": "Api token to authenticate to jira.",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        }
      },
      "required": [
        "url",
        "email",
        "api_token"
      ]
    },
    {
      "title": "K8SSchema",
      "type": "object",
      "properties": {
        "kubeconfig": {
          "title": "Kubeconfig",
          "description": "Contents of the kubeconfig file.",
          "type": "string"
        }
      },
      "required": [
        "kubeconfig"
      ]
    },
    {
      "title": "KafkaSchema",
      "type": "object",
      "properties": {
        "broker": {
          "title": "Broker",
          "description": "host[:port] that the producer should contact to bootstrap initial cluster metadata. Default port is 9092",
          "type": "string"
        },
        "sasl_username": {
          "title": "SASL Username",
          "description": "Username for SASL PlainText Authentication.",
          "default": "",
          "type": "string"
        },
        "sasl_password": {
          "title": "SASL Password",
          "description": "Password for SASL PlainText Authentication.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        }
      },
      "required": [
        "broker"
      ]
    },
    {
     "title": "MongoDBSchema",
     "type": "object",
     "properties": {
      "host": {
        "title": "Host",
        "description": "Full MongoDB URI, in addition to simple hostname. It also supports mongodb+srv:// URIs",
        "type": "string"
      },
      "port": {
        "title": "Port",
        "description": "Port on which mongoDB server is listening.",
        "default": 27017,
        "type": "integer"
      },
      "authentication": {
        "title": "Authentication",
        "discriminator": "auth_type",
        "anyOf": [
          {
            "$ref": "#/definitions/AtlasSchema"
          },
          {
            "$ref": "#/definitions/AuthSchema"
          }
        ]
      }
    },
    "required": [
      "host",
      "authentication"
    ],
    "definitions": {
      "AtlasSchema": {
        "title": "AtlasSchema",
        "type": "object",
        "properties": {
          "auth_type": {
            "title": "Auth Type",
            "enum": [
              "Atlas Administrative API using HTTP Digest Authentication"
            ],
            "type": "string"
          },
          "atlas_public_key": {
            "title": "Atlas API Public Key",
            "description": "The public key acts as the username when making API requests",
            "default": "",
            "type": "string"
          },
          "atlas_private_key": {
            "title": "Atlas API Private Key",
            "description": "The private key acts as the password when making API requests",
            "default": "",
            "type": "string",
            "writeOnly": true,
            "format": "password"
          }
        },
        "required": [
          "auth_type"
        ]
      },
      "AuthSchema": {
        "title": "AuthSchema",
        "type": "object",
        "properties": {
          "auth_type": {
            "title": "Auth Type",
            "enum": [
              "Basic Auth"
            ],
            "type": "string"
          },
          "user_name": {
            "title": "Username",
            "description": "Username to authenticate with MongoDB.",
            "default": "",
            "type": "string"
          },
          "password": {
            "title": "Password",
            "description": "Password to authenticate with MongoDB.",
            "default": "",
            "type": "string",
            "writeOnly": true,
            "format": "password"
          }
        },
        "required": [
          "auth_type"
        ]
      }
     }
    },
    {
      "title": "MySQLSchema",
      "type": "object",
      "properties": {
        "DBName": {
          "title": "Database name",
          "description": "Name of the database to connect to MySQL.",
          "type": "string"
        },
        "User": {
          "title": "Username",
          "description": "Username to authenticate to MySQL.",
          "default": "",
          "type": "string"
        },
        "Password": {
          "title": "Password",
          "description": "Password to authenticate to MySQL.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "Host": {
          "title": "Hostname",
          "description": "Hostname of the MySQL server.",
          "type": "string"
        },
        "Port": {
          "title": "Port",
          "description": "Port on which MySQL server is listening.",
          "default": 5432,
          "type": "integer"
        }
      },
      "required": [
        "DBName",
        "Host"
      ]
    },
    {
      "title": "PostgreSQLSchema",
      "type": "object",
      "properties": {
        "DBName": {
          "title": "Database name",
          "description": "Name of the database to connect to.",
          "type": "string"
        },
        "User": {
          "title": "Username",
          "description": "Username to authenticate to postgres.",
          "default": "",
          "type": "string"
        },
        "Password": {
          "title": "Password",
          "description": "Password to authenticate to postgres.",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "Host": {
          "title": "Hostname",
          "description": "Hostname of the postgres server.",
          "type": "string"
        },
        "Port": {
          "title": "Port",
          "description": "Port on which postgres server is listening.",
          "default": 5432,
          "type": "integer"
        }
      },
      "required": [
        "DBName",
        "Host"
      ]
    },
    {
      "title": "RESTSchema",
      "type": "object",
      "properties": {
        "base_url": {
          "title": "Base URL",
          "description": "Base URL of REST server",
          "type": "string"
        },
        "username": {
          "title": "Username",
          "description": "Username for Basic Authentication",
          "default": "",
          "type": "string"
        },
        "password": {
          "title": "Password",
          "description": "Password for the Given User for Basic Auth",
          "default": "",
          "type": "string",
          "writeOnly": true,
          "format": "password"
        },
        "headers": {
          "title": "Headers",
          "description": "A dictionary of http headers to be used to communicate with the host.Example: Authorization: bearer my_oauth_token_to_the_host .These headers will be included in all requests.",
          "type": "object"
        }
      },
      "required": [
        "base_url"
      ]
    },
    {
      "title": "SlackSchema",
      "type": "object",
      "properties": {
        "bot_user_oauth_token": {
          "title": "OAuth Access Token",
          "description": "OAuth Access Token of the Slack app.",
          "type": "string"
        }
      },
      "required": [
        "bot_user_oauth_token"
      ]
    },
    {
      "title": "SSHSchema",
      "type": "object",
      "properties": {
        "port": {
          "title": "Port",
          "description": "SSH port to connect to.",
          "default": 22,
          "type": "integer"
        },
        "username": {
          "title": "Username",
          "description": "Username to use for authentication",
          "default": "",
          "type": "string"
        },
        "proxy_host": {
          "title": "Proxy host",
          "description": "SSH host to tunnel connection through so that SSH clients connect to host via client -> proxy_host -> host.",
          "type": "string"
        },
        "proxy_user": {
          "title": "Proxy user",
          "description": "User to login to proxy_host as. Defaults to username.",
          "type": "string"
        },
        "proxy_port": {
          "title": "Proxy port",
          "description": "SSH port to use to login to proxy host if set. Defaults to 22.",
          "default": 22,
          "type": "integer"
        },
        "authentication": {
          "title": "Authentication",
          "discriminator": "auth_type",
          "anyOf": [
            {
              "$ref": "#/definitions/AuthSchema"
            },
            {
              "$ref": "#/definitions/PrivateKeySchema"
            },
            {
              "$ref": "#/definitions/VaultSchema"
            },
            {
              "$ref": "#/definitions/KerberosSchema"
            }
          ]
        }
      },
      "required": [
        "authentication"
      ],
      "definitions": {
        "AuthSchema": {
          "title": "Basic Auth",
          "type": "object",
          "properties": {
            "auth_type": {
              "title": "Auth Type",
              "enum": [
                "Basic Auth"
              ],
              "type": "string"
            },
            "password": {
              "title": "Password",
              "description": "Password to use for password authentication.",
              "default": "",
              "type": "string",
              "writeOnly": true,
              "format": "password"
            },
            "proxy_password": {
              "title": "Proxy user password",
              "description": "Password to login to proxy_host with. Defaults to no password.",
              "type": "string"
            }
          },
          "required": [
            "auth_type"
          ]
        },
        "PrivateKeySchema": {
          "title": "Pem File",
          "type": "object",
          "properties": {
            "auth_type": {
              "title": "Auth Type",
              "enum": [
                "API Token"
              ],
              "type": "string"
            },
            "private_key": {
              "title": "Private Key File",
              "description": "Contents of the Private Key File to use for authentication.",
              "default": "",
              "type": "string"
            },
            "proxy_private_key": {
              "title": "Proxy Private Key File",
              "description": "Private key file to be used for authentication with proxy_host.",
              "type": "string"
            }
          },
          "required": [
            "auth_type"
          ]
        },
        "VaultSchema": {
          "title": "Vault",
          "type": "object",
          "properties": {
            "auth_type": {
              "title": "Auth Type",
              "enum": [
                "Vault"
              ],
              "type": "string"
            },
            "vault_url": {
              "title": "Vault URL",
              "description": "Vault URL eg: http://127.0.0.1:8200",
              "type": "string"
            },
            "vault_secret_path": {
              "title": "SSH Secret Path",
              "description": "The is the path in the Vault Configuration tab of ssh secret. eg: ssh",
              "type": "string"
            },
            "vault_role": {
              "title": "Vault Role",
              "description": "Vault role associated with the above ssh secret.",
              "type": "string"
            }
          },
          "required": [
            "auth_type",
            "vault_url",
            "vault_secret_path",
            "vault_role"
          ]
        },
        "KerberosSchema": {
          "title": "Kerberos",
          "type": "object",
          "properties": {
            "auth_type": {
              "title": "Auth Type",
              "enum": [
                "Kerberos"
              ],
              "type": "string"
            },
            "user_with_realm": {
              "title": "Kerberos user@REALM",
              "description": "Kerberos UserName like user@EXAMPLE.COM REALM is usually defined as UPPER-CASE",
              "type": "string"
            },
            "kdc_server": {
              "title": "KDC Server",
              "description": "KDC Server Domain Name. like kdc.example.com",
              "type": "string"
            },
            "admin_server": {
              "title": "Admin Server",
              "description": "Kerberos Admin Server. Normally same as KDC Server",
              "default": "",
              "type": "string"
            },
            "password": {
              "title": "Password",
              "description": "Password for the above Username",
              "default": "",
              "type": "string",
              "writeOnly": true,
              "format": "password"
            },
            "proxy_password": {
              "title": "Proxy user password",
              "description": "Password to login to proxy_host with. Defaults is no password.",
              "default": "",
              "type": "string",
              "writeOnly": true,
              "format": "password"
            }
          },
          "required": [
            "auth_type",
            "user_with_realm",
            "kdc_server"
          ]
        }
      }
    },
    {
      "title": "SalesforceSchema",
      "type": "object",
      "properties": {
      "Username": {
        "title": "Username",
        "description": "Username to authenticate to Salesforce.",
        "type": "string"
      },
      "Password": {
        "title": "Password",
        "description": "Password to authenticate to Salesforce.",
        "type": "string",
        "writeOnly": true,
        "format": "password"
      },
      "Security_Token": {
        "title": "Security token",
        "description": "Token to authenticate to Salesforce.",
        "type": "string"
      }
    },
    "required": [
      "Username",
      "Password",
      "Security_Token"
    ]
  }
  ]
'''

def create_stub_cred_files(dirname: str):
    """create_stub_cred_files This function creates the stub files needed by creds-ui"""
    if not os.path.exists(dirname):
        return

    # Lets read the Stubs Creds file and create placeholder files
    if not os.path.exists(STUB_FILE):
        print("Credential placeholder file JSON is missing. Please run this at unskript-ctl directory!")
        sys.exit(0)

    with open(STUB_FILE, 'r') as f:
        stub_creds_json = json.load(f)

    for cred in stub_creds_json:
        f_name = os.path.join(dirname, cred.get('display_name'))
        f_name = f_name + '.json'
        # Lets check if file already exists, if it does not, then create it
        if not os.path.exists(f_name):
            with open(f_name, 'w') as f:
                f.write(json.dumps(cred, indent=4))

#CREDS_DIR = os.environ.get('HOME') + "/.local/share/jupyter/metadata/credential-save/"
CREDS_DIR = os.environ.get('HOME') + "/creds/"

class CredentialsAdd():
    def __init__(self):
      create_stub_cred_files(CREDS_DIR)
      try:
        schema_json = json.loads(credential_schemas)
      except Exception as e:
        print(f"Exception occured {e}")
        return
      mainParser = ArgumentParser(prog='add_creds')
      description = ""
      description = description + str("\n")
      description = description + str("\t  Add credentials \n")
      mainParser.description = description
      mainParser.add_argument('-c', '--credential-type', choices=[
         'AWS',
         'K8S',
         'GCP',
         'Elasticsearch',
         'Redis',
         'PostGRES',
         'MongoDB',
         'Kafka'
         ], help='Credential type')

      args = mainParser.parse_args(sys.argv[1:3])
      if len(sys.argv) == 1:
          mainParser.print_help()
          sys.exit(0)

      getattr(self, args.credential_type)()

    def write_creds_to_file(self, json_file_name, data):
      creds_file = CREDS_DIR + json_file_name
      if os.path.exists(creds_file) is False:
          raise AssertionError(f"credential file {json_file_name} missing")

      with open(creds_file, 'r', encoding="utf-8") as f:
          contents = json.loads(f.read())
      if not contents:
          raise AssertionError(f"credential file {json_file_name} is invalid")

      contents['metadata']['connectorData'] = data

      with open(creds_file, 'w', encoding="utf-8") as f:
          f.write(json.dumps(contents, indent=2))

    def AWS(self):
      parser = ArgumentParser(description='Add AWS credential')
      parser.add_argument('-a', '--access-key', required=True, help='AWS Access Key')
      parser.add_argument('-s', '--secret-access-key', required=True, help='AWS Secret Access Key')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) != 4:
         parser.print_help()
         sys.exit(0)

      if args.access_key is None or args.secret_access_key is None:
          raise AssertionError('Access Key or Secret Access Key missing')

      d = {}
      d['authentication'] = {}
      d['authentication']['auth_type'] = "Access Key"
      d['authentication']['access_key'] =  args.access_key
      d['authentication']['secret_access_key'] = args.secret_access_key
      self.write_creds_to_file('awscreds.json', json.dumps(d))

    def K8S(self):
      parser = ArgumentParser(description='Add K8S credential')
      parser.add_argument('-k', '--kubeconfig', required=True, help='Contents of the kubeconfig file')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) != 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['kubeconfig'] = args.kubeconfig
      self.write_creds_to_file('k8screds.json', json.dumps(d))

    def GCP(self):
      parser = ArgumentParser(description='Add GCP credential')
      parser.add_argument('-g', '--gcp-credentials', help='Contents of the GCP credentials json file')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) != 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['credentials'] = args.gcp_credentials
      self.write_creds_to_file('gcpcreds.json', json.dumps(d))

    def Elasticsearch(self):
      parser = ArgumentParser(description='Add Elasticsearch credential')
      parser.add_argument('-s', '--host', required=True, help='''
                          Elasticsearch Node URL. For eg: https://localhost:9200.
                          NOTE: Please ensure that this is the Elastisearch URL and NOT Kibana URL.
                          ''')
      parser.add_argument('-a', '--api-key', help='API key')
      parser.add_argument('--no-verify-certs', action='store_true', help='Not verify server ssl certs. This can be set to true when working with private certs.')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) < 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['host'] = args.host
      if args.api_key is not None:
         d['api_key'] = args.api_key

      if args.no_verify_certs == True:
         d['verify_certs'] = False
      else:
         d['verify_certs'] = True

      self.write_creds_to_file('escreds.json', json.dumps(d))

    def Redis(self):
      parser = ArgumentParser(description='Add Redis credential')
      parser.add_argument('-s', '--host', required=True, help='Hostname of the redis server')
      parser.add_argument('-p', '--port', help='Port on which redis server is listening', type=int, default=6379)
      parser.add_argument('-u', '--username', help='Username')
      parser.add_argument('-pa', '--password', help='Password')
      parser.add_argument('-db', '--database', help='ID of the database to connect to', type=int)
      parser.add_argument('--use-ssl', action='store_false', help='Use SSL to connect to redis host')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) < 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['host'] = args.host
      d['port'] = args.port
      if args.username is not None:
         d['username'] = args.username
      if args.password is not None:
         d['password'] = args.password
      if args.database is not None:
         d['db'] = args.database
      d['use_ssl'] = args.use_ssl
      self.write_creds_to_file('rediscreds.json', json.dumps(d))

    def PostGRES(self):
      parser = ArgumentParser(description='Add POSTGRES credential')
      parser.add_argument('-s', '--host', required=True, help='Hostname of the PostGRES server')
      parser.add_argument('-p', '--port', help='Port on which PostGRES server is listening', type=int, default=5432)
      parser.add_argument('-db', '--database-name', help='Name of the database to connect to', required=True)
      parser.add_argument('-u', '--username', help='Username')
      parser.add_argument('-pa', '--password', help='Password')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) < 4:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['Host'] = args.host
      d['Port'] = args.port
      d['DBName'] = args.database_name
      if args.username is not None:
         d['User'] = args.username
      if args.password is not None:
         d['Password'] = args.password
      self.write_creds_to_file('postgrescreds.json', json.dumps(d))

    def MongoDB(self):
      parser = ArgumentParser(description='Add MongoDB credential')
      parser.add_argument('-s', '--host', required=True, help='Full MongoDB URI, in addition to simple hostname. It also supports mongodb+srv:// URIs"')
      parser.add_argument('-p', '--port', help='Port on which MongoDB server is listening', type=int, default=27017)
      parser.add_argument('-u', '--username', help='Username')
      parser.add_argument('-pa', '--password', help='Password')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) < 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['host'] = args.host
      d['port'] = args.port
      #TBD: Add support for atlas
      d['authentication'] = {}
      d['authentication']['auth_type'] = "Basic Auth"
      if args.username is not None:
        d['authentication']['user_name'] = args.username
      if args.password is not None:
        d['authentication']['password'] = args.password

      self.write_creds_to_file('mongodbcreds.json', json.dumps(d))

    def Kafka(self):
      parser = ArgumentParser(description='Add Kafka credential')
      parser.add_argument('-b', '--broker', required=True, help='''
                          host[:port] that the producer should contact to bootstrap initial cluster metadata. Default port is 9092.
                          ''')
      parser.add_argument('-u', '--sasl-username', help='Username for SASL PlainText Authentication.')
      parser.add_argument('-p', '--sasl-password', help='Password for SASL PlainText Authentication.')
      parser.add_argument('-z', '--zookeeper', help='Zookeeper connection string. This is needed to do health checks. Eg: host[:port]. The default port is 2182')
      args = parser.parse_args(sys.argv[3:])

      if len(sys.argv[3:]) < 2:
         parser.print_help()
         sys.exit(0)

      d = {}
      d['broker'] = args.broker
      if args.sasl_username is not None:
         d['sasl_username'] = args.sasl_username

      if args.sasl_password is not None:
         d['sasl_password'] = args.sasl_password

      if args.zookeeper is not None:
         d['zookeeper'] = args.zookeeper

      self.write_creds_to_file('kafkacreds.json', json.dumps(d))

if __name__ == '__main__':
    CredentialsAdd()
