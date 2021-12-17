#!/bin/sh

for file in Input/*.png
do
	new_file=$(echo "$file" | sed -e 's/Input/Output/g')
	echo "$file"
	echo "$new_file"
	convert "$file" -fuzz 10% -trim +repage "$new_file"

done

