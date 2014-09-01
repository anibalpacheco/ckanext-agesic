import socket
from datetime import date, timedelta
from urlparse import urlparse, urlunsplit
from requests import head

from ckan.model import Session, Package
import ckan.plugins as plugins

class BrokenurlsCmd(plugins.toolkit.CkanCommand):
    """
    Check for broken resource urls.
    Additionaly alert for out of date datasets.
    """
    summary = __doc__

    def command(self):
        self._load_config()
        for pck in Session.query(Package).filter(Package.state == 'active'):
            upd_freq = pck.extras.get('update_frequency')
            if upd_freq and pck.metadata_modified.date() + timedelta(int(
                    upd_freq)) < date.today():
                print 'OUT OF DATE: %s - %s' % (pck.name, pck.title)
            for res in pck.resources:
                o = urlparse(res.url)
                if 'comprasestatales.gub.uy' in o.netloc:
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'comprasestatales.gub.uy', 'comprasestatales.red.uy'),
                        o.path, o.query, o.fragment))
                elif 'test.catalogodatos.gub.uy' in o.netloc and \
                        socket.gethostname() == self._get_config().get(
                            'agesic.test_hostname'):
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'test.catalogodatos.gub.uy', 'localhost'), o.path,
                        o.query, o.fragment))
                elif 'catalogodatos.gub.uy' in o.netloc and \
                        socket.gethostname() == self._get_config().get(
                            'agesic.prod_hostname'):
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'catalogodatos.gub.uy', 'localhost'), o.path, o.query,
                        o.fragment))
                else:
                    url = res.url
                try:
                    assert head(url).ok
                except AssertionError:
                    print '%s FROM %s "%s"' % (url, pck.name, pck.title)
                except Exception, e:
                    print '%s FROM %s "%s" (%s)' % (url, pck.name, pck.title,
                        e.__class__.__name__)
