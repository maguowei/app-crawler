import os

# Redis
REDIS = {
    'host': os.environ.get('REDIS_HOST', '127.0.0.1'),
    'port': os.environ.get('REDIS_PORT', 31412),
    'db': os.environ.get('REDIS_DB', 0),
    'decode_responses': True,
}

# MySQL
MYSQL = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 30279),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'db': 'varys',
}
