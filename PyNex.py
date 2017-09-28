import urllib3
import json

class PyNex:
    def __init__(
           self,
           base_organization="",
           base_url="https://bbp-nexus.epfl.ch/dev/v0",
           encoding="UTF-8"
           ):
        self.url = base_url
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
            params_text += "&"
        url += params_text

        assignments = {
                "read" : "GET",
                "create" : "PUT",
                "update" : "POST",
                "delete" : "DELETE"
            }

        if action in assignments:
            return self._http_request(assignments[action], url, http_body_text)
        else:
            self._error("Unknown action")

    def _error(self, error_message):
        error = {}
        error["success"] = False
        error["message"] = error_message
        return error
    
    def _http_request(self, method, url, http_body):
        http = urllib3.PoolManager()
        
        r = http.request(
                method,
                url,
                headers={'Content-Type': 'application/json'},
                body=http_body)
        
        return json.loads(r.data.decode(self._encoding))

    def organization_list(self, params={}):
        url = self.url + "/organizations"
        return self._actions("read", url, params)

    def organization(
            self,
            action,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url_formatting = {
                "url" : self.url,
                "organization" : organization
            }

        url_format = "{url}/organizations/{organization}"

        url = url_format.format(**url_formatting)
        return self._actions(action, url, params, http_body)


    def domain_list(self, organization=None, params={}):

        if organization is None:
            organization = self._base_organization

        url_formatting = {
                "url": self.url,
                "organization" : organization
            }

        url_format = "{url}/organizations/{organization}/domains"

        url = url_format.format(**url_formatting)

        return self._actions("read", url, params)

    def domain(
            self,
            action,
            domain,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url_formatting = {
                "url": self.url,
                "organization" : organization,
                "domain" : domain
            }

        url_format = "{url}/organizations/{organization}/domains/{domain}"
        url = url_format.format(**url_formatting)

        return self._actions(action, url, params, http_body)

    def schema_list(
            self,
            domain=None,
            organization=None,
            params={},
            http_body={}):
        if organization is None:
            organization = self._base_organization

        url_formatting = {
                "url": self.url,
                "organization" : organization
            }

        url_format = "{url}/schemas/{organization}/"
        url = url_format.format(**url_formatting)

        if not domain is None:
            url += domain + "/"

        return self._actions("read", url, params, http_body)

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

        url_formatting = {
                "url" : self.url,
                "organization" : organization,
                "domain" : domain,
                "name" : name,
                "version" : version
            }

        url_format = "{url}/schemas/{organization}/{domain}/{name}/{version}"

        url = url_format.format(**url_formatting)

        return self._actions(action, url, params, http_body)

    def instance_list(
            self,
            domain="",
            name="",
            version="",
            organization=None,
            params={},
            http_body={}):

        if organization is None:
            organization = self._base_organization

        url = self.url + "/data/"

        if not organization is "":
            url += organization + "/"
        if not domain is "":
            url += domain + "/"
        if not name is "":
            url += name + "/"
        if not version is "":
            url += version + "/"

        return self._actions("read", url, params, http_body)

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

        return self.instance_list(domain, name, version, organization, params)

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

        url = "{}/data/{}/{}/{}/{}/{}".format(
                self.url,
                organization,
                domain,
                name,
                version,
                instance
            )
        return self._actions(action, url, params, http_body)

    @staticmethod
    def match(search, dataset):
        result = []

        for data in dataset:
            match = 0

            for entry in data:
                for s in search:
                    if s == entry and search[s] == data[s]:
                        match += 1

            if match == len(search):
                result.append(data)

        return result
