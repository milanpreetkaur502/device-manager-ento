#!/bin/bash


CONF_FILE="/etc/entomologist/ento.conf"
OUTFILE="/tmp/job"

job_status=inactive

# job data read function
job_data () {

	#conf_data=$(cat $CONF_FILE)
	#echo $conf_data | jq '.'
	job_id=$(jq '.device.JOB_ID' /etc/entomologist/ento.conf)
	on_time=$(jq '.device.ON_TIME' /etc/entomologist/ento.conf)
	off_time=$(jq '.device.OFF_TIME' /etc/entomologist/ento.conf)
	serial_id=$(jq '.device.SERIAL_ID' /etc/entomologist/ento.conf)
}


# rana service status check
rana_service () {
	rana_status="$(systemctl is-active rana)"
	cam_status="$(systemctl is-active cam)"
	
	if [[ $rana_status = active ]] || [[ $cam_status = active ]];
	then
		job_status=active
	fi 

}

#while [ true ]
#do
	job_data
	rana_service

	echo  "{
		\"job_status\":\"$job_status\",
		\"on_time\":$on_time,
		\"off_time\":$off_time,
		\"job_id\":\"$job_id\",
		\"device_id\":$serial_id
}" > $OUTFILE
#sleep 60
#done	




