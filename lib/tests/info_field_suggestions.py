"""Field suggestions tests."""
from lib.utils import graph_query, get_error, curlify


def field_suggestions(url, proxy, headers, debug_mode):
  """Retrieve field suggestions."""
  res = {
    'result':False,
    'title':'Field Suggestions',
    'description':'Field Suggestions are Enabled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'LOW',
    'color': 'blue',
    'curl_verify':''
  }

  q = 'query cop { __schema { directive } }'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)

  try:
    if 'Did you mean' in get_error(gql_response.json()):
      res['result'] = True
  except:
    pass

  return res
