
### setup:
```
## node:
npm install

## venv:
python3 -m venv ks_venv
source ks_venv/bin/activate
pip3 install -r requirements.txt

## setup:
npm run-script setup-app  # interactive setup and build

## serve:
npm run-script serve-app  # interactive choose and launch WSGI (Waitress or Werkzeug)

## visit locally at:
# 127.0.0.1:8080

## cleanup:
npm run-script clean
```
