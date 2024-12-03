from typing import Optional, Literal
import os

KeyType = Optional[Literal['ios', 'v2ray', 'clash']]

module_sites = []
sub_dir = "sub"

with open("./sites.txt", encoding="utf-8", mode="r") as f:
  module_sites = f.read().strip().split(' ')

dir_list = os.listdir(sub_dir)

headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
