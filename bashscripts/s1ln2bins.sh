for i in 'Vtk' 'Pecube' 'Test'
do
for j in 'Session1A/bin/'
do
	ln -s "/home/imalkov/Documents/codeblock/bin/$i"  "/home/imalkov/Documents/$j$i"
	#echo "/home/imbgu/Documents/Pecube/srcDir/ver2/bin/$i"  
	#echo "/home/imbgu/Documents/Pecube/DTree/Session1/$j$i"
done
done
