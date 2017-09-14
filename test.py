import pprint
from PythonNexus import PythonNexus

pretty = pprint.PrettyPrinter()

# Instantiate PythonNexus
pn = PythonNexus(base_organization="bbp")

# Request all organizations
organizations = pn.organizations()

# Print all organizations
pretty.pprint(organizations)

# PythonNexus makes the request a dictionary
# This example shows the link of the first listed organization
pretty.pprint( organizations["results"][0]["resultId"] )

my_organization = pn.organization("show")
pretty.pprint(my_organization)

# Request an instance
organization = "nexus"
domain = "schemaorg"
name = "organization"
version = "v0.0.1"
instance = "ab54b438-c1f8-45ac-8531-cc366b5f0f9a"

inst = pn.instance("show", domain, name, version, instance, organization)

pretty.pprint(inst)
