#!/bin/tcsh
foreach d (*)
	print $d
	checkTime.py $d
	end
