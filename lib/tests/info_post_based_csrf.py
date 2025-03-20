"""Checks if queries are allowed over POST not in JSON."""
from lib.utils import request, curlify


def post_based_csrf(url, proxies, headers, debug_mode):
  res = {
    'result':False,
    'title':'POST based url-encoded query (possible CSRF)',
    'description':'GraphQL accepts non-JSON queries over POST',
    'impact':'Possible Cross Site Request Forgery - /' + url.rsplit('/', 1)[-1],
    'severity':'MEDIUM',
    'color': 'yellow',
    'curl_verify':'',
    'response': ''
  }

  q = 'query cop { __typename }'
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = res['title']
  response = request(url, proxies=proxies, headers=headers, data={'query': q}, verb='POST')
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
