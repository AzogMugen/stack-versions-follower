import os

os.environ['MONGODB_HOSTNAME'] = '127.0.0.1' # => to delete when mongo docker ready
MONGO_URI = 'mongodb://' + os.environ['MONGODB_HOSTNAME'] + ':27017' # => to delete when mongo docker ready
# MONGO_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017'