# PyNex
Pynex is a python module for handling data transfers for BlueBrain's [KnowledgeGraph](https://bbp-nexus.epfl.ch/).
Use can also use [KnowledgeGraph Documentation](https://bbp-nexus.epfl.ch/dev/docs/kg/index.html) additionaly.

## Loading Pynex
To use pynex, import it and create an object:

```python
import pynex

pn = pynex.PyNex("bbp")
```
The first parameter of the initialization function is your own organization. If you are using an alternative to
EPFL's self-hosted KnowledgeGraph, you can simply specify it as a second parameter:

```python
pn = pynex.PyNex("bbp", "http://localhost:8080")
```
The url may not contain a trailing slash. The standard url is https://bbp-nexus.epfl.ch/

## Organizations
### List of Organizations
To obtain a list of organizations, you simply call the organizations() function:
```python
orgs = pn.organizations()
```
You will receive a Python dictionary with the number of organizations and a list containing all organizations:
```json
{
  "total": 4,
  "results": [
    {
      "resultId": "https://bbp-nexus.epfl.ch/dev/v0/organizations/bbp",
      "source": {
        "@id": "https://bbp-nexus.epfl.ch/dev/v0/organizations/bbp",
        "links": [
          {
            "rel": "self",
            "href": "https://bbp-nexus.epfl.ch/dev/v0/organizations/bbp"
          }
        ]
      }
    },
    ...
    ]
}
```
The above dictionary is the same as the JSON response from https://bbp-nexus.epfl.ch/dev/v0/organizations
You can also use pagination on the organizations list:
```python
orgs = pn.organizations(params={"from" : 1, "size" : 2})
```
### Information on an organization
To obtain information on an organization, you need to call the organization() function:
```python
pn.organization("read", "bbp")
```
If you specified an organization during intialization, you do not need to specify the second paramerter unless
you need information from another organization.

### Update Existing Organization
You can also update information of your organization. Before you can update your organization, 
you need to know the current revision number. You can obtain it with the read 
function from above.

Once you have the revision number, you can simply update via
```python
old_information = pn.organization("bbp")

my_organization = {
  "description" : "My organization"
}

revision = {
  "rev" : old_information["rev"]
}

pn.organization("update", "bbp", params=revision, http_body=my_organization)
```
### Create new Organization
To create a new organization, simply use
```python
pn.organization("create", "myneworg", http_body=my_organization)
```

### Deprecate organization
To deprecate an organization, use
```
pn.organization("delete", "myneworg")
```

## Domains

### List Domains
### Show Domain
### Create Domain
### Update Domain
### Delete Domain

## Schemas

### Show Schemas
### Create Schema
### Update Schema
### Delete Schema

## Instances

### Show Instances
### Create Instance
### Update Instance
### Delete Instance
