#!/bin/bash
echo "line 2"
echo "line 4"
int0=0
int1=1
while ((${int0} <=30))
do
    while(( $int1<=30 ))
    do
        echo $int1
        let "int1++"
        python3 produce_json.py ${int1}
        cat parameter.json
        python3 -m algorithm_ncs.ncs_client -d ${1} -c parameter.json 
    done
    let "int0++"
    let "int1=1"
    python3 produce_data_by_data.py ${1}
done