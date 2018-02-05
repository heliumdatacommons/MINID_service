# MINID_service
A MINID (http://minid.bd2k.org/) instance for minting identifiers for use across the DataCommons software architecture

mid = MINIDIntegration(config='../config/my-config.cfg', filename='ark:/88120/r8059v', test=True)

##  Command line to class
Register User

`minid.py --register_user --email <email> --name <name> [--orcid <orcid>]`

```
MINIDIntegration(
    config='../config/my-config.cfg', 
    register_user=True, 
    email=abc@123.edu, 
    name=user test=True)
```  

## Register Entity

`minid.py --register [--title <title>] <file_name>`

```
 MINIDIntegration(config='../config/my-config.cfg', register=True, title='title'. file_name=<"file or identifier to retrieve information about or register">)
```
## Retrieve metadata about a file or identifier

`minid.py <file_name>`

```MINIDIntegration(config='../config/my-config.cfg', filename=<"file or identifier to retrieve information about or register">)inid.py <identifier>```

## Update metadata about an identifier:

`minid.py --update [--title <title>] [--status <status>] [--obsoleted_by <minid>] [--locations <loc1> <loc2>] <identifier>`

``` 
MINIDIntegration(
    config='../config/my-config.cfg', 
    title=<title>, 
    status=<status>, 
    obsoleted_by=<minid>, 
    locations=<loc1> <loc2>,
    filename=<"file or identifier to retrieve information about or register">,
    )```

