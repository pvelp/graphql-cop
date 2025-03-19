"""Batch tests."""
from lib.utils import graph_query, curlify


def batch_query(url, proxy, headers, debug_mode):
  """Check for batch queries."""
  res = {
    'result':False,
    'title':'Array-based Query Batching',
    'description':'Batch queries allowed with 10+ simultaneous queries',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'color': 'red',
    'curl_verify':''
  }

  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload='query cop { __typename }', batch=True)

  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)
  
  try:
      if len(gql_response.json()) >= 10:
        res['result'] = True
  except:
    pass

  return res
