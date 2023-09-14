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

from creds_ui import main as ui
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

def main():
    """main: This is the Main function that interfaces with the creds-ui"""
    try:
        schema_json = json.loads(credential_schemas)
    except Exception as e:
        print(f"Exception occured {e}")
        return
  
    parser = ArgumentParser(prog='unskript-ctl')
    description = ""
    description = description + str("\n")
    description = description + str("\t  Credential App \n")
    parser.description = description

    parser.add_argument('-o', '--output-directory', type=str, required=True,
                        help="Output Directory to store credentials, should be absolute path")
    

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    if args.output_directory not in ('', None):
        if os.path.exists(args.output_directory):
            if os.path.isdir(args.output_directory):
                os.environ['CREDS_DIR'] = args.output_directory
            else:
                print(f"ERROR: Given Path {args.output_directory} is not a directory. A File by that name already exists!")
                sys.exit(0)
        else:
            print(f"CREATING DIRECTORY: {args.output_directory}")
            os.makedirs(args.output_directory)
            os.environ['CREDS_DIR'] = args.output_directory
    else:
        print(f"Output Directory Name is empty {args.output_directory}")
        sys.exit(0)
    
    create_stub_cred_files(args.output_directory)
    ui(schema_json=schema_json, creds_dir=args.output_directory) 

if __name__ == '__main__':
    main()