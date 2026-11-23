# 接口与排错

## 接口
- GET /：网页。
- GET /api/status：当前人数、接收时间、online；约 6 秒未更新为离线。
- POST /api/frame：JPEG 请求体，X-Person-Count 请求头。更新内存画面和人数，不写历史。
- GET /live.mjpg：MJPEG 最新画面流，慢客户端可能跳过中间帧。
- POST /api/alert：JSON；device_id、event_time、person_count、max_confidence、image_base64、test。保存进入截图与 JSONL。
- GET /api/events：最近 100 条历史，倒序。
- GET /images/<id>.jpg：历史截图。

## 排错
1. SSH 无法连接：确认开发板通电、IP、路由器、TCP 22，不把 VPN 地址当局域网地址。
2. HTTP 超时：确认服务窗口、地址、防火墙；只允许可信局域网所需端口，不关闭整个防火墙。
3. onnx.mapping 错误：转换环境固定 onnx==1.16.1，并使用锁定清单。
4. RKNN 静态形状动态范围查询警告：若 init_runtime 为 0 且推理成功，此提示可忽略。
5. 没有摄像头：v4l2-ctl --list-devices；确认 video0 是 Video Capture，避免多程序抢占。
6. 页面旧布局：Ctrl+F5；确认启动的是对应目录的 server.py。
7. 有框但无报警：画框阈值 0.25，进入事件阈值 0.5 且需要连续 3 帧。
8. 内存持续增长、延迟变大：暂停长期运行，记录负载、RSS、网络速度；用户已确认 30 分钟测试正常，仍应定位新出现的问题。
