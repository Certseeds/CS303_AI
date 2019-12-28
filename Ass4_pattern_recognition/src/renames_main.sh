start=$(date "+%s")
dir=./
declare -A map=()
while read line
do
  #echo $line
  #echo ${line:0:9}
  #echo ${line##*${line:0:9}}
  map[${line:0:9}]=${line##*${line:0:9}}
done < data_names.txt


for key in ${!map[@]}
do  
    echo ${key}
    echo ${map[$key]}
    file_folder=${dir}${key}/
    ./rename_son.sh ${file_folder} ${map[$key]}
done

now=$(date "+%s")
time=$((now-start))
echo "time used:$time seconds"
exit 1;

# for x in `ls *.tar`
# do
#   echo "begin"
#   filename=${x%*.tar}
#   echo ${filename}
#   file_folder=${dir}${filename}
#   ./rename_son.sh ${file_folder}
#   echo "end"
# done
