#
# Description
# Authenticates against sheldon 
#
#from urlparse import urlparse
#from eventlet.green import httplib

from keystone.common import wsgi
from keystone.openstack.common import log as logging
import webob
import requests


class SheldonAuth(wsgi.Middleware):
    def __init__(self, app, conf):
        self.app = app
        self.config = conf
        self.log = logging.getLogger(__name__)
        #super(SheldonAuth, self).__init__(*args, **kwargs)

    def __call__(self, environ, start_response):
        return self.process_request(environ, start_response)

    def str2bool(self, str):
        if not str:
            return False
        if str in ['false', 'False', 'no', '0']:
            return False
        return True

    def do_auth(self, environ):
        '''Performs the actual authentication on the request
        This will check a dictionary to see if there is a alias for this user'''
        auth = self.get_auth_details(environ)
        userlookup = False
        userlookupdict = self.get_userlookuplist()
        if auth == None:
            self.log.debug('Not authenticating to Sheldon')
            return None

        if auth[0] in userlookupdict.keys():
            userlookup = str(auth[0])
            self.log.info("Found a alias for this user")
            auth = (userlookupdict[auth[0]], auth[1])
        url = self.config.get('url')
        verify = self.str2bool(self.config.get('verify_ssl', 'True'))
        r = requests.get(url, auth=auth, verify=verify)
        if r.status_code == 200:
            if userlookup:
                self.log.info('Aliased admin user: authenticated user {0} against Sheldon'.format(auth[0]))
                return userlookup
            self.log.info('Authenticated user {0} against Sheldon'.format(auth[0]))
            return auth[0]

        self.log.info('Failed authenticating user {0} against Sheldon'.format(auth[0]))
        return None

    def get_userlookuplist(self):
        userlookupdict = {}
        aliascsv = self.config.get('aliaslist')
        try:
            aliaslines = [line.strip() for line in open(aliascsv)]
        except:
            self.log.info('Failed to open alias file, aliases disabled')
            return userlookupdict
        for alias in aliaslines:
            userlookupdict[alias.split(',')[0]] = alias.split(',')[1].strip()
        return userlookupdict

    def get_auth_details(self, environ):
        '''Extracts auth details from requests and returns a tuple (username, password) if found,
        otherwise returns None'''
        try:
            auth = environ['openstack.params']['auth']['passwordCredentials']
            username = auth['username']
            password = auth['password']
        except KeyError:
            # request contains no or invalid authentication context
            self.log.debug('No authentication context in request')
            return None
        return (username, password)

    def process_request(self, environ, start_response):
        if environ.get('REMOTE_USER', None) is not None:
            # Assume that it is authenticated upstream
            return self.application

        username = self.do_auth(environ)
        if username is not None:
            # User is authenticated, set REMOTE_USER and hand off to next app
            environ['REMOTE_USER'] = self.config.get('user_prefix', '') + username + self.config.get('user_suffix', '')
        return self.app(environ, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return SheldonAuth(app, conf)
    return auth_filter

