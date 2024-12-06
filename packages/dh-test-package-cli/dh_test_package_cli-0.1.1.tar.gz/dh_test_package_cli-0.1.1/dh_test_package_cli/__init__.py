import sys
import base64

print(eval(base64.b64decode(sys.argv[1])))
