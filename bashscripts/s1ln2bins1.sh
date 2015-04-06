for i in 'Vtk' 'Pecube' 'Test'
do
for j in 'Session1A/bin/' 'Session1B/bin/'
do
	ln -s "/home/imbgu/Documents/Pecube/srcDir/ver2/bin/$i"  "/home/imbgu/Documents/Pecube/DTree/Session1/$j$i"
	#echo "/home/imbgu/Documents/Pecube/srcDir/ver2/bin/$i"  
	#echo "/home/imbgu/Documents/Pecube/DTree/Session1/$j$i"
done
done
