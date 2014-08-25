#!/bin/bash

# User specific environment and startup programs

PATH=${PATH}:~/Documents/HarvardX-Tools/shellscripts:~/Documents/HarvardX-Tools/src/main/python:~/Documents/HarvardX-Tools/src/main/python/logs:~/Documents/HarvardX-Tools/src/main/python/convertfiles:~/Documents/HarvardX-Tools/src/main/python/checkData:$PATH

export PATH

#setenv DISPLAY :0
#set prompt = "$user %! >"
#setenv HXTOOLS /Users/waldo/Harvard/CTO/HarvardX/ResData/Tools
#setenv PATH $HXTOOLS/shellscripts:$HXTOOLS/src/main/python:$HXTOOLS/src/main/python/logs:$HXTOOLS/src/main/python/convertfiles:$HXTOOLS/src/main/python/checkData:/Users/waldo/Desktop/scala-2.10.1/bin:/Users/waldo/bin/java6/Commands:/usr/local/bin:/Users/waldo/maven/bin:/Users/waldo/bin:$PATH
#setenv M2_HOME /Users/waldo/maven
#setenv JAVA_HOME /System/Library/Frameworks/JavaVM.framework/Versions/1.6/Home
#setenv PYTHONPATH /System/Library/Frameworks/Python.framework/Versions/2.7/bin/:/Users/waldo/Harvard/CTO/Harvardx/ResData/Tools:/Users/waldo/Harvard/CTO/Harvardx/ResData/Tools/src/main/python

##test -r /sw/bin/init.csh && source /sw/bin/init.csh

# Setting PATH for Python 2.7
# The orginal version is saved in .cshrc.pysave
set path=(/Library/Frameworks/Python.framework/Versions/2.7/bin $path)
