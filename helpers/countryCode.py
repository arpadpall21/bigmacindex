import pycountry

def getCountryCode(country:str):
    if country == 'Russia':     # not supported by this package :/   -> duck taping
        return 'RUS'

    countries = {}
    for c in pycountry.countries:
        countries[c.name] = c.alpha_3

    return countries.get(country, 'Unknown code')
