                             #!/usr/bin/env bash

## Get the directory where this script is located
directory="$( cd "$( dirname $0)" && pwd )"
## Build the ${plugin} variable
for files in `find ${directory}/lib/ext -maxdepth 1 -type f`; do
plugins="${plugins};${files}"
done
## Build the libraries variable
for files in `find ${directory}/lib -maxdepth 1 -type f`; do
libraries="${libraries}:${files}"
done
## Remove the first ; or :
plugins=`echo ${plugins} | sed -e 's/^;//'`
libraries=`echo ${libraries} | sed -e 's/^://'`

## Build the jmeter options for plugins and libraries
search_paths=`echo "-Jsearch_paths=${plugins}"`
class_path=`echo "-Juser.classpath=${libraries}"`

## Set your JAVA location by adding it to the $PATH variable
JAVA_HOME="${directory}/java"
export PATH="${JAVA_HOME}/bin:${PATH}"
## JVM_ARGS & JMETER_OPTS etc can be placed here. Just make sure that you
## add them to the command at the end

## Start jmeter
## The "$@" will pass any arguments from the command line to the jmeter.sh script
${directory}/jmeter/bin/jmeter.sh ${search_paths} ${class_path} \
-j ${directory}/logs/jmeter.log ${any_other_variables} "$@"