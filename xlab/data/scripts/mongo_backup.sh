#!/bin/bash

# mongo_backup - Script for creating and restoring mongo backup.
# Mainly to be used with cron.

if [[ -z "${1}" ]]; then
  echo "Please specify a command: create, list, clean, or restore"
  exit
fi

date=$(date '+%Y-%m-%d')
DATA_DUMP_ROOT_DIR="/Users/$(whoami)/mongodump/xlab"

if [[ ! -d "${DATA_DUMP_ROOT_DIR}" ]]; then
  echo "Trying to make ${DATA_DUMP_ROOT_DIR}"
  mkdir -p "${DATA_DUMP_ROOT_DIR}"
fi

case "${1}" in
create)
  echo "Creating a backup to ${DATA_DUMP_ROOT_DIR}/${date}"
  mongodump --db=xlab --gzip --out="${DATA_DUMP_ROOT_DIR}/${date}"
  ;;
list)
  ls "${DATA_DUMP_ROOT_DIR}"
  ;;
clean)
  echo "Deleting backups older than 7 days"
  find ${DATA_DUMP_ROOT_DIR} -mtime +7 -delete
  ;;
restore)
  if [[ -z "${2}" ]]; then
    echo "Please specify the which backup directory to use."
    echo "Use 'list' command to see the backups available."
  fi
  echo "Restoring DB to the most recently backup"
  mongorestore "${DATA_DUMP_ROOT_DIR}/${2}" --drop --gzip
  ;;
*)
  echo "${1} is not a supported command"
  ;;
esac
