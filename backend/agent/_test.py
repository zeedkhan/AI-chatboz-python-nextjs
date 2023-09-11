import json

t = "{'use_function': true, 'response': ['googlecloudauth']}"

input_text = t.replace("'", "\"")

print(json.loads(input_text))