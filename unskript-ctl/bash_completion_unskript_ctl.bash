#!/bin/bash

_unskript-client-completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    connector_list=("aws" "k8s" "postgres" "mongodb" "elasticsearch" "vault" "ssh" "keycloak" "github" "redis")


    # Find the absolute path of unskript-client.py
    local unskript_client_script
    unskript_client_script="$(which unskript_ctl_main.py)"

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
    opts="run list show debug --create-credential"

    # Completion logic
    case "${prev}" in
        run)
            # Provide completion suggestions for runbook filenames
            COMPREPLY=( $(compgen -W "--script  check" -- "${cur}" -o nospace) )
            return 0
            ;;

        list)
            # Provide completion suggestions for running script
            COMPREPLY=( $(compgen -W "failed-checks checks --credential" -- "${cur}" -o nospace) )
            return 0
            ;;

        show)
            case ${prev} in
                audit-trail)
                    COMPREPLY=( $(compgen -W "--all --type --execution_id" -- "${cur}" -o nospace) )
                    ;;
                failed-logs)
                    COMPREPLY=( $(compgen -W "--execution_id <EXECUTION_ID>" -- "${cur}" -o nospace) )
                    ;;
                *)
                    COMPREPLY=( $(compgen -W "audit-trail failed-logs" -- "${cur}" -o nospace) )
                    ;;
            esac 
            return 0
            ;;
        debug)
            COMPREPLY=( $(compgen -W "--start --stop" -- "${cur}" -o nospace) )    
            return 0
            ;;

        *)  # Default: Provide completion suggestions for global options             
            if [[ (" ${COMP_WORDS[*]} " == *"run check --name "* )\
                 || (" ${COMP_WORDS[*]} " =~ *"run [^[:space:]]+ check --name "* ) \
                 || (" ${COMP_WORDS[*]} " =~ *"run  [^[:space:]]+ check --name "* ) \
                 || (" ${COMP_WORDS[*]} " == *"check --name "* ) ]];
            then
                cur=${cur#--check}
                cur=${cur#--name}
                opt2="$(grep -E "^${cur}" /tmp/checknames.txt)"
                COMPREPLY=( $(compgen -W "${opt2}" -o nospace) )
                compopt -o nospace
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " =~ *"check --name [^[:space:]]+ "* )  \
                   || (" ${COMP_WORDS[*]} " == *"check --all"* )  \
                   || (" ${COMP_WORDS[*]} " == *"check --type \ [^[:space:]]+ "* )  \
                   || (" ${COMP_WORDS[*]} " == *"check --type \ [^[:space:]]+ "* ) ]];
            then
                COMPREPLY=( $(compgen -W "--script SCRIPT_NAME" -- "${cur}" -o nospace) )
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"run check --type "* )  \
                  || (" ${COMP_WORDS[*]} " == *"list checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"list failed-checks --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"show audit-trail --type "* ) \
                  || (" ${COMP_WORDS[*]} " == *"check --type "* ) \
                  ]];

            then
                COMPREPLY=( $(compgen -W "aws k8s postgres mongodb elasticsearch vault ssh keycloak redis" -o nospace) )
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " == *"run check --all "*) \
                  || (" ${COMP_WORDS[*]} " == *"check --all "* ) \
                  && (" ${COMP_WORDS[*]} " != *"run check --all --report"* ) ]];
            then
                COMPREPLY=( $(compgen -W "--script SCRIPT_NAME --report" -o nospace) )
                return 0
            fi
            if [[ (" ${COMP_WORDS[*]} " == *"run [^[:space:]]+ check "*) \
                  || (" ${COMP_WORDS[*]} " == *"run [^[:space:]]+ check "*) \
                  || (" ${COMP_WORDS[*]} " == *"check "*) ]];
            then
                COMPREPLY=( $(compgen -W "--all --type --name" -- "${cur}" -o nospace) ) 
                return 0
            fi
            

            if [[ (" ${COMP_WORDS[*]} " == *"list failed-checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"list checks --all"*) \
                  || (" ${COMP_WORDS[*]} " == *"show audit-trail --all"*) \
                  ]];
            then
                return 0
            fi


            if [[ (" ${COMP_WORDS[*]} " == *"list failed-checks "*) \
                  || (" ${COMP_WORDS[*]} " == *"list failed-checks "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"list --checks "*) \
                  || (" ${COMP_WORDS[*]} " == *"list checks "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type" -- "${cur}" -o nospace) ) 
                return 0
            fi
           
            if [[ (" ${COMP_WORDS[*]} " == *"show audit-trail --execution_id"*) \
                  && (" ${COMP_WORDS[*]} " != *"show audit-trail --execution_id EXECUTION_ID"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "EXECUTION_ID" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"show failed-logs"*) \
                  || (" ${COMP_WORDS[*]} " == *"show failed-logs "*) ]];
            then
                COMPREPLY=( $(compgen -W "--execution_id EXECUTION_ID" -- "${cur}" -o nospace) ) 
                return 0
            fi


            if [[ (" ${COMP_WORDS[*]} " == *"show audit-trail "*) \
                  || (" ${COMP_WORDS[*]} " == *"show audit-trail "*)]];
            then
                COMPREPLY=( $(compgen -W "--all --type --execution_id" -- "${cur}" -o nospace) ) 
                return 0
            fi


            if [[ (" ${COMP_WORDS[*]} " == *"run --script "*) \
                  && (" ${COMP_WORDS[*]} " != *"run --script SCRIPT_FILE"*) \
                  && (" ${COMP_WORDS[*]} " != *"run --script \ [^[:space:]]+"*) \
                  && (" ${COMP_WORDS[*]} " != *"check "*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "SCRIPT_FILE" -- "${cur}" -o nospace) ) 
                return 0
            fi


            IFS=' ' read -r -a words <<<"${COMP_WORDS[*]}"
            if [[ " ${COMP_WORDS[*]} " == *"run --script "* && " ${COMP_WORDS[*]} " != *"check "* ]]; then
                last_word="${words[${#words[@]}-1]}"
                if [[ "${last_word}" != "" && "${last_word}" =~ ^[^[:space:]]+$ ]]; then
                    COMPREPLY=( $(compgen -W "check" -- "${cur}" -o nospace) )
                else
                    COMPREPLY=( $(compgen -W "SCRIPT_FILE" -- "${cur}" -o nospace) )
                fi
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " =~ *"run --script  [^[:space:]]+"*) \
                  || (" ${COMP_WORDS[*]} " =~ *"run --script  [^[:space:]]+"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "check" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " =~ *"run --script \ [^[:space:]]+"*) \
                  || (" ${COMP_WORDS[*]} " =~ *"run --script  [^[:space:]]+"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "check" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"run --script \ [^[:space:]]+ check"*) \
                  || (" ${COMP_WORDS[*]} " == *"run --script \ [^[:space:]]+ check"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "--type --all --name" -- "${cur}" -o nospace) ) 
                return 0
            fi



            if [[ (" ${COMP_WORDS[*]} " == *"run check --all --report"*) \
                  || (" ${COMP_WORDS[*]} " == *"run check --all --report "*)]];
            then
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"debug --start"*) \
                  || (" ${COMP_WORDS[*]} " == *"debug --start "*) \
                  && (" ${COMP_WORDS[*]} " != *"debug --start --config OVPNFILE"*) \
                  ]];
            then
                COMPREPLY=( $(compgen -W "--config OVPNFILE" -- "${cur}" -o nospace) ) 
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"debug --stop"*) \
                  || (" ${COMP_WORDS[*]} " == *"debug --stop "*) \
                  ]];
            then
                return 0
            fi

            if [[  " ${COMP_WORDS[*]} " == *"--create-credential"* ]];
            then
                return 0
            fi

            if [[ (" ${COMP_WORDS[*]} " == *"run"* ) \
                && ( "${COMP_WORDS[*]} " != *"check"* ) \
                && (" ${COMP_WORDS[*]} " == *"--script \ [^[:space:]]+"* )]];
            then
                if [[ " ${COMP_WORDS[*]} " == *"check"* ]];
                then 
                    COMPREPLY=( $(compgen -W "--all --type --name" -- "${cur}" -o nospace) )
                else 
                    COMPREPLY=( $(compgen -W "check" -- "${cur}" -o nospace) )
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
