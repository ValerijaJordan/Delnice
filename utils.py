import csv
import re
import os
from urllib.request import urlretrieve

delnice = ['SBITOP', 'GRVG', 'IEKG', 'KRKG', 'LKPG', 'MELR', 'PETG', 'POSR', 'TLSG', 'ZVTG', 'DPRG', 'ITBG', 'MAJG', 'MTSG', 'NIKN', 'SALR', 'SAVA', 'TCRG', 'UKIG', 'AGOG', 'CETG', 'CICG', 'DATR', 'GHUG', 'GSBG', 'IHPG', 'INRG', 'KDHR', 'KSFR', 'MKOG', 'MLHR', 'MR1R', 'NALN', 'RGZR', 'SING', 'SKDR', 'ST1R', 'TEAG', 'VHDR', 'ZDDG', 'PPDT', 'ADM2', 'AGO1', 'DPR1', 'DRS1', 'DRS3', 'GV01', 'IM01', 'KDH3', 'NLB19', 'PET2', 'PET3', 'RS33', 'RS38', 'RS49', 'RS53', 'RS62', 'RS63', 'RS66', 'RS67', 'RS69', 'RS70', 'RS72', 'RS73', 'RS74', 'SIJ4', 'SIJ5', 'SKD1', 'SOS3', 'TLS1', 'ZT02']


def shrani(url, ime_datoteke):
    '''Shrani html kodo spletne strani v .txt datoteko'''
    return urlretrieve(url, ime_datoteke)

def vsebina(file_name):
    '''Vrne vsebino datoteke'''
    with open(file_name) as dat:
        vsebina = dat.read()
    dat.close()
    return vsebina

def shrani_zgodovino():
    '''Za vsako delnico shrani html kodo in združi vrstice - da je laže z regularnimi izrazi'''
    for delnica in delnice:
        if delnica != 'SBITOP':
            ime_datoteke = '{}.txt'.format(delnica)
            url = 'http://www.ljse.si/cgi-bin/jve.cgi?doc=1298&date1=01.08.2015&date2=31.07.2016&SecurityId={}&IndexOrSecurity=%24SBITOP&x=26&y=8'.format(delnica)
            shrani(url, ime_datoteke)
            vrstice = []
            with open(ime_datoteke) as file:
                for vrstica in file:
                    vrstice.append(vrstica.strip())
            file.close()
            vrstica = ''.join(vrstice)
            with open(ime_datoteke, 'w') as file:
                file.write(vrstica)
            file.close

def naredi_csv():
    for delnica in delnice:
        if delnica == 'SBITOP':
            ime_datoteke = 'ADM2.txt'
            reg_ex = re.compile(r'<TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top>(?P<datum>\d{2}.\d{2}.\d{4})</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>\d*,*\d*-*</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<tocke>\d*,*\d*-*)</TD>')
        else:
            ime_datoteke = '{}.txt'.format(delnica)
            reg_ex = re.compile(r'<TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top>(?P<datum>\d{2}.\d{2}.\d{4})</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<odpiralni_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<najvisji_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<najnizji_tecaj>\d*,*\d*-*)</TD><TD c?l?a?s?s?=?o?z?a?d?j?e?T?e?c?a?j?n?i?c?a? ?vAlign=top align=right>(?P<uradni_tecaj>\d*,*\d*-*)</TD>')
        for ujemanje in re.finditer(reg_ex, vsebina(ime_datoteke)):
            slovar = ujemanje.groupdict()
            if delnica == 'SBITOP':
                slovar['tocke'].replace(',', '.')
            else:
                slovar['odpiralni_tecaj'] = slovar['odpiralni_tecaj'].replace(',', '.')
                slovar['najvisji_tecaj'] = slovar['najvisji_tecaj'].replace(',', '.')
                slovar['najnizji_tecaj'] = slovar['najnizji_tecaj'].replace(',', '.')
                slovar['uradni_tecaj'] = slovar['uradni_tecaj'].replace(',', '.')
            if not os.path.isfile('{}.csv'.format(delnica)):
                with open('{}.csv'.format(delnica), 'w') as csv_dat:
                    writer = csv.DictWriter(csv_dat, slovar.keys())
                    writer.writeheader()
                    writer.writerow(slovar)
                csv_dat.close()
            else:
                with open('{}.csv'.format(delnica), 'a') as csv_dat:
                    writer = csv.DictWriter(csv_dat, slovar.keys())
                    writer.writerow(slovar)
                csv_dat.close()

naredi_csv()


