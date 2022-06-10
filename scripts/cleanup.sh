#!/bin/bash

echo -e 'cleaning up...'

echo -e '\n cleaning transpiled ts ... \n'
rm -rf ./pub/static/assets/js/payments.js
rm -rf ./pub/static/assets/js/soft-design-system.js


echo -e '\n cleaning node_modules/ ... \n'
rm -rf node-modules/

echo -e '\n cleaning venv ... \n'
rm -rf dla_venv

echo -e '\n ...cleanup done! \n'