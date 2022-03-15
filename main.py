from bitrix24 import *
from nbformat import read
from config import *
import argparse
import csv
import json

bx24 = Bitrix24(token)
parser = argparse.ArgumentParser(description='Process file path')
parser.add_argument('-i','--input', default='input.csv')
parser.add_argument('-d','--delimiter', default=';')
parser.add_argument('-o','--output',default='error.csv')
parser.add_argument('-l','--mode', action='store_true')
parser.add_argument('-e','--encoding', default='utf-8')
args = parser.parse_args()
dictionary={}
columns=[]

with open(args.input, newline='', encoding=args.encoding) as csvfile:
    reader = csv.reader(csvfile, delimiter=args.delimiter)
    file=list(reader)
    columns=file[0]
    for row in file[1::]:
        dictionary[row[0]]={key: row[index] for key, index in zip(columns[1::],range(1,len(columns)))}
print(dictionary)

fields=bx24.callMethod('crm.lead.fields') if args.mode is True else bx24.callMethod('crm.deal.fields') 
print(fields)
extractedFields={}
for field, info in fields.items():
    if info!=None:
        extractedFields[field]={}
        if 'items' in info:
            extractedFields[field]['values']={item['VALUE']:item['ID'] for item in info['items']}
        if 'listLabel' in info:
            extractedFields[field]['title']=info['listLabel']
        else:
            extractedFields[field]['title']=info['title']
        extractedFields[field]['isMultiple']=info['isMultiple']


def convert(origin, template):
    result={}
    table={}
    for column in list(origin.values())[0]:
        for id, info in template.items():
            if info['title']==column:
                table[column]=id
    for id, fields in origin.items():
        result[id]={}
        for column, value in fields.items():
            if 'values' in template[table[column]]:
                if template[table[column]]['isMultiple']:     
                    result[id][table[column]]=[template[table[column]]['values'][value]]
                else:
                    result[id][table[column]]=template[table[column]]['values'][value]
            else:
                result[id][table[column]]=value

    return result

errors={}

converted=convert(dictionary, extractedFields)
for id, fields in converted.items():
    result=bx24.callMethod('crm.lead.update',id=id,fields=fields) if args.mode is True else bx24.callMethod('crm.deal.update',id=id,fields=fields) 
    print(str(id) + ":" + str(result))
    if result is not True:
        errors[id]=dictionary[id]

with open(args.output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, args.delimiter,
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(columns)
    for id, field in errors.items():
        writer.writerow(columns)