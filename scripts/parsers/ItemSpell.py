# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0301

"""
@author: Kutikuti
"""

import sys
import os
import csv
import operator
from collections import OrderedDict

generatedDir = os.path.join('scripts', 'DBC', 'generated')
addonEnumDir = os.path.join('addon', 'DBC')

os.chdir(os.path.join(os.path.dirname(sys.path[0]), '..', '..', 'hero-dbc'))

## Mapping
# id_parent and id_spell itemEffect

# Parse every csv files into dict
db = {}
dbFiles = ['ItemEffect']
for dbFile in dbFiles:
    with open(os.path.join(generatedDir, f'{dbFile}.csv')) as csvfile:
        reader = csv.DictReader(csvfile, escapechar='\\')
        db[dbFile] = {}
        for row in reader:
            db[dbFile][int(row['id'])] = row

# Get every spell id associated to an item effect
Items = {}
with open(os.path.join(generatedDir, 'ItemXItemEffect.csv')) as csvfile:
    reader = csv.DictReader(csvfile, escapechar='\\')
    reader = sorted(reader, key=lambda d: int(d['id_parent']))
    for row in reader:
        if int(row['id']) > 0:
            Items[int(row['id_parent'])] = int(db['ItemEffect'][int(row['id_item_effect'])]['id_spell'])

with open(os.path.join(addonEnumDir, 'ItemSpell.lua'), 'w', encoding='utf-8') as file:
    file.write('HeroDBC.DBC.ItemSpell = {\n')
    for _, itemRow in enumerate(Items):
        file.write('  [' + str(itemRow) + '] = ' + str(Items[itemRow]) + ',\n')
    file.write('}\n')
