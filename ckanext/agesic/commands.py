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
                try:
                    assert head(r.url).ok
                except AssertionError:
                    print '%s FROM %s "%s"' % (r.url, p.name, p.title)
                except Exception, e:
                    print '%s FROM %s "%s" (%s)' % (r.url, p.name, p.title,
                        e.__class__.__name__)
