
import yaml

import zeep
from zeep.wsse.username import UsernameToken


# Get_Workers
def get_workers():

    with open('config.yml', 'r') as cfg_f:
        config = yaml.safe_load(cfg_f)
    username = config['workday_username']
    password = config['workday_password']

    # Soap client
    # https://community.workday.com/sites/default/files/file-hosting/productionapi/Human_Resources/v30.2/Human_Resources.html
    # https://community.workday.com/sites/default/files/file-hosting/productionapi/Human_Resources/v30.2/Get_Workers.html
    wsdl_url = 'https://community.workday.com/sites/default/files/file-hosting/productionapi/Human_Resources/v30.2/Human_Resources.wsdl'
    client = zeep.Client(
        wsdl_url,
        wsse=UsernameToken(username, password))

    # Get service location
    # Login to workday, search for Public Web Service, Click on '...' next to Human Resources, Web Service -> View WSDL
    # This will give you an xml file. Open it in a text editor, scroll to the bottom, look for soapbind:address
    # copy the 'location' value
    # also take notice of wsdl:port, see 'binding' is 'wd-wsdl:Human_ResourcesBinding'
    location = 'https://SERVICE-INST.myworkday.com/ccx/service/TENANT/Human_Resources/v30.2'

    # Get binding path
    # http://docs.python-zeep.org/en/master/client.html#creating-new-serviceproxy-objects
    # Open the wsdl_url, search for xmlns:wd-wsdl, you will see 'urn:com.workday/bsvc/Human_Resources'
    # combine with what we saw from 'binding' above
    binding_path = '{urn:com.workday/bsvc/Human_Resources}Human_ResourcesBinding'

    # create service
    service = client.create_service(binding_path, location)
    result = service.Get_Workers()
    print(result)


if __name__ == '__main__':
    get_workers()