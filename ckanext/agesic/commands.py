import requests

from ckan.model import Session, Package
import ckan.plugins as plugins


class BrokenurlsCmd(plugins.toolkit.CkanCommand):
    """ Check for broken resource urls """
    summary = __doc__

    def command(self):
        self._load_config()
        for p in Session.query(Package).filter(Package.state == 'active'):
            for r in p.resources:
                if not requests.head(r.url).ok:
                    print p.name, p.title, r.url
