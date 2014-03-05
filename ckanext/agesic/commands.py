from urlparse import urlparse, urlunsplit
from requests import head

from ckan.model import Session, Package
import ckan.plugins as plugins


class BrokenurlsCmd(plugins.toolkit.CkanCommand):
    """ Check for broken resource urls """
    summary = __doc__

    def command(self):
        self._load_config()
        for p in Session.query(Package).filter(Package.state == 'active'):
            for r in p.resources:
                o = urlparse(r.url)
                if 'comprasestatales.gub.uy' in o.netloc:
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'comprasestatales.gub.uy', 'comprasestatales.red.uy'),
                        o.path, o.query, o.fragment))
                else:
                    url = r.url
                try:
                    assert head(url).ok
                except AssertionError:
                    print '%s FROM %s "%s"' % (url, p.name, p.title)
                except Exception, e:
                    print '%s FROM %s "%s" (%s)' % (url, p.name, p.title,
                        e.__class__.__name__)
