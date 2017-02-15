#!/bin/bash
curl -i -X POST host:port/post-file -H "Content-Type: text/xml" --data-binary "@path/to/file"
curl -i -X POST -H "Key: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" http://localhost:5000/api/v1/post_trade
