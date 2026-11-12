
import requests

url = r'https://s5.fourmizzz.fr'



def queryzzz(qry):
    # qry = r'/api/exports/'  # liste des versions
    ans = requests.get(f'{url}{qry}')
    if ans.status_code  == 200 : #200 = OK
        return ans.json()
    else : raise ValueError('api return status code {ans.status_code}')


def querylast():
    versions = queryzzz(r'/api/exports/')
    last = versions['players'][0]
    qry = f'/api/exports/players/?version={last}'
    ans = queryzzz(qry)
    return ans
# a = queryzzz()

def findally(players, ally = 'SCF'):
    filt = []
    for p in players:
        if p['alliance'] == ally:
            filt.append(p)
    return filt

SCF = findally(querylast())

