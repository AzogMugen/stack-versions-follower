from os import environ

if environ.get('MONGODB_HOSTNAME') is None:
	environ['MONGODB_HOSTNAME'] = '127.0.0.1' # for local dev without docker
MONGO_URI = 'mongodb://' + environ.get('MONGODB_HOSTNAME') + ':27017' # still in place cause I couldn't use volumes with docker desktop 2.2.0.5
# MONGO_URI = 'mongodb://' + environ.get('MONGODB_USERNAME') + ':' + environ.get('MONGODB_PASSWORD') + '@' + environ.get('MONGODB_HOSTNAME') + ':27017/?authSource=admin'