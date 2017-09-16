import urllib3
import json

class PythonNexus:
    def __init__(
           self,
           base_url="https://bbp-nexus.epfl.ch",
           env="dev",
           version="v0",
           encoding="UTF-8",
           base_organization=""):
        self.url = base_url + "/" + env + "/" + version + "/"
        self._encoding = encoding
        self._base_organization = base_organization

    def _actions(self, action, url, params, http_body={}):
        if not http_body:
            http_body_text = ""
        else:
            http_body_text = json.dumps(http_body)
        params_text = "?"

        for key in params:
            if params[key] is True:
                params_text += key + "=true" 
            elif params[key] is False:
                params_text += key + "=false"
            else:
                params_text += key + "=" + str(params[key])
        url += params_text

        assignments = {
                "write" : "GET",
                "create" : "POST",
                "update" : "PUT",
                "delete" : "DELETE"
            }

        if action in assigments:
            return self._http_request(assignments[action], url, http_body_text)
        else:
            self._error("Unknown action")

    def _error(self, error_message):
        error = {}
        error["success"] = False
        error["message"] = error_message
    
    def _http_request(self, method, url, http_body):
        http = urllib3.PoolManager()

        url+="&pretty=true"
        
        r = http.request(
                method,
                url,
                headers={'Content-Type': 'application/json'},
                body=http_body)
        
        return json.loads(r.data.decode(self._encoding))

    def organizations(self, params={}):
        url = self.url + "organizations"
        return self._actions("show", url, params)

    def organization(
            self,
            action,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization
        url = self.url + "organizations/" + organization
        return self._actions(action, url, params, http_body)


    def domains(self, organization=None, params={}):

        if organization is None:
            organization = self._base_organization

        url = self.url + "organizations/" + organization + "/domains"

        return self._actions("show", url, params)

    def domain(
            self,
            action,
            domain,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url = self.url + "domains/" + organization + "/domains/" + domain

        return self._actions(action, url, params, http_body)

    def schemas(
            self,
            domain=None,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url = self.url + "schemas/" + organization + "/"

        if not domain is None:
            url += domain + "/"

        return self._actions("GET", url, params, http_body)

    def schema(
            self,
            action,
            domain,
            name,
            version="",
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url = self.url + "schemas/" + organization + "/" + "domain/"
        url += name + "/"
        url += version

        return self._actions(action, url, params, http_body)

    def instances(
            self,
            domain="",
            name="",
            version="",
            organization=None,
            params={},
            http_body={}):

        if organization is None:
            organization = self._base_organization

        url = self.url + "data/"

        if not organization is "":
            url += organization + "/"
        if not domain is "":
            url += domain + "/"
        if not name is "":
            url += name + "/"
        if not version is "":
            url += version + "/"

        return self._actions("show", url, params, http_body)

    def fullsearch(
            self,
            search_query,
            domain="",
            name="",
            version="",
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization
        params = { "q" : search_query }

        return self.instances(domain, name, version, organization, params)

    def instance(
            self,
            action,
            domain,
            name,
            version,
            instance="",
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url = self.url + "data/"
        url += organization + "/"
        url += domain + "/"
        url += name + "/"
        url += version + "/"
        url += instance

        return self._actions(action, url, params, http_body)

