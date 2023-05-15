import asyncio
from pathlib import Path
from random import randint
from typing import Dict

import yaml
from fabric2 import Connection
from glances_api import Glances


async def main():
    remotes_conf = Path('remotes.yaml')
    with open(remotes_conf, 'r') as remote_file:
        remotes_info: Dict[str: Dict[str, str]] = yaml.safe_load(remote_file)
    
    # select only linux machines
    linux_remotes = {k:v for k, v in remotes_info.items() if v['type'] == 'linux'}
    
    for remote, params in linux_remotes.items():
        c = Connection(params['hostname'], user=params['sysadmin'])
        try:
            result = c.run(f'glances -s')
        except:
            pass

        data = Glances(host=params['hostname'])
        await data.get_data()

if __name__ == "__main__":
    asyncio.run(main())
