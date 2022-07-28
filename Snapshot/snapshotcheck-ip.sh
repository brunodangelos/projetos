#!/bin/bash
##----------------------------------------------------------------------------##
## Zabbix check script for esx to check existence of snapshots, consolidation ##
## required and to which VMs the status is applied. Outputs two files which   ##
## are read by zabbix agent to monitor status.                                ##
##                                                                            ##
## Requirements:                                                              ##
##  * /root/.ssh/id_rsa SSH key to permit passwordless login to ESXi          ##
##  * Corresponding public key added to /etc/ssh/keys-root/authorized_keys    ##
##  * snapshot_check.sh to exist              ##
##  * Cron job to exist in /etc/crontab An example of the cron job would be:  ##
##  snapshot_check.sh esx.your.tld 0 1 2>&1   ##
##  * Zabbix 2.2+                                                             ##
##                                                                            ##
## Script tested on vmware esx/esxi: 3.5/4.0/4.1/5.5/6.0/6.5                  ##
##                                                                            ##
## on early version you have to create an alias for vim-cmd                   ##
## #cd /usr/bin                                                               ##
## #ln -s ./vmware-vim-cmd vim-cmd                                            ##
##                                                                            ##
##----------------------------------------------------------------------------##
## Check to see if the snapshot-status file exists
if [ -f "snapshot-status" ]; then
  ## Delete file if it does exist, to make sure we don't get wonky output
  rm -rf snapshot-status
fi

## check if consolidate-status file exists
if [ -f "consolidation-status" ]; then
  ## Delete file if it does exist, to make sure we don't get wonky output
  rm -rf consolidation-status
fi
## Reset variables
((i=0));
((snaptotal=0));
((snapshotnum=0));
vms=$(vim-cmd vmsvc/getallvms | sed -e '1d' -e 's/ \[.*$//' | awk '$1 ~ /^[0-9]+$/ {print  $1":"substr($0,8,80)}'|sort | grep -i -v replica);
for vm in "${vms[@]}"; 
do
  id=$(echo $vm |awk -F: '{print $1}')
  vmname=$(echo $vm |awk -F: '{print $2}')
  snapshotnum=$(vim-cmd vmsvc/snapshot.get $id |grep "Snapshot Name" |wc -l)
  snap[$i]="$vmname:$snapshotnum";
  snaptotal=$snaptotal+$snapshotnum;
  i++;
done
if [ "$snaptotal" -lt "0" ]; then
  echo "0 snapshots found" > snapshot-status
  exit 
else
  echo "$snaptotal snapshots found on " "${snap[@]}"
  exit 0
fi
exit 0

