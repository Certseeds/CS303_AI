import json

jsonData= input()
text = json.loads(jsonData)
print(text)
print(text['baseCases'])
for i in text['baseCases']:
    print("{}\n {}\n {}\n".format(i['datasetName'], i['time'], i['result']))
