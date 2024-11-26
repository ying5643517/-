import requests
import base64

data = [
  ('3k', "https://3k.fxxk.dedyn.io/auto"),
  ('king361', 'https://king361.fxxk.dedyn.io/auto'),
  ('comorg', 'https://alvless.comorg.us.kg/TCorg'),
  ('Moist_R', 'https://owo.o00o.ooo/ooo'),
  ('durl', 'https://vless.durl.nyc.mn/zrf')
]

def get_nodes(file: str, url: str) -> None:
  try:
    with requests.get(url, timeout=10) as response:
      if response.status_code < 300:
        print(response.status_code, url, 'successfully')
        text = base64.b64decode(response.text).decode('utf-8')
        # print(text[:500])
        with open(f'cf_sub/{file}', mode="w+", encoding='utf-8') as f:
          f.write(text)
      else:
        print('状态码错误：', response.status_code)
  except Exception as e:
    print(e.args)
    get_nodes(file, url)


if __name__ == '__main__':
  for it in data:
    # print(it)
    get_nodes(*it)