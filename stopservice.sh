#!/bin/bash

function get_pid(){
	script_name=$1
	script_folder=$2
	pid=`ps -ef | grep $script_name | grep $script_folder | head -n 1 | awk '{printf $2}'`
	echo "$pid"
}

function kill_process(){
	script_name=$1
	script_folder=$2
	process_id=`get_pid $script_name $script_folder`
	kill -9 $process_id
}

`kill_process manage.py core_pdf_page`
`kill_process test.py core_pdf_page`