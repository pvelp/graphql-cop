"""Collect GraphiQL details."""
from json import JSONDecodeError

from lib.utils import request, curlify

def detect_graphiql(url, proxy, headers, debug_mode):
  """Get GraphiQL."""
  res = {
    'result':False,
    'title':'GraphQL IDE',
    'description':'GraphiQL Explorer/Playground Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'LOW',
    'color': 'blue',
    'curl_verify':'',
    'response': ''
  }

  heuristics = ('graphiql.min.css', 'GraphQL Playground', 'GraphiQL', 'graphql-playground')

  if "Accept" in headers.keys():
    backup_accept_header=headers["Accept"]
  headers["Accept"]= "text/html"
  if debug_mode:
      headers['X-GraphQL-Cop-Test'] = res['title']
  response = request(url, proxies=proxy, headers=headers)
  try:
    res['response'] = response.json()
  except Exception as e:
    print(e)

  res['curl_verify'] = curlify(response)
  try:
    if response and any(word in response.text for word in heuristics):
      res['result'] = True
  except:
      pass

  del headers["Accept"]
  if 'backup_accept_header' in locals():
    headers["Accept"]=backup_accept_header

  return res
