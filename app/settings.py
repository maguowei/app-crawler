import os

# Redis
REDIS = {
    'host': os.environ.get('REDIS_HOST', 'redis'),
    'port': os.environ.get('REDIS_PORT', 6379),
    'db': os.environ.get('REDIS_DB', 0),
    'decode_responses': True,
}

# MySQL
MYSQL = {
    'host': os.environ.get('DB_HOST', 'mysql'),
    'port': os.environ.get('DB_PORT', 3306),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'db': 'varys',
    # 'charset': 'utf8mb4',
}
