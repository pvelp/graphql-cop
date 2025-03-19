"""Directive overloading tests."""
from lib.utils import graph_query, curlify


def directive_overloading(url, proxy, headers, debug_mode):
  """Check for directive overloading."""
  res = {
    'result':False,
    'title':'Directive Overloading',
    'description':'Multiple duplicated directives allowed in a query',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'color': 'red',
    'curl_verify':''
  }

  q = 'query cop { __typename @aa@aa@aa@aa@aa@aa@aa@aa@aa@aa }'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)
  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)

  try:
    if len(gql_response.json()['errors']) == 10:
      res['result'] = True
  except:
    pass

  return res
