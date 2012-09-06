#!/bin/sh

for l in libavahi-client libfreeipmi libusb libnetsnmp libneon
do
  rp=""
  for p in /usr/lib64 /lib64 /usr/lib /lib
  do
    if [ -f ${p}/${l}.so ]
    then
      fn=$( readlink ${p}/${l}.so )
      mfn=${fn%.so.*}.so
      sfn=${fn##*.so.}
      tfn=$mfn
      while [ $tfn = ${l}.so ] || [ ! -f ${p}/${tfn} -a -n "$sfn" ]
      do
        tfn=${tfn}.${sfn%%.*}
        sfn=${sfn#*.}
      done
      if [ -f ${p}/${tfn} ]
      then
        rp=${tfn}
      else
        rp=${fn}
      fi
      break
    fi
  done
  echo "#define $( echo "$l" | tr '[a-z]-' '[A-Z]_')_PATH \"$rp\""
done

VINFO=$(sed -e '/version-info/!d' -e 's/#.*$//' -e 's/^.*-version-info//' -e 's/[[:space:]]//g' clients/Makefile)
echo "#define LIBUPSCLIENT_PATH \"libupsclient.so.$(( ${VINFO%%:*}-${VINFO##*:} ))\""
