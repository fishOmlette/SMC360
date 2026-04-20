# utilising web scraping due to API restriction

import os, json, requests, logging
from functools import reduce

logger = logging.getLogger(__name__)
timestamp = os.getenv('timestamp')

class credentials:
    def __init__(self):
        env = os.getenv('platform')
        cred = json.loads(env) if env is not None else {}
        self.reddit = "https://www.reddit.com/r/"

class load_to_object_storage(credentials):
    def __init__(self, object_storage):
        super().__init__()
        self.object_storage = object_storage.connection()
        self.default_limit = 5000
        self.__file_path = f'reddit/{timestamp}'
    
    def posts(self, parameters):
        defaults = {
            'limit': 100
        }
        maxResults = self.default_limit
        url = self.reddit+parameters['subreddit']+'/'+parameters['type']+'.json'
        while maxResults > 0:
            maxResults -= defaults['limit']
            try:
                response = requests.get(url, params=defaults, headers = {'User-agent': 'smc360 reddit 0.1'})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(str(e))
                return
            data = response.json().get('data')
            defaults['after'] = data.get('after') if data.get('after') is not None else None
            if defaults['after'] is None:
                break
            for item in data.get('children'):
                post = item.get('data')
                json_string = json.dumps(post)
                self.object_storage.add_file(f"{self.__file_path}/posts/{post.get('id')}.json", json_string)

class load_to_database:
    def __init__(self, database, object_storage):
        self.database = database.connection()
        self.object_storage = object_storage.connection()
        self.timestamp = timestamp
        self.__file_path = f'reddit/{self.timestamp}'

    def read_parse_load(self, model, table_name):
        column_names = list(model.keys())
        paths = self.object_storage.get_objects(f'{self.__file_path}/{table_name}')
        entries = []
        for path in paths:
            try:
                file = json.loads(self.object_storage.read_file(path))
            except Exception as e:
                logger.error(str(e))
            entry = [self.timestamp]
            for keys in model.values():
                entry.append(reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys.split("."), file))
            entries.append(tuple(entry))
        with self.database as conn:
            try:
                conn.create_or_update_table(table_name, column_names)
                conn.add_records(table_name, column_names, entries)
            except Exception as e:
                logger.error(str(e))
    
    posts = read_parse_load