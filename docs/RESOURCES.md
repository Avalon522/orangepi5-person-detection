# 资源清单与来源

## 核心上游
- RKNN Toolkit2 / Lite2 v2.3.0：https://github.com/airockchip/rknn-toolkit2/tree/v2.3.0
- RKNN Model Zoo v2.3.0 YOLOv8：https://github.com/airockchip/rknn_model_zoo/tree/v2.3.0/examples/yolov8
- 官方适配 YOLOv8 源码：https://github.com/airockchip/ultralytics_yolov8
- ONNX 1.16.1：https://github.com/onnx/onnx/tree/v1.16.1
- Orange Pi 官方资料入口：http://www.orangepi.org/

转换脚本来自 Model Zoo，按其 Apache-2.0 许可保留上游许可文件。板端位置解码流程参考该示例并用 NumPy 实现。YOLO 上游仓库包含 AGPL-3.0 许可，模型与厂商运行库应按各自许可使用；不要将整个模型工具链概括为单一宽松许可。

## 模型
模型本地完整资料包保留，公开仓库提供来源、转换方式和哈希，不重复分发权重。参见 models/README.md。

## 原始资料
用户提供的《Orange Pi 5 YOLO 人员检测与电脑端报警实施方案》与《OrangePi 5 RK3588S 用户手册 v2.2》保存在本地资料包的原始资料目录，不上传公开仓库。

## 不收录内容
账号密码、SSH 私钥、真实报警截图与人员照片、原始 alerts.jsonl、虚拟环境、运行缓存和个人网络地址。可再生成的依赖通过锁定清单恢复。
