import json
import sys



x = json.loads(sys.argv[1])

x["ans"] = "hmmmm"


print(json.dumps(x))