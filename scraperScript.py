from mitmproxy import http
from mitmproxy import types
from mitmproxy import ctx
import json
import csv

f = open('database.csv','a',newline='')
writer = csv.writer(f)

def response(flow: http.HTTPFlow) -> None:
  
  if (flow.request.path.startswith('/v1/posts/comments?')):
    postInfo = json.loads(flow.response.content)['posts'][0]
    text, date = postInfo['context'], postInfo['created_at'][0:10]
    row = (date,text)
    writer.writerow(row)

  elif (flow.request.path.startswith('/like/')):
    f.close()
    ctx.master.shutdown()

