#!/bin/tcsh
# shell script to move all of the raw logs from a staging
# area to the collection area, for example, from the weekly
# dump of the logs of the prod* servers to the AllLogs directory.
# This should be run from the parent directory above the Harvard,
# HarvardX, HSPH, etc. directories, and will move all of the 
# daily logs to a directory that contains a similar directory
# structure. For example, run in a harvardx-2013-MM-DD directory
# with the command line
# moveRawLogs.sh ../AllLogs

foreach h (H*)
    cd $h
    foreach d (prod*)
        cd $d
	foreach f (20*)
	    mv $f $1/$h/$d/$f
	end
	cd ..
    end
    cd ..
end 
