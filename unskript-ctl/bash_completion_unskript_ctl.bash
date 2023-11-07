#!/bin/bash

_unskript-client-completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    connector_list=("aws" "k8s" "postgres" "mongodb" "elasticsearch" "vault" "ssh" "keycloak" "github" "redis")


    # Find the absolute path of unskript-client.py
    local unskript_client_script
    unskript_client_script="$(which unskript_ctl.py)"

    if [ -n "$unskript_client_script" ]; then
        # Check if the script exists and save check names
        if [ ! -f "/tmp/allopts.txt" ]; then
             /usr/bin/env python "$unskript_client_script" -h > /tmp/allopts.txt
        fi
        if [ ! -f "/tmp/checknames.txt" ]; then
            /usr/bin/env python "$unskript_client_script" --save-check-names /tmp/checknames.txt

        fi
    fi
    # Define options with each option on a separate line using newline characters
    opts="--run --list --show --debug --create-credential"

    # Completion logic
    case "${prev}" in
        -r|--run)
            # Provide completion suggestions for runbook filenames
            COMPREPLY=( $(compgen -W "--script --runbook --check" -- "${cur}" -o nospace) )
            return 0
            ;;

        -l|--list)
            # Provide completion suggestions for running script
            COMPREPLY=( $(compgen -W "--runbooks --failed-checks --checks --credential" -- "${cur}" -o nospace) )
            return 0
            ;;

        -s|--show)
            case ${prev} in
                --audit-trail)
                    COMPREPLY=( $(compgen -W "--all --type --execution-id" -- "${cur}" -o nospace) )
                    ;;
                --failed-logs)
                    COMPREPLY=( $(compgen -W "--execution-id <EXECUTION_ID>" -- "${cur}" -o nospace) )
                    ;;
                *)
                    COMPREPLY=( $(compgen -W "--audit-trail --failed-logs" -- "${cur}" -o nospace) )
                    ;;
            esac 
            return 0
            ;;
        -d|--debug)
            COMPREPLY=( $(compgen -W "--start --stop" -- "${cur}" -o nospace) )    
            return 0
            ;;

        *)  # Default: Provide completion suggestions for global options             
            if [[ (" ${COMP_WORDS[*]} " == *"-r --check --name "* )\
                 || (" ${COMP_WORDS[*]} " == *"--run --check --name "* ) \
                 || (" ${COMP_WORDS[*]} " =~ *"--run [^[:space:]]+ --check --name "* ) \
                 || (" ${COMP_WORDS[*]} " =~ *"-run  [^[:space:]]+ --check --name "* ) \
                 || (" ${COMP_WORDS[*]} " == *"--check --name "* ) ]];
            then
                cur=${cur#--check}
                cur=${cur#--name}
                opt2="$(grep -E "^${cur}" /tmp/checknames.txt)"
                COMPREPLY=( $(compgen -W "${opt2}" -o nospace) )
                compopt -o nospace
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " =~ *"--check --name [^[:space:]]+ "* )  \
                   || (" ${COMP_WORDS[*]} " == *"--check --all"* )  \
                   || (" ${COMP_WORDS[*]} " == *"--check --type \ [^[:space:]]+ "* )  \
                   || (" ${COMP_WORDS[*]} " == *"--check --type \ [^[:space:]]+ "* ) ]];
            then
                COMPREPLY=( $(compgen -W "--script SCRIPT_NAME" -- "${cur}" -o nospace) )
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-r --check --type "* )  \
                  || (" ${COMP_WORDS[*]} " == *"--run --check --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"-l --checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"--list --checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"-l --failed-checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"--list --failed-checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"-s --audit-trail --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"--show --audit-trail --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"--check --type "* ) \
                  ]];

            then
                COMPREPLY=( $(compgen -W "aws k8s postgres mongodb elasticsearch vault ssh keycloak redis" -o nospace) )
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " == *"-r --check --all "*) \
                  || (" ${COMP_WORDS[*]} " == *"--run --check --all "* ) \
                  || (" ${COMP_WORDS[*]} " == *"--check --all "* ) \
                  && (" ${COMP_WORDS[*]} " != *"--run --check --all --report"* ) ]];
            then
                COMPREPLY=( $(compgen -W "--script SCRIPT_NAME --report" -o nospace) )
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " == *"-r [^[:space:]]+ --check "*) \
                  || (" ${COMP_WORDS[*]} " == *"--run [^[:space:]]+ --check "*) ]];
            then
                COMPREPLY=( $(compgen -W "--all --type --name" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-l --failed-checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"--list --failed-checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"-l --checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"--list --checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"-s --audit-trail --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"--show --audit-trail --all"*) \
                  ]];
            then
                return 0
            fi


            if [[ (" ${COMP_WORDS[*]} " == *"-l --failed-checks "*) \
                  || (" ${COMP_WORDS[*]} " == *"--list --failed-checks "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-l --checks "*) \
                  || (" ${COMP_WORDS[*]} " == *"--list --checks "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type" -- "${cur}" -o nospace) ) 
                return 0
            fi
           
            if [[ (" ${COMP_WORDS[*]} " == *"-s --audit-trail --execution_id"*) \
                  || (" ${COMP_WORDS[*]} " == *"--show --audit-trail --execution_id"*) \
                  && (" ${COMP_WORDS[*]} " != *"--show --audit-trail --execution_id EXECUTION_ID"*) \
                  && (" ${COMP_WORDS[*]} " != *"--show --audit-trail --execution_id EXECUTION_ID"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "EXECUTION_ID" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-s --failed-logs"*) \
                  || (" ${COMP_WORDS[*]} " == *"--show --failed-logs "*) ]];
            then
                COMPREPLY=( $(compgen -W "--execution_id EXECUTION_ID" -- "${cur}" -o nospace) ) 
                return 0
            fi


            if [[ (" ${COMP_WORDS[*]} " == *"-s --audit-trail "*) \
                  || (" ${COMP_WORDS[*]} " == *"--show --audit-trail "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type --execution_id" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-r --runbook "*) \
                  || (" ${COMP_WORDS[*]} " == *"--run --runbook "*) \
                  && (" ${COMP_WORDS[*]} " != *"--run --runbook RUNBOOK"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "RUNBOOK" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-r --script "*) \
                  || (" ${COMP_WORDS[*]} " == *"--run --script "*) \
                  && (" ${COMP_WORDS[*]} " != *"--run --script SCRIPT_FILE"*) \
                  && (" ${COMP_WORDS[*]} " != *"-r --script SCRIPT_FILE"*) \
                  && (" ${COMP_WORDS[*]} " != *"--check "*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "SCRIPT_FILE" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " =~ *"-r --script  [^[:space:]]+"*) \
                  || (" ${COMP_WORDS[*]} " =~ *"--run --script  [^[:space:]]+"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "--check" -- "${cur}" -o nospace) ) 
                echo "D1"
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-r --script \ [^[:space:]]+ --check"*) \
                  || (" ${COMP_WORDS[*]} " == *"--run --script \ [^[:space:]]+ --check"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "--type --all --name" -- "${cur}" -o nospace) ) 
                echo "D2"
                return 0
            fi



            if [[ (" ${COMP_WORDS[*]} " == *"-r --check --all --report"*) \
                  || (" ${COMP_WORDS[*]} " == *"--run --check --all --report "*)]];
            then
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-d --start"*) \
                  || (" ${COMP_WORDS[*]} " == *"--debug --start "*) \
                  && (" ${COMP_WORDS[*]} " != *"--debug --start --config OVPNFILE"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "--config OVPNFILE" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"-d --stop"*) \
                  || (" ${COMP_WORDS[*]} " == *"--debug --stop "*) \
                  ]];
            then
                return 0
            fi

            if [[  " ${COMP_WORDS[*]} " == *"--create-credential"* ]];
            then
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"--run"* ) \
                || (" ${COMP_WORDS[*]} " == *"-r"* ) \
                && ( "${COMP_WORDS[*]} " != *"--check"* ) \
                && (" ${COMP_WORDS[*]} " == *"--script \ [^[:space:]]+"* )]];
            then
                if [[ " ${COMP_WORDS[*]} " == *"--check"* ]];
                then 
                    COMPREPLY=( $(compgen -W "--all --type --name" -- "${cur}" -o nospace) )
                else 
                    COMPREPLY=( $(compgen -W "--check" -- "${cur}" -o nospace) )
                fi
                return 0
            fi

            if [ "${#COMP_WORDS[@]}" != "1" ];
            then 
                COMPREPLY=( $(compgen -W "${opts}" -- "${cur}" -o nospace) )
                return 0
            fi

            return 0
            ;;
    esac
}

# Register the completion function for unskript-client.py
complete -F _unskript-client-completion unskript-ctl.sh
