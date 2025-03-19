"""Perform introspection tests."""
from lib.utils import graph_query, curlify


def introspection(url, proxy, headers, debug_mode):
  """Run introspection."""
  res = {
    'result':False,
    'title':'Introspection',
    'description':'Introspection Query Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'color': 'red',
    'curl_verify':''
  }

  q = 'query cop { __schema { types { name fields { name } } } }'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)
  try:
    if gql_response.json()['data']['__schema']['types']:
      res['result'] = True
  except:
    pass

  return res
