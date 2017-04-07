#!/bin/bash
### register
curl -k -i -X POST -H "Content-Type: application/json" -d '{"username":"demo","password":"demo"}' https://api.fusionworks.cn/api/users

### get resource
#curl -u demo:123456 -i -X GET http://127.0.0.1:5000/api/resource

### get token
#curl -u demo:123456 -i -X GET http://127.0.0.1:5000/api/token

### use token
#curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MDAwMDc4NSwiaWF0IjoxNDkwMDAwMTg1fQ.eyJpZCI6Mn0.oUqfkdGBoQ6mENNwRn1wCjDJ2rqNJtiE9Vve4DrKP94:whatever \
#    -i -X GET http://127.0.0.1:5000/api/resource

### upload file
#curl -i -X POST -H "Content-Type: application/pdf" --data-binary "@path/to/file" http://localhost:5000/api/v1/upload

### post
#curl -u demo:123456 -i -X POST -d '{"tradeid":"1234456","lots":1}' http://127.0.0.1:5000/api/v1/post_trade
#curl -i -X POST -H "Key: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" http://localhost:5000/api/v1/post_trade
