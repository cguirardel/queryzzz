
import requests
# import numpy as np

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

##
def filterdate(startdate,stopdate):
    if checkshort(startdate): startdate = short2round(startdate)
    if checkshort(stopdate): stopdate = short2round(stopdate)
    versions = queryzzz(r'/api/exports/')['players']
    vnum = []
    for v in versions:
        vi = int(v)
        if vi >= startdate and vi <= stopdate:
            vnum.append(vi)
        elif vi < startdate : break # accelerate the process, date are read from most recent to oldest
    return vnum

def findally(players, ally = 'SCF', playerlist = None):
    filt = []
    keys = ['pseudo', 'field', 'grade']
    for p in players:
        if p['alliance'] == ally :
            if playerlist is not None and p['pseudo'] in playerlist :
                pslice = {k:p[k] for k in keys}
                filt.append(pslice)
    return filt

def integrate(startdate,stopdate,playerlist = None):
    versions = filterdate(startdate,stopdate)
    p_dic = {}
    d_dic = {}
    for version in versions :
        players = findally(queryversion(version),ally='SCF', playerlist=playerlist)
        s = 0
        N = len(players)
        for p in players :
            name = p['pseudo']
            field = p['field']
            bois  = 2*field
            s += bois/N
            if name not in p_dic :
                p_dic[name] = bois
            else :
                p_dic[name] += bois

        for p in players :
            name = p['pseudo']
            field = p['field']
            bois  = 2*field
            if name not in d_dic :
                d_dic[name] = bois-s
            else :
                d_dic[name] += bois-s
    return p_dic, d_dic


##
d1 = '2026-11-05-12h'
d2 = '2026-11-12-12h'

tstart = int(f'{d1[:4]}{d1[5:7]}{d1[8:10]}{d1[11:13]}')
tstop = int(f'{d2[:4]}{d2[5:7]}{d2[8:10]}{d2[11:13]}')

playerlist = ['Mattimeo', 'Cat_Woman', 'AntiDot', 'antman', 'cytaf', 'Gadestryll', 'louispretends']

p_dic, d_dic = integrate(tstart,tstop,playerlist=playerlist)

##
s = ''
s = s+f'Du [b]{d1[8:10]}/{d1[5:7]}/{d1[:4]}[/b] à {d1[11:13]}h '
s = s+f'au [b]{d2[8:10]}/{d2[5:7]}/{d2[:4]}[/b] à {d2[11:13]}h\n\n'

fulld = 0
for name in p_dic:
    d = d_dic[name]
    fulld+=d # verify that this is 0 in the end
    if d < 0 : color = 'c5130f'
    else : color = '09750c'
    s = s+f'\t{name} : {p_dic[name]} ([color=#{color}]{d_dic[name]:+.0f}[/color])\n'

print(s)



