from glob import glob
import os
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Set, Union

import schema
import yaml


class KeyType(Enum):
    RSA="ssh-rsa"
    ED25519="ssh-ed25519"

@dataclass
class Key:
    key_type: KeyType
    key: str
    name: str

    def authorized_key_entry(self):
        return f'{self.key_type.value} {self.key} {self.name}'

def ssh_manager():
    key_schema = schema.Schema({
        str: {
            str: {
                "type": schema.Or(*(e.value for e in KeyType)),
                "key": str,
                "account": [str]
            }
        }
    })
    key_conf = Path('pubkeys.yaml')
    with open(key_conf, 'r') as key_file:
        key_info = yaml.safe_load(key_file)
    
    key_info: Dict[str, Dict[str, Dict[str, Union[str, List[str]]]]] = key_schema.validate(key_info)
    
    authorized_keys: Dict[str, List[Key]] = {}
    user_access_report: Dict[str, Set[str]] = {}
    account_access_report: Dict[str, Set[str]] = {}

    for user, keys in key_info.items():
        if user not in user_access_report:
            user_access_report[user] = set()

        for key_name, key_data in keys.items():
            key = Key(KeyType(key_data['type']), key_data['key'], key_name)
            for account in key_data['account']:
                if account not in authorized_keys:
                    authorized_keys[account] = [key]
                else:
                    authorized_keys[account].append(key)
    
                user_access_report[user].add(account)

                if account not in account_access_report:
                    account_access_report[account] = set([user])
                else:
                    account_access_report[account].add(user)
    
    accounts_to_create: List[str] = []
    for account in authorized_keys:
        try:
            subprocess.run(['id', '-u', account], check=True)
        except subprocess.CalledProcessError:
            accounts_to_create.append(account)
    
    with open('account_create.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        for account in accounts_to_create:
            f.write(f'useradd -m -s /bin/bash {account}\n')
    
    old_keys = glob("*_authorized_keys")
    for old_key_file in old_keys:
        os.remove(old_key_file)

    with open('account_update.sh', 'w') as update:
        update.write('#!/bin/bash\n')
        for account, keys in authorized_keys.items():
            with open(f'{account}_authorized_keys', 'w') as f:
                f.write('# Do not modify this file by hand - please submit keys to be added to the server admin\n')
                for key in keys:
                    f.write(key.authorized_key_entry() + '\n')
            update.write(f'mkdir -p /home/{account}/.ssh\n')
            update.write(f'chown {account}:{account} /home/{account}/.ssh\n')
            update.write(f'cp {account}_authorized_keys /home/{account}/.ssh/authorized_keys\n')
            update.write(f'chown {account}:{account} /home/{account}/.ssh/authorized_keys\n')
            update.write(f'chmod 600 /home/{account}/.ssh/authorized_keys\n\n')
        
    with open('user_access_report.md', 'w') as report:
        report.write("# User Access Report\n")
        for user, accounts in user_access_report.items():
            report.write(f"## `{user}`\n")
            for account in accounts:
                report.write(f'- `{account}`\n')
            report.write('\n')
    
    with open('account_access_report.md', 'w') as report:
        report.write('# Account Access Report\n')
        for account, users in account_access_report.items():
            report.write(f'## `{account}`\n')
            for user in users:
                report.write(f'- `{user}`\n')
            report.write('\n')
            
if __name__ == '__main__':
    ssh_manager()
