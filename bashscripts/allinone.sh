#!\bin\bash
find -name *.png | xargs cp -r --backup=t --target-directory=../pics/

find -L -name fault_parameters.txt -exec cp '{}' --backup=t --target-directory=/home/imalkov/Documents/fault_fdupes/ \;
find -L -name fault_parameters.txt -exec ln -s '{}' --backup=t --target-directory=/home/imalkov/Documents/fault_fdupes/ \;
for i in `seq 10 15`; do  cp -rp ./TOPO_TYPES1/ ./TOPO_TYPES$i; done

gcc -Wall -W -ansi -pedantic test.c -o test

for i in 'Vtk' 'Pecube' 'Test'
do
	ln -s "/home/imalkov/Documents/PECUBE/WDIR/FIVE_TASKS_ENV/FLUV_SINGLE_INPUT_ENV/src/pec_src_1b_nohprod/bin/$i"  $i
done

ipython notebook --pylab=inline --notebook-dir='/home/imalkov/Dropbox/M.s/Research/NbWorkspace'

for i in `seq 1 15`;
do
	fdupes  /home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDFAULTS/TOPO_TYPES$i/fault_files/ >> /home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDFAULTS/cmp.txt
done

for i in `seq 1 15`;
do
	find -L /home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDTOPO/TOPO_TYPE$i -name fault_parameters.txt -exec ln -s '{}' --backup=t --target-directory=/home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDFAULTS/TOPO_TYPES$i/fault_files_mapping/ \;
done