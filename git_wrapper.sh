#!/bin/bash
ARGS=("$@")
for ((i=0; i<${#ARGS[@]}; i++)); do
  if [[ "${ARGS[i]}" == file:///* ]]; then
    # Convert file:///path to /path
    ARGS[i]="${ARGS[i]#file://}"
  fi
done
exec /usr/bin/git "${ARGS[@]}"
