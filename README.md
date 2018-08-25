## Cloud Native App

## Make request by using the curl
```
 curl -i -H "Content-Type: application/json" -X POST -d '{
    "username":"mahesh@rocks", "email": "mahesh99@gmail.com",
    "password": "mahesh123", "name":"Mahesh" }' http://localhost:5000/api/v1/users

curl -i -H "Content-Type: application/json" -X delete -d '{
   "username":"mahesh@rocks" }' http://localhost:5000/api/v1/users
```
