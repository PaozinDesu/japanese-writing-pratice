# ResultadoMobile é um estado estático: reaproveita a fonte e aplica os tokens do Design System.
import re, ds
from common import HELMET
s = open('resultado_src.html').read()
s = re.sub(r'<helmet>.*?</helmet>', lambda m: HELMET, s, count=1, flags=re.S)
from common import to_mobile_links
open('project/ResultadoMobile.dc.html', 'w').write(ds.normalize(to_mobile_links(s), mobile=True))
