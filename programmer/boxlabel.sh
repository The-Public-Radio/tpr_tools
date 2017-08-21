#!/bin/bash

# create text image
convert -density 300 -pointsize 12 -font \
/usr/share/fonts/truetype/msttcorefonts/Courier_New_Bold.ttf \
-size 637.5x1200 -gravity North \
label:'\n\nYour Public Radio\nis tuned to\n'"$1"' MHz\n\n\nEnjoy :)\n\n\n--------------------' \
~/TPR_ops/temp/text.png

# create QR code for serial number
qrencode -o ~/TPR_ops/temp/sn.png "$2"

# resize QR code
convert -resize 300% ~/TPR_ops/temp/sn.png ~/TPR_ops/temp/sn.png

# merge two images into one
convert ~/TPR_ops/temp/text.png ~/TPR_ops/temp/sn.png -gravity center -geometry +0+300 -composite ~/TPR_ops/temp/label.png

# print the result
lpr ~/TPR_ops/temp/label.png

# delete all the temp files
rm ~/TPR_ops/temp/*
