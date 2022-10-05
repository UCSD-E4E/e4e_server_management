# `kastner-ml` Management Utility
## SSH Manager
### pubkeys.yaml
```
{user.email}:
    {ssh_key.name}:
        type: {ssh_key.type}
        key: {ssh_key.key}
        account:
            - {account_username}
```
For example, if gbluefin@ucsd.edu has an RSA key with hash ABCDEF  (`ssh-rsa ABCDEF gbluefin@MacBook`) and needs to access the account system_tester, then we would enter the following:
```
"gbluefin@ucsd.edu":
    "gbluefin@MacBook":
        type: ssh-rsa
        key: ABCDEF
        account:
            - system_tester
```
## Remote System Manager
### remotes.yaml
```
{system.name}:
    hostname: {hostname or IP}
    sysadmin: {sysadmin.username}
    type: {linux or windows}
```