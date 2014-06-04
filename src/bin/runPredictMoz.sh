#!/bin/bash

appRoot='/home/xiejl/OSS/bin/triager'
model=$appRoot'/data/mozilla/moz_model'

buginfo=`$appRoot/bin/application/extractInfoByBugID.py $appRoot/data/mozilla/linfo_level2.tmp $appRoot/data/mozilla/lactivity_level2.tmp $1`

buginfo=($buginfo)
if [ ${buginfo[0]} = "False" ]; then
	echo "Error,${buginfo[3]}"
	exit 1
fi

metrics=`$appRoot/bin/application/queryMetrics.py $appRoot/data/mozilla/product_information_assi $appRoot/data/mozilla/login_product_information_assi $appRoot/data/mozilla/login_peer_info $appRoot/data/mozilla/login_ncomment ${buginfo[1]} ${buginfo[2]} ${buginfo[3]}`

pro=`R --slave <<EOF
source("$appRoot/bin/rscript/predictAssi.r")
#predict_from_file("$2", "$1")
predict_from_input("$model", $metrics, "${buginfo[3]}")
#EOF`

pro=($pro)
pro=${pro[1]}

threshold=`cat $appRoot/data/mozilla/predictThreshold`
threshold=($threshold)
minThr=${threshold[1]}
maxThr=${threshold[0]}

echo "${buginfo[1]},${buginfo[2]},${buginfo[3]},$metrics,$pro,$minThr,$maxThr"
