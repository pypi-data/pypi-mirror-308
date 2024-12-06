import subprocess
import re

process = subprocess.Popen(["/flag"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

output = process.stdout.readline()

match = re.search(r"(\d+) \* (\d+) \+ (\d+)", output)
if match:
    A = int(match.group(1))
    B = int(match.group(2))
    C = int(match.group(3))
    
    answer = A * B + C

    process.stdin.write(f"{answer}\n")
    process.stdin.flush()
    
    result = process.stdout.read()
    print(result.strip())

process.wait()