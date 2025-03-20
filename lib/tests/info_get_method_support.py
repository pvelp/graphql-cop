"""Collect all supported methods."""
from lib.utils import request, curlify


def get_method_support(url, proxies, headers, debug_mode):
  """Get the supported methods."""
  res = {
    'result':False,
    'title':'GET Method Query Support',
    'description':'GraphQL queries allowed using the GET method',
    'impact':'Possible Cross Site Request Forgery (CSRF) - /' + url.rsplit('/', 1)[-1],
    'severity':'MEDIUM',
    'color': 'yellow',
    'curl_verify':'',
    'response': ''
  }

  q = 'query cop {__typename}'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  response = request(url, proxies=proxies, headers=headers, params={'query':q})
  try:
    res['response'] = response.json()
  except Exception as e:
    print(e)
  res['curl_verify'] = curlify(response)

  try:
    if response and response.json()['data']['__typename']:
      res['result'] = True
  except:
      pass

  return res
