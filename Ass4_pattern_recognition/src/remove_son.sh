file_folder=$1
aim_folder=$2
echo ${file_folder}
echo ${aim_folder}
if [ -d "${file_folder}" ] 
then
  for x in `ls ${file_folder}`
  do
    if [ -f "${file_folder}${x}" ] 
    then
    echo "${file_folder}${x}"
    cp ${file_folder}${x} ${aim_folder}
    fi
  done
else 
  exit 2;
fi

