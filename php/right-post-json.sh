#!/bin/bash
curl -X POST -H "'Content-type':'application/json', 'charset':'utf-8', 'Accept': 'text/plain'" -d "{'d': {'ddd':'sss'}}" "http://localhost:8888/post-json.php"
