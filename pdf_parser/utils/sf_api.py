"""
    SALESFORCE API MODULE
"""
import requests
from simple_salesforce import Salesforce, SFType
from pdf_parser.sf_config import ConnectionString


class SFConnectAPI:
    """
        SALESFORCE API CLASS
    """
    sf = None
    sf_bulk = None

    def __init__(self, sf_config=ConnectionString):
        """
        :param sf_config:
        """
        print("connecting with salesforce.")
        self.sf = Salesforce(username=sf_config.USERNAME,
                             password=sf_config.PASSWORD,
                             security_token=sf_config.SF_AUTH_TOKEN)
        # self.sf = Salesforce(instance=sf_config.SF_URL,
        #                      session_id=sf_config.ACCESS_TOKEN )
        self.sf_config = sf_config
        print("connection success")


    def get_header(self, session_id):
        """
        :return:
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + session_id,
            'X-PrettyPrint': '1'
        }
    def get_login_connection(self):
        """
        :param host:
        :return:
        """
        from simple_salesforce import  SalesforceLogin
        session_id, instance = SalesforceLogin(
            username=self.sf_config.USERNAME,
            password=self.sf_config.PASSWORD,
            security_token=self.sf_config.SF_AUTH_TOKEN )
        return session_id

    def get_access_token(self, sf_conn=ConnectionString):
        """
        :param sf_conn:
        :return:
        """
        con_data ={"grant_type":'password',
                   "client_id": "3MVG9d8..z.hDcPKNQnA7syhInwXgWNnvlVvxuvQ79VPmlbJp1CIg8dvDFWje3yzZCSdnowqpRrPFEsO3Xwxg",  # Consumer Key
                   "client_secret": "8951347997964366262",  # Consumer Secret
                   "username":sf_conn.USERNAME,
                   "password":sf_conn.PASSWORD+sf_conn.SF_AUTH_TOKEN}

        r = requests.post( "https://login.salesforce.com/services/oauth2/token", params=con_data )
        access_token = r.json().get( "access_token" )
        return access_token

    def execute_soql(self, query):
        """
        :param sf_conn:
        :param query:
        :param host:
        :return:
        """

        result = self.sf.query(query)
        return result

    def create_record(self, object_name='Employee__c', data=None):
        from simple_salesforce import SalesforceLogin
        session_id, instance = SalesforceLogin(
            username=self.sf_config.USERNAME,
            password=self.sf_config.PASSWORD,
            security_token=self.sf_config.SF_AUTH_TOKEN )
        from simple_salesforce import SFType
        try:
            sf_obj = SFType(object_name, session_id, self.sf_config.SF_URL)
            result = sf_obj.create(data)
        except Exception as ex:
            result = ex
            print repr(ex)
        return result


sf  =SFConnectAPI()
print repr(sf)
result =sf.create_record(object_name="Resume__c", data={"name":"test2", "Email__c":"amansinghbawa@gmail.com", "Phone__c":"7800100291", "Experience__c":"Test Experience", "Education__c":"Test Education"})
print result