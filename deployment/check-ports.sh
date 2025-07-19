#!/bin/bash
echo "🔍 监听中的TCP/UDP端口："
sudo ss -tulwn | awk 'NR>1 {
  split($5, a, ":");
  proto = tolower($1);
  if (a[2] ~ /^[0-9]+$/) {
    port = a[2];
    printf "%-5s %-6s", proto, port;
    system("sudo lsof -i :" port " -sTCP:LISTEN -P -n | awk \"NR==2 {printf \\\"%-20s %s\\\",\\$1,\\$9}\"");
    print ""
  }
}'
echo "✅ 检测完成 (需要sudo权限)"