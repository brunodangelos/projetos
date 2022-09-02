RESULT=$(isql $1 $2 $3 -b < /usr/lib/zabbix/externalscripts/active.sql HIVE 2>&1 | sed '4q;d' | awk {'print $2'});

if [ "$RESULT" = 1 ];
then
        echo $RESULT;
else
        echo 0;
fi