# /bin/sh
oldcksum=`cksum /etc/nginx/nginx.conf`

inotifywait -e modify,move,create,delete -m --timefmt '%d/%m/%y %H:%M' --format '%T' \
/etc/nginx/nginx.conf | while read date time; do

	newcksum=`cksum /etc/nginx/nginx.conf`
	if [ "$newcksum" != "$oldcksum" ]; then
		echo "At ${time} on ${date}, config file update detected."
		oldcksum=$newcksum
		nginx -s reload
	fi

done