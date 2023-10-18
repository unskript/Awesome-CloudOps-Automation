#!/bin/bash


_unskript-client-completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    connector_list=("aws" "k8s" "postgres" "mongodb" "elasticsearch" "vault" "ssh" "keycloak" "github" "redis")


    # Find the absolute path of unskript-client.py
    local unskript_client_script
    unskript_client_script="$(which unskript-client.py)"

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
    opts="--list-runbooks --run-runbook --run-checks --display-failed-checks --list-checks --show-audit-trail --display-failed-logs --create-credentials --credential-list --start-debug --stop-debug" 

    # Completion logic
    case "${prev}" in
        -rr|--run-runbook)
            # Provide completion suggestions for runbook filenames
            COMPREPLY=( $(compgen -f -- "${cur}" -o nospace) )
            return 0
            ;;

        -rc|--run-checks)
            case ${prev} in
                -rc|--run-checks)
                    case ${cur} in 
                        --check)
                            cur=${cur#--check}
                            opt2="$(cat /tmp/checknames.txt)"
                            COMPREPLY=( $(compgen -W "${opt2}" -o nospace) )
                            ;;
                        *)
                            #COMPREPLY=( $(compgen -W "--all  --type  --failed  --check" -- "${cur}" -o nospace) )
                            COMPREPLY=( $(compgen -W "--all  --type  --failed  --check" -o nospace) )
                            ;;
                    esac
                    return 0
                    ;;
                *)
                    COMPREPLY=( $(compgen -W "${opts}" "${cur}" -o nospace) )
                    ;;

            esac
            return 0
            ;;

        -lc|--list-checks)
            # Provide completion suggestions for list-checks options
            COMPREPLY=( $(compgen -W "--all   --type" -- "${cur}" -o nospace) )
            return 0
            ;;

        -sa|--show-audit-trail)
            # Provide completion suggestions for show-audit-trail options
            COMPREPLY=( $(compgen -W "--all   --type   --execution_id" -- "${cur}" -o nospace) )
            return 0
            ;;

        -dl|--display-failed-logs)
            # Provide completion suggestions for display-failed-logs options
            COMPREPLY=( $(compgen -W "--execution_id" -- "${cur}" -o nospace) )
            return 0
            ;;

        -cc|--create-credentials)
            # Provide completion suggestions for create-credentials options
            COMPREPLY=( $(compgen -W "--type" -- "${cur}" -o nospace) )
            return 0
            ;;

        *)  # Default: Provide completion suggestions for global options
            _cmd="${COMP_WORDS[COMP_CWORD-2]}"
            if [ "${prev}" = "--check" ];
            then
                cur=${cur#--check}
                opt2="$(grep -F ${cur} /tmp/checknames.txt)"
                COMPREPLY=( $(compgen -W "${opt2}" -o nospace) )
                compopt -o nospace
            elif [ "${_cmd}" = "--check" ];
            then 
                COMPREPLY=( $(compgen -W "--report" -o nospace) )
            elif [ "${cur}" = "--report" ];
            then
                COMPREPLY=()
            elif [[ "${_cmd}" = '-cc' || "${_cmd}" = '--create-credentials' ]];
            then
                COMPREPLY+=("-k8s <KUBECONFIG_FILE_PATH>")
            elif [[ "${_cmd}" = '-rc' || "${_cmd}" = '--run-checks' || "${_cmd}" = '--list-checks' || "${_cmd}" = '-lc' ]];
            then
                if [ "${prev}" = "--type" ];
                then
                    COMPREPLY=( $(compgen -W "aws k8s postgres mongodb elasticsearch vault ssh keycloak github redis" -o nospace) )
                elif [[ "${prev}" = "--all" || "${prev}" = "--failed" ]];
                then
                    COMPREPLY+=('--report')
                fi
            elif [[ "${_cmd}" = "--type" && "${COMP_WORDS[COMP_CWORD-3]}" = '-rc' || "${COMP_WORDS[COMP_CWORD-3]}" = '--run-checks' ]];
            then 
                for item in "${connector_list[@]}";
                do
                    if [ "$item" == "${prev}" ];
                    then
                        COMPREPLY+=("--report")
                        break
                    fi
                done 
            elif [[ "${_cmd}" = '-sa' || "${_cmd}" = '--show-audit-trail' ]];
            then
                if [ "${prev}" = '--type' ];
                then
                    COMPREPLY=( $(compgen -W "aws k8s postgres mongodb elasticsearch vault ssh keycloak github redis" -o nospace) )
                elif [ "${prev}" = '--execution_id' ];
                then
                    COMPREPLY=( $(compgen -W "<EXECUTION_ID>" -o nospace) )
                fi
            else
                if [ "${#COMP_WORDS[@]}" != "2" ]; 
                then
                    return 0
                fi
                COMPREPLY=( $(compgen -W "${opts}" -- "${cur}" -o nospace) )
            fi

        return 0
        ;;
    esac
}

# Register the completion function for unskript-client.py
complete -F _unskript-client-completion unskript-ctl.sh