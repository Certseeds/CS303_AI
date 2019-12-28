file_folder=$1
file_inside=$2
echo ${file_folder}
echo ${file_inside}
for x in `ls ${file_folder}*.JPEG`
do
  echo $2 > ${x%*.JPEG}.txt
done