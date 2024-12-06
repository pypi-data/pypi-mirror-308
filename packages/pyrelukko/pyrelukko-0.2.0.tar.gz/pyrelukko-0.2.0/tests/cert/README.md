# How To
```
openssl req -x509 -sha256 -days 7300 -noenc -newkey rsa:2048 -keyout rootCA.key -out rootCA.crt
ln -s rootCA.crt "$(openssl x509 -hash -noout -in rootCA.crt)"
openssl req -newkey rsa:2048 -noenc -keyout relukko.key -out relukko.csr
openssl x509 -req -CA rootCA.crt -CAkey rootCA.key -in relukko.csr -out relukko.crt -days 7299 -CAcreateserial
openssl x509 -inform PEM -in rootCA.crt  -outform DER -out rootCA.der
```
