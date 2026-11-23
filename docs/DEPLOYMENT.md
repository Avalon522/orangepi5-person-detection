# 部署与日常启动

## 开发板
采用已验证的 Orange Pi Ubuntu 22.04 镜像，先验证相机与 NPU，勿盲目替换驱动。实际环境 Runtime/Lite2 2.3.0、驱动 0.9.8。

将 board 目录中的正式 Python 文件放到 `~/orangepi_person_detection/`，将 RKNN 文件放到其 models 子目录。
```bash
sudo apt install python3-venv python3-opencv python3-numpy v4l-utils
cd ~/orangepi_person_detection
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install 'numpy<2' 'rknn-toolkit-lite2==2.3.0'
ALARM_SERVER_URL=http://电脑局域网IP:8000 python -u main.py
```
摄像头使用 /dev/video0；实际节点需 v4l2-ctl 核实。默认 NPU 核心 0，输入 640×640，摄像头 640×480。

## Windows
安装 Python（实际使用 3.13.5），接收服务仅依赖标准库。将 pc_receiver 文件夹放到方便的位置。复制 config.example.json 为 config.local.json，填写开发板 IP、电脑 IP、Python 可执行文件路径。config.local.json 不提交 Git。

双击 Start-Monitor.cmd 自动启动电脑服务、浏览器并 SSH 到开发板运行 main.py，按提示输入开发板 SSH 密码。需已安装 Windows OpenSSH 客户端，两端接同一路由器，允许可信局域网的 TCP 8000。

脚本假设开发板账号为 orangepi、项目位于 /home/orangepi/orangepi_person_detection，修改账号或目录时同步修改启动脚本。flock 防止由该入口重复启动，旧手动进程需先停止。

## 手动启动电脑服务
```powershell
$env:MONITOR_HOST = "电脑局域网IP"
python server.py
```
浏览器打开 http://电脑局域网IP:8000。直接启动且没有设置 MONITOR_HOST 时，只监听本机回环地址，开发板无法访问，这是公开版本避免误绑定的默认值。

## 停止与重启
先在检测窗口 Ctrl+C，再停止接收窗口；需关机时在开发板 sudo poweroff 后断电。不需要启动 WSL；WSL 仅用于模型转换。运行期间保持 SSH 与电脑服务窗口开启、电脑不睡眠。没有开机自启、Windows 服务或 systemd 托管。IP 建议在路由器 DHCP 中保留。

## 首次验收
无人时画面持续变化；人员出现后状态变红；同一次停留只新增一次历史；离开后状态变白；再次进入生成新事件；断开设备状态应变未知。网络阻塞可能影响 FPS。30 分钟连续运行已获用户确认正常，更长时间运行可按需测试。
