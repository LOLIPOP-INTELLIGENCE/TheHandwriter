import json

dict_str = '{"test": 1}'
dict_obj = json.loads(dict_str)

print(dict_obj['test'])