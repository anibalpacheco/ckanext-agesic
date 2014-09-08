import socket, csv, smtplib
from datetime import date, timedelta
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from urlparse import urlparse, urlunsplit
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from requests import head

from ckan.model import Session, Package
import ckan.plugins as plugins

class BrokenurlsCmd(plugins.toolkit.CkanCommand):
    """
    Check for broken resource urls.
    Additionaly alert for recently updated and out of date datasets.
    """
    summary = __doc__

    def command(self):
        self._load_config()
        sio = StringIO()
        output, today, cfg = csv.writer(sio), date.today(), self._get_config()
        output.writerow(['Fecha', 'Tipo', 'Nombre', 'Titulo', 'Fecha o URL'])
        for pck in Session.query(Package).filter(Package.state == 'active'):
            upd_freq = pck.extras.get('update_frequency')
            # check if this dataset should have been updated
            if upd_freq and pck.metadata_modified.date() + timedelta(int(
                    upd_freq)) < today:
                output.writerow([today, 'Dataset Desactualizado', pck.name,
                    pck.title,
                    pck.metadata_modified.date() + timedelta(int(upd_freq))])
            # check if this dataset was updated this week
            if pck.metadata_modified.date() > today - timedelta(7):
                output.writerow([today, 'Dataset Actualizado', pck.name,
                    pck.title, pck.metadata_modified.date()])
            # and now check its resources for broken links
            for res in pck.resources:
                o = urlparse(res.url)
                if 'comprasestatales.gub.uy' in o.netloc:
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'comprasestatales.gub.uy', 'comprasestatales.red.uy'),
                        o.path, o.query, o.fragment))
                elif 'test.catalogodatos.gub.uy' in o.netloc and \
                        socket.gethostname() == cfg.get('agesic.test_hostname'):
                    url = urlunsplit((o.scheme, o.netloc.replace(
                        'test.catalogodatos.gub.uy', 'localhost'), o.path,
                        o.query, o.fragment))
                elif 'catalogodatos.gub.uy' in o.netloc and \
                        socket.gethostname() == cfg.get('agesic.prod_hostname'):
                    url = urlunsplit((o.scheme.replace('https', 'http'),
                        o.netloc.replace('catalogodatos.gub.uy', 'localhost'),
                        o.path, o.query, o.fragment))
                else:
                    url = res.url
                try:
                    assert head(url).ok
                except AssertionError:
                    output.writerow([today, 'Enlace Roto', pck.name, pck.title,
                        url])
                except Exception, e:
                    output.writerow([today, 'Enlace Roto - ' + \
                        e.__class__.__name__, pck.name, pck.title, url])
        adjunto = MIMEText(sio.getvalue())
        adjunto.add_header('Content-Disposition', 'attachment',
            filename='brokenurls_%s.csv' % today.strftime("%Y%m%d"))
        msg = MIMEMultipart()
        msg['To'] = cfg.get('agesic.brokenurls_msg_to')
        msg['Subject'] = "[CKAN] Reporte de actualizaciones y enlaces rotos"
        msg.attach(adjunto)
        smtp = smtplib.SMTP(cfg.get('smtp.server', 'localhost'),
            cfg.get('smtp.port', 0))
        try:
            smtp.login(cfg.get('smtp.user'), cfg.get('smtp.password'))
        except smtplib.SMTPException:
            pass
        smtp.sendmail(cfg.get('smtp.mail_from'),
            [cfg.get('agesic.brokenurls_msg_to')], msg.as_string())
