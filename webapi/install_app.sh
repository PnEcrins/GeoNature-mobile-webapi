
if [ ! -d 'log' ]
  then
      mkdir log
fi

APP_DIR=$(readlink -e "${0%/*}")
echo $APP_DIR
echo $PWD
sudo -s cp  webapi-service.conf /etc/supervisor/conf.d/
sudo -s sed -i "s%APP_PATH%${PWD}%" /etc/supervisor/conf.d/webapi-service.conf

sudo -s supervisorctl reread
sudo -s supervisorctl reload