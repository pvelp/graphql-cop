"""Collect trace mode details."""
from lib.utils import graph_query, curlify


def unhandled_error_detection(url, proxy, headers, debug_mode):
  """Get unhandled errors."""
  res = {
    'result':False,
    'title':'Unhandled Errors Detection',
    'description':'Exception errors are not handled',
    'impact':'Information Leakage - /' + url.rsplit('/', 1)[-1],
    'severity':'INFO',
    'color': 'green',
    'curl_verify':'',
    'response': ''
  }

  q = 'qwerty cop { abc }'

  try:
    if debug_mode:
      headers['X-GraphQL-Cop-Test'] = res['title']
    gql_response = graph_query(url, proxies=proxy, headers=headers, payload=q)

    try:
      res['response'] = gql_response.json()
    except Exception as e:
      print(e)
    res['curl_verify'] = curlify(gql_response)
    if gql_response.json()['errors'][0]['extensions']['exception']:
      res['result'] = True
    elif '\'extensions\': {\'exception\':' in str(gql_response.json()).lower():
      res['result'] = True
  except:
    pass

  return res
