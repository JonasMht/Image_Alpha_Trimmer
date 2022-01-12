#!/bin/bash

usage() {
cat << EOF
Usage: manipulate.sh -t -r <percentage>
-t : trims the alpha of the image
-r : resizes the image by percentage (number) using adaptive-resize
EOF
exit 1
}


resize=false;
trim=false;


if [ $# -gt 3 ] || [ $# -lt 1 ]; then
	usage;
fi

while getopts "tr:" flag # x: flag with optional arg, x
do
    case "${flag}" in
    	t){
        	trim=true;
        };;
        r){
        	resize=true;
        	percentage=${OPTARG};
        	# Check if is number
        	re='^[-+]?[0-9]+\.?[0-9]*$'
		if ! [[ $percentage =~ $re ]]; then
			usage;
		fi
		
        };;
        \?){
		echo "Invalid option: -$OPTARG" >&2;
		exit 1;
	};;
	:){
		echo "Option -$OPTARG requires an argument." >&2;
		exit 1;
	};;
    esac
done

echo "Percentage: $percentage%";
echo "Resize?: $resize";
echo "Trim?: $trim";

for file in Input/*.png
do
	new_file=$(echo "$file" | sed -e 's/Input/Output/g')
	echo "$file"
	echo "$new_file"
	
	tmpfile=$(mktemp /tmp/abc-script.XXXXXX)
	cp -fr "$file" "$tmpfile"
	
	if $resize; then
		convert "$tmpfile" -adaptive-resize "$percentage%" "$tmpfile"
	fi
	if $trim; then
		convert "$tmpfile" -fuzz 10% -trim +repage "$tmpfile"
	fi
	
	cp "$tmpfile" "$new_file"
	
	rm "$tmpfile"
done

