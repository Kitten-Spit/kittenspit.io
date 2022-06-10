#!/bin/bash

# Flask setup:

echo "Setup Flask:"

# Defaults
SECRET_KEY=`cat /dev/urandom | head -c 24 | base64`
FLASK_PORT_DEFAULT=8080
FLASK_DIRECTORY_DEFAULT="$(pwd)/app/"
FLASK_DOMAIN_DEFAULT="0.0.0.0"
FRONTEND_DOMAIN_DEFAULT=${FLASK_DOMAIN_DEFAULT}":"${FLASK_PORT_DEFAULT}"/"
MEDIA_DIR_DEFAULT="$(pwd)/pub/"
DIST_NOW_DEFAULT='YES'

read -p "Flask Directory [$FLASK_DIRECTORY_DEFAULT]: " FLASK_DIRECTORY
FLASK_DIRECTORY=${FLASK_DIRECTORY:-$FLASK_DIRECTORY_DEFAULT}
echo

read -p "Flask App Port [$FLASK_PORT_DEFAULT]: " FLASK_PORT
FLASK_PORT=${FLASK_PORT:-$FLASK_PORT_DEFAULT}
echo

read -p "Flask Domain: Server [$FLASK_DOMAIN_DEFAULT]: " FLASK_DOMAIN
FLASK_DOMAIN=${FLASK_DOMAIN:-$FLASK_DOMAIN_DEFAULT}
echo

read -p "Flask Domain: Client [$FRONTEND_DOMAIN_DEFAULT]: " FRONTEND_DOMAIN
FRONTEND_DOMAIN=${FRONTEND_DOMAIN:-$FRONTEND_DOMAIN_DEFAULT}
echo

read -p "Media Directory: [$MEDIA_DIR_DEFAULT]: " MEDIA_DIR
MEDIA_DIR=${MEDIA_DIR:-$MEDIA_DIR_DEFAULT}
echo

wait

# Rename config.cfg.sample to config.cfg
CONFIG_EXAMPLE_FILE=./app/main/config/config.cfg.sample
CONFIG_FILE="./app/main/config/config.cfg"
cp -R $CONFIG_EXAMPLE_FILE $CONFIG_FILE

if [[ "$OSTYPE" == "darwin"* ]] ; then

  # Save configuration values to config.cfg
  # use GNU sed utility if on Mac, e.g.
  # `brew install gsed`
  echo "detected fruit based operating system, checking gnu-sed..."

if ![ whichapp 'gsed' &>/dev/null ]; then
    echo "Please use GNU sed utility if on Mac, e.g."
    echo -e "\` brew install gsed \`"
    echo "exiting..."
    exit 0
fi

  gsed -i "s~##SECRET_KEY##~$SECRET_KEY~g" $CONFIG_FILE
  gsed -i "s~##FLASK_PORT##~$FLASK_PORT~g" $CONFIG_FILE
  gsed -i "s~##FLASK_DIRECTORY##~$FLASK_DIRECTORY~g" $CONFIG_FILE
  gsed -i "s~##FLASK_DOMAIN##~$FLASK_DOMAIN~g" $CONFIG_FILE
  gsed -i "s~##FRONTEND_DOMAIN##~$FRONTEND_DOMAIN~g" $CONFIG_FILE

else

  sed -i "s~##SECRET_KEY##~$SECRET_KEY~g" $CONFIG_FILE
  sed -i "s~##FLASK_PORT##~$FLASK_PORT~g" $CONFIG_FILE
  sed -i "s~##FLASK_DOMAIN##~$FLASK_DOMAIN~g" $CONFIG_FILE
  sed -i "s~##FLASK_DOMAIN##~$FLASK_DOMAIN~g" $CONFIG_FILE
  sed -i "s~##FRONTEND_DOMAIN##~$FRONTEND_DOMAIN~g" $CONFIG_FILE

fi

echo "Config saved!"

read -p "Build dev now? [$DIST_NOW_DEFAULT]: " DIST_NOW
DIST_NOW=${DIST_NOW:-$DIST_NOW_DEFAULT}
echo

if [ $DIST_NOW  == 'YES' ]; then

  npm run-script dev-soft-ui
  wait

  npm run-script dev-payments
  wait

fi

exit 0
