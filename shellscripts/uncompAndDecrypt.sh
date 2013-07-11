#!/bin/tcsh

foreach f (*.gpg)
    echo $f
    gpg -o $f:r -d $f
    rm $f
end
