#!/bin/sh

OUTFILE="/tmp/cellular"

operator_name=NULL
operator_name=$(mmcli -m 0 | awk '/operator name/ {print $4}')

signal_strength=NULL
signal_strength=$(mmcli -m 0 | awk '/signal quality/ {print $4}')

state=NULL
state=$(mmcli -m 0 | awk '/  state/ {print $3}')

pstate=NULL
pstate=$(mmcli -m 0 | awk '/power state/ {print $4}')


tech=NULL
tech=$(mmcli -m 0 | awk '/access tech/ {print $4}')

imei=NULL
imei=$(mmcli -m 0 | awk '/imei/ {print $4}')

op_id=NULL
op_id=$(mmcli -m 0 | awk '/operator id/ {print $4}')

reg=NULL
reg=$(mmcli -m 0 | awk '/registration/ {print $3}')



# writing json file

echo "{
	\"operator\":\"$operator_name\",
	\"strength\":\"$signal_strength\",
	\"state\":\"$state\",
	\"pow\":\"$pstate\",
	\"reg\":\"$reg\",
	\"tech\":\"$tech\",
	\"op_id\":\"$op_id\",
	\"imei\":\"$imei\",
	\"apn\":\"data.apn.name\"
}" > $OUTFILE
