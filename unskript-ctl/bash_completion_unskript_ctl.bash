#!/bin/bash


_unskript-client-completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"


    # Find the absolute path of unskript-client.py
    local unskript_client_script
    unskript_client_script="$(which unskript-client.py)"

    if [ -n "$unskript_client_script" ]; then
        # Check if the script exists and save check names
        /usr/bin/env python "$unskript_client_script" --save-check-names /tmp/checknames.txt
        /usr/bin/env python "$unskript_client_script" -h > /tmp/allopts.txt
        if [ -f "/tmp/checknames.txt" ]; then
            opt2="$(cat /tmp/checknames.txt)"
        fi
    fi
    # Define options with each option on a separate line using newline characters
    opts="--list-runbooks --run-runbook --run-checks --display-failed-checks --list-checks --show-audit-trail --display-failed-logs --create-credentials --credential-list --start-debug --stop-debug" 

    # Completion logic
    case "${prev}" in
        -rr|--run-runbook)
            # Provide completion suggestions for runbook filenames
            COMPREPLY=( $(compgen -f -- "${cur}") )
            return 0
            ;;

        -rc|--run-checks)
            case ${prev} in
                -rc|--run-checks)
                    case ${cur} in 
                        -f)
                            COMPREPLY=( ${opt2} )
                            ;;
                        *)
                            COMPREPLY=( $(compgen -W "--all | --type | --failed | --check" -- "${cur}") )
                            ;;
                    esac
                    return 0
                    ;;
                *)
                    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
                    ;;
            esac
            return 0
            ;;

        -lc|--list-checks)
            # Provide completion suggestions for list-checks options
            COMPREPLY=( $(compgen -W "--all |  --type" -- "${cur}") )
            return 0
            ;;

        -sa|--show-audit-trail)
            # Provide completion suggestions for show-audit-trail options
            COMPREPLY=( $(compgen -W "--all |  --type |  --execution_id" -- "${cur}") )
            return 0
            ;;

        -dl|--display-failed-logs)
            # Provide completion suggestions for display-failed-logs options
            COMPREPLY=( $(compgen -W "--execution_id <EXECUTION_ID>" -- "${cur}") )
            return 0
            ;;

        -cc|--create-credentials)
            # Provide completion suggestions for create-credentials options
            COMPREPLY=( $(compgen -W "--type creds_file_path" -- "${cur}") )
            return 0
            ;;

        *)  # Default: Provide completion suggestions for global options
            COMPREPLY=( $(compgen -W "${opts}" -- "${cur}" -o nospace) )
            return 0
            ;;
    esac
}

# Register the completion function for unskript-client.py
complete -F _unskript-client-completion unskript-ctl.sh
