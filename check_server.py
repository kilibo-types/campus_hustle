import urllib.request
import urllib.error

paths = ['/', '/marketplace/', '/dashboard/', '/gigs/create/', '/profile/']
for p in paths:
    try:
        u = urllib.request.urlopen('http://127.0.0.1:8001' + p)
        d = u.read(1000).decode('utf-8', 'replace')
        print(p, '->', u.status)
        print('\n'.join(d.splitlines()[:10]))
    except urllib.error.HTTPError as e:
        print(p, 'HTTPError', e.code)
        print(e.read(1000).decode('utf-8', 'replace').splitlines()[:20])
    except Exception as ex:
        print(p, 'ERR', ex)
