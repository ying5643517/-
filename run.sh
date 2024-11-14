#!/bin/bash

# modules=("abshare" "mksshare" "tolinkshare2")
modules=($(cat "sites.txt"))
echo "${modules[@]}"
updated_submodules=()

for sub in "${modules[@]}"; do
  # 进入子仓库目录
  cd "$sub.github.io" || continue
  echo "check $sub"
  
  # 获取本地和远程的 commit ID
  git fetch
  localCommit=$(git rev-parse HEAD)
  remoteCommit=$(git rev-parse origin/main)
  
  # 比较两个 commit
  if [ "$localCommit" != "$remoteCommit" ]; then
    git fetch origin
    git reset --hard origin/main
    echo "$sub has updates."
    updated_submodules+=("$sub")
  fi

  # 返回上一层目录
  cd ..
done

# 检查是否有更新的子模块
if [ ${#updated_submodules[@]} -gt 0 ]; then
  for sub in "${updated_submodules[@]}"; do
    # 调用 Python 脚本处理子模块
    python3 main.py "$sub"
  done

  # 添加所有更改
  git add .

  # 设置时区并获取当前时间（设置为中国标准时间）
  currentDateTime=$(TZ="Asia/Shanghai" date +"%Y-%m-%d %H:%M:%S")

  # 提交更改
  git commit -m "update node from ${updated_submodules[*]} at $currentDateTime"
  
  currentBranch=$(git rev-parse --abbrev-ref HEAD)
  if [ "$currentBranch" == "main" ]; then
    git push --force
  else
    echo "Current branch is not 'main', skipping push."
  fi
fi
