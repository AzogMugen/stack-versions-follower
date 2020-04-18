# Stack Versions Tracker SVT
A small and simple flask and mongo app to keep track of versions of an environment 

## Synthesis

Meant to be called with a simple call to `/create` by Jenkins, Gitlab-ci or else, whenever an app is deployed into an environment.  
So at every moment the SVT will keep track of the versions of the apps deployed in an environment   
  
Actually only 2 routes :  
  
- `/list` method GET [string:env] : 
Returns list of all applications of an env from DB  

- `/create` method POST [string:env, string:name, string:version] :  
Creates (if not exist, based on name) or updates (if exist, based on name) an application with its name, version, and environment of deployment  
  
Checks if required params are presents, and also if param version matches a regex.  
  
Actually doesn\'t work in standalone, needs to have local mongo server.  

Since it\'s mongoDB, no schema and one can add whatever param he likes such as url.


## Config

URL : `http://127.0.0.1:5000`
MongoDB : `mongodb://127.0.0.1:27017`

## Todos

- Check if collection (env) exists in the DB and create a new one if not
- Manage configuration outside of code, not hard coded
- Manage history by adding each time another version, instead of updating one
- Create a page with datatables to see actual applications deployed in the selected env with templates
- Create a page to view history of deployment of a certain application
- Add requirements.txt
- Dockerize the application (nginx ?)
- Manage https (nginx ?)
- Add tests
- Add authentication ?

## Tests

On my machine I tried to insert 260 000 different entries like the following :

```python
{
	"env":"dev",
	"name":"Name of the application",
	"url":"http://www.whatever.com:1337/random/url/long/enough",
	"version":"5.27.94"
}
```

And the mongo collection weighed about ~ 46 MB.  
  
I choosed 260 000 because it represents :  
365 days - (52 * 2) days of weekend = almost 260 days  

And after it\'s a factor of a 1000 to represent the number of applications, deployments per day and years :  
 - 10 applications deployed 10 times a day over 10 years  
 - 100 applications deployed 1 times a day over 10 years  
 - 1000 applications deployed 1 times a day over 1 year  
 - you choose

So I think it\'s worth looking for keeping an history of the apps  

## Changelog

0.9.0 
=====

1st version
