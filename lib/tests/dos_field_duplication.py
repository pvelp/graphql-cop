"""Field duplication tests."""
from lib.utils import graph_query, curlify


def field_duplication(url, proxy, headers, debug_mode):
  """Check for field duplication."""
  res = {
    'result':False,
    'title':'Field Duplication',
    'description':'Queries are allowed with 500 of the same repeated field',
    'impact':'Denial of Service - /' + url.rsplit('/', 1)[-1],
    'severity':'HIGH',
    'color': 'red',
    'curl_verify':''
  }

  duplicated_string = '__typename \n' * 500
  q = 'query cop { ' + duplicated_string + '} '
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

  try:
    res['response'] = gql_response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(gql_response)

  try:
    if gql_response.json()['data']['__typename']:
      res['result'] = True
  except:
    pass

  return res
