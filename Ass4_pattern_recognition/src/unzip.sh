dir=./
for x in `ls *.tar`
do
  echo ${x%*.tar}
  filename=`basename ${x%*.tar}`
  echo ${filename}
  mkdir ${filename}
  tar -xvf ${x} -C ./${filename}
done