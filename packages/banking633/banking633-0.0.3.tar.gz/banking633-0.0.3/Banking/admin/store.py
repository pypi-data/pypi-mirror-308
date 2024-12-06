import os
import json
from .action import action
from .card import Card, User

current_work_dir = os.path.dirname(__file__)


class Store():
    data_file_path = os.path.join(current_work_dir, '../data.json')

    def __init__(self):
        self.users = self.read_users_from_file()
        

    def save_all_data(self):
        new_data = {}
        for k in self.users.keys():
            new_data[k] = self.users[k].to_dict()
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_data, ensure_ascii=False))

    def read_users_from_file(self):
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            for k, v in data.items():
                v['card'] = Card(**v['card'])
                data[k] = User(**v)
            return data

        
    def admin_view(self):
        pass

    def user_view(self):
        pass
