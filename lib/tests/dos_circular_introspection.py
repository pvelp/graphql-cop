"""Perform Circular Query based on Introspection."""
from lib.utils import graph_query, curlify

def circular_query_introspection(url, proxy, headers, debug_mode):
  """Run a Circular Query using introspection."""
  res = {
    'result':False,
    'title':'Introspection-based Circular Query',
    'description':'Circular-query using Introspection',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'color': 'red',
    'curl_verify':''
  }

  q = 'query cop { __schema { types { fields { type { fields { type { fields { type { fields { type { name } } } } } } } } } } }'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)
  try:
    if len(gql_response.json()['data']['__schema']['types']) > 25:
      res['result'] = True
  except:
    pass

  return res
