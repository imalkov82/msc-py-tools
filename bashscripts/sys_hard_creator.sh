for i in `seq 1 15`;
do 
	find -L /home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDTOPO/TOPO_TYPE$i -name fault_parameters.txt -exec cp '{}' --backup=t --target-directory=/home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDFAULTS/TOPO_TYPES$i/fault_files/ \; 
done

for i in `seq 1 15`;
do 
	find -L /home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDTOPO/TOPO_TYPE$i -name fault_parameters.txt -exec ln -s '{}' --backup=t --target-directory=/home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDFAULTS/TOPO_TYPES$i/fault_files_mapping/ \;
done
