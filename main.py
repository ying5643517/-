import os
import re
from sys import argv
import requests
import base64
import urllib.parse

headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

class Main:
  paths = [
    "tolinkshare2",
    "abshare",
    "mksshare"
  ]
  dirs = ['v2ray', 'ios', 'clash']
  sub_links = {}

  def __init__(self) -> None:
    self.submodule_path = self.paths[0]

  def add_suffix(self, line: str) -> str:
    if line.strip() == "":
      return line
    # 提取备注
    # 去掉 ss:// 前缀
    ss_content = line[5:]
    # 进行 Base64 解码，添加必要的填充
    base64_str = ss_content.split('@')[0]
    padding = len(base64_str) % 4
    if padding != 0:
      base64_str += '=' * (4 - padding)

    try:
      # 进行 Base64 解码
      decoded_bytes = base64.b64decode(base64_str)
      decoded_string = decoded_bytes.decode('utf-8')

      # 提取加密方式和密码
      server, port_with_remark = ss_content.split('@')[1].split(':', 1)
      method, password = decoded_string.split(':')
      port, remark = port_with_remark.split('#')
      remark = urllib.parse.unquote(remark)
      if '|' not in remark:
        return ""
      cleaned_remark = re.sub(r' \|.*', f'_{self.submodule_path}', remark)
      return f'ss://{base64.b64encode(f"{method}:{password}".encode()).decode()}@{server}:{port}#{urllib.parse.quote(cleaned_remark)}'
    except Exception as e:
      print(e.args)
      return line

  def parse_origin(self, text: str) -> str:
    decoded_bytes = base64.b64decode(text)
    decoded_string = decoded_bytes.decode('utf-8')
    return "\n".join([self.add_suffix(line) for line in decoded_string.split('\n')])

  def get_item_link(self, key: str, url: str):
    try:
      url = re.sub(r'https?:/', 'https://', url) if re.match(r'https:/[^/]', url) else url
      with requests.get(url, headers=headers, timeout=10) as res:
        print(res.status_code, url)
        if res.status_code < 300:
          os.makedirs(key, exist_ok=True)
          with open(f"{key}/{self.submodule_path}.{key}", mode="w+", encoding="utf-8") as f:
            f.write(self.parse_origin(res.text))
    except:
      self.get_item_link(key, url)

  def request_links(self):
    items = self.sub_links.items()
    if len(items) != 3:
      return

    for key, url in items:
      self.get_item_link(key, url)

  def set_links(self):
    with open(f"{self.submodule_path}/README.md", mode="r", encoding="utf-8") as f:
      text = f.read()
      res = re.search(
        r".*?Clash订阅.*?(?P<clash>http.*?)\n"
        r".*?v2rayN订阅.*?(?P<v2ray>http.*?)\n"
        r".*?iOS小火箭订阅.*?(?P<ios>http.*?)\n.*?",
        text,
        re.DOTALL
      )
      self.sub_links = res.groupdict()
      
  def walk(self, p: str):
    if self.submodule_path in self.paths:
      self.set_links()
      self.request_links()
    if p == 'all':
      for it in self.paths:
        self.submodule_path = it
        self.set_links()
        self.request_links()

    for d in self.dirs:
      sites = ""
      for key in self.paths:
        with open(f'{d}/{key}.{d}', mode="r", encoding="utf-8") as f:
          sites += (f.read().strip() + '\n')
      encoded = base64.b64encode(sites.encode('utf-8')).decode('utf-8')
      with open(f"{d}/index", mode="w+", encoding="utf-8") as f:
        f.write(encoded)


if __name__ == '__main__':
  Main().walk(argv[1])