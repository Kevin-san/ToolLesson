#!/bin/bash

config=$1

source $config

if [[ $METHOD_NAME="search_keys_included_file_from_git" ]]
then
	$(search_keys_included_file_from_git )
	
	
	
fi

function search_keys(){
	key_line=$1
	search_dir=$2
	output_file=$3
	key_dir=$4
	for file in `ls $search_dir`
	do
		if [[ $file == $key_dir ]]
		then
			continue
		fi
		if [[ ! -d ${search_dir}$file ]]
		then
			if grep -qi $key_line ${search_dir}$file
			then
				echo "	${search_dir}$file" >> $output_file
			else
				continue
			fi
		else
			continue
		fi
	done
}

function get_directories_from_home_recur(){
	artifact_home=$1
	directory_file=$2
	echo "${artifact_home}" >> $directory_file
	for file in `ls -d ${artifact_home}*/`
	do
		$(get_directories_from_home_recur ${file} $directory_file)
	done
}

function get_key_from_key_dir(){
	key_dir=$1
	key_suffix=$2
	key_file=$3
	for key_line in `ls $key_dir`
	do
		key=`basename $key_line .$key_suffix`
		echo $key >> $key_file
	done
}

function search_keys_included_file_from_git(){
	if [ $ISREMOVE == 1 ]
	then
		echo "" > $KEYFILE
		echo "" > $OUTPUTFILE
		$(get_key_from_key_dir $KEYDIRECTORY $SUFFIX $KEYFILE)
	fi
	echo "" > $DIRECTORYFILE
	$(get_directories_from_home_recur $ARTIFACTHOME $DIRECTORYFILE)
	for key in `cat $KEYFILE`
	do
		echo $key >> $OUTPUTFILE
		for dir in `cat $DIRECTORYFILE`
		do
			if [[ $KEYDIRECTORY != $dir ]]
			then
				$(search_keys $key $dir $OUTPUTFILE $KEYDIRECTORY)
			fi
		done
	done
}

function exclude_values(){
	for line in `cat $SP_LIST`
	do
		count=0
		for inLine in `cat $INCLUDEFILE`
		do
			if [[ $inLine == $line ]]
			then
				count=$(( $count +1 ))
			fi
		done
		if [[ "$count" == "0" ]]
		then
			echo "$line" >> $EXCLUDEFILE
		fi
	done
}

function extract_table_ddl_from_schema_sql(){
	filename=`basename $SCHEMA_SQL .sql`
	schema=$(echo "${filename/\_DDL/}")
	schema_dir=$(echo "${filename/\_//}")
	mkdir -p $OUTPUT_HOME/$schema_dir
	new_tab_sql=""
	IFS=$'\n'
	for line in `cat $SCHEMA_SQL`
	do
		table="${line#*DROP TABLE }"
		echo "$table"
		if [[ $line != $table ]]
		then
			new_tab_sql=$OUTPUT_HOME/$schema_dir/$table.sql
			echo "" > $new_tab_sql
			echo "USE $schema" >> $new_tab_sql
			echo "GO" >> $new_tab_sql
			echo "IF EXISTS(SELECT name FROM sysobjects WHERE name = '$table' AND type = 'U')" >> $new_tab_sql
			echo "	DROP TABLE $table" >> $new_tab_sql
			echo "GO" >> $new_tab_sql
		else
			if [[ $new_tab_sql != "" ]]
			then
				if [[ $line =~ \(\)$ || $line =~ GO$ ]]
				then
					echo "" >> $new_tab_sql
				else
					echo "$line" >> $new_tab_sql
					echo "GO" >> $new_tab_sql
				fi
			fi
		fi
	done
}

function extract_stored_procedure_from_schema_sql(){
	rm $SP_LIST
	filename=`basename $SCHEMA_SQL .sql`
	schema=$(echo "${filename/\_SP/}")
	schema_dir=$(echo "${filename/\_//}")
	mkdir -p $OUTPUT_HOME/$schema_dir
	new_sp_sql=""
	sp_name=""
	IFS=$'\n'
	for line in `cat $SCHEMA_SQL | sed "{s/^\/$//g;s/^\*\*$//g;s/^\/\**\*\/$//g;s/^\/\**$/\ \/\*/g;s/^\**\/$/\ \*\//g;s/^\**$//g}"`
	do
		sp="${line#DROP PROCEDURE }"
		if [[ "$line" != "$sp" ]]
		then
			sp="${sp#schema.dbo.}"
			sp_name=$sp
			echo "$sp" >> $SP_LIST
			new_sp_sql=$OUTPUT_HOME/$schema_dir/$sp.sp
			echo ""> $new_sp_sql
			echo "USE $schema" >> $new_sp_sql
			echo "GO" >> $new_sp_sql
			echo "IF EXISTS(SELECT name FROM sysobjects WHERE name='$sp' AND type ='P')" >> $new_sp_sql
			echo "	DROP PROCEDURE $sp" >> $new_sp_sql
		else
			if [[ $new_sp_sql != "" ]]
			then
				line="${line// dbo./ }"
				if [[ $line =~ ^EXEC ]]
				then
					echo "GRANT EXEC ON $sp_name to $PERMISSION" >> $new_sp_sql
				else
					echo "$line" >> $new_sp_sql
				fi
			fi
		fi
	done
}

