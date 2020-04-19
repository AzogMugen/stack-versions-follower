# Stack Versions Tracker SVT
A small and simple flask and mongo app to keep track of versions of an environment 

## Synthesis

Meant to be called with a simple call to `/create` by Jenkins, Gitlab-ci or else, whenever an app is deployed into an environment.  
So at every moment the SVT will keep track of the versions of the apps deployed in an environment   
  
Actually 3 routes :  

- `/create` method POST [string:env, string:name, string:version] :  
Creates (if not exist, based on name) or updates (if exist, based on name) an application with its name, version, and environment of deployment  
Checks if required params are presents, and also if param version matches a regex.  
Since it\'s mongoDB, no schema and one can add whatever param he likes such as url. Just they won\'t show up
  
- `/list` method GET [string:env] : 
Returns list of all applications of an env from DB  

- `/` method GET [ ] : 
Shows a template page html with all the entries of one stack  

  
Actually doesn\'t work in standalone, needs to have local mongo server.  

  
## Config

URL : `http://127.0.0.1:5000`  
MongoDB : `mongodb://127.0.0.1:27017`
Default database : `stacks`

## Todos

- Add datatables to filter results by application name, fuzzy search mandatory
- Clean the mess a little with the templates
- Add bootstrap because it's naked
- Dockerize the application (nginx ?)
- Manage configuration outside of code, not hard coded
- Manage https (nginx ?)
- Add tests
- Add authentication ? UI, API, DB ?
- Manage history by adding each time another version, instead of updating one ?
- If yes, create a page to view history of deployment of a certain application ?
 => Remind that it will lose params like url if not sent, and mongo queries with dates will be needed

## Tests

`test_regex.py` allows to kind of "unit test" the regex for the versions. Probably some tests are missing.

In the hypothesis of keeping an history, I tried to insert 260 000 different random entries like the following :

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
 - 100 applications deployed 10 times a day over 1 year  
 - 1000 applications deployed 1 times a day over 1 year  
 - you choose



## Changelog

0.10.1
======

 - Added requirements.txt via https://github.com/bndr/pipreqs
 - Prepared env vars for mongo

0.10.1
======

 - Added dropdown to select the environment
 - Added screenshots of poor UI

0.10.0
======

 - Added page to view the result for only one default stack
 - Forced the date on creation and update of an entry


0.9.0 
=====

1st version
