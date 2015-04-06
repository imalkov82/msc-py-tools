#!\bin\bash
find -name *.png | xargs cp -r --backup=t --target-directory=../pics/

find -L -name fault_parameters.txt -exec cp '{}' --backup=t --target-directory=/home/imalkov/Documents/fault_fdupes/ \;
find -L -name fault_parameters.txt -exec ln -s '{}' --backup=t --target-directory=/home/imalkov/Documents/fault_fdupes/ \;
for i in `seq 10 15`; do  cp -rp ./TOPO_TYPES1/ ./TOPO_TYPES$i; done

gcc -Wall -W -ansi -pedantic test.c -o test

fdupes ... (something??)
