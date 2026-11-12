
import requests
import numpy as np

url = r'https://s5.fourmizzz.fr'

##
def full2short(timestamp):
    short = int(int(timestamp)/100)
    return short

def short2round(timestamp):
    return 100*timestamp

def full2round(timestamp):
    short = full2short(timestamp)
    return short2round(short)

def checkshort(timestamp):
    ts = int(timestamp)
    if ts < 2*10e8 : raise ValueError('too short for a short !')
    if ts > 3*10e10 : raise ValueError('too long for a long !')
    return int(timestamp) < 2*10e10
##
def queryzzz(qry):
    # qry = r'/api/exports/'  # liste des versions
    ans = requests.get(f'{url}{qry}')
    if ans.status_code  == 200 : #200 = OK
        return ans.json()
    else : raise ValueError('api return status code {ans.status_code}')

def querylast():
    versions = queryzzz(r'/api/exports/')
    last = versions['players'][0]
    ans = queryversion(last)
    return ans
# a = queryzzz()
def queryversion(version):
    if full2short(version) < 2026100616: raise ValueError(f'requested version is {version} API was not started at this date : /')
    qry = f'/api/exports/players/?version={version}'
    ans = queryzzz(qry)
    return ans

def filterdate(startdate,stopdate):
    if checkshort(startdate): startdate = short2round(startdate)
    if checkshort(stopdate): stopdate = short2round(stopdate)
    versions = queryzzz(r'/api/exports/')['players']
    vnum = []
    for v in versions:
        vi = int(v)
        if vi >= startdate and vi <= stopdate:
            vnum.append(vi)
    return vnum

def findally(players, ally = 'SCF'):
    filt = []
    keys = ['pseudo', 'field', 'grade']
    for p in players:
        if p['alliance'] == ally:
            pslice = {k:p[k] for k in keys}
            filt.append(pslice)
    return filt

def integrate(startdate,stopdate):
    versions = filterdate(startdate,stopdate)
    p_dic = {}
    for version in versions :
        players = findally(queryversion(version),ally='SCF')
        for p in players :
            name = p['pseudo']
            field = p['field']
            bois  = 2*field
            if name not in p_dic :
                p_dic[name] = bois
            else :
                p_dic[name] += bois
    return p_dic

SCF = integrate(2026111018,2026111212)

