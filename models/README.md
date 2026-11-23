# 模型获取与转换

官方 ONNX 下载地址：
https://ftrg.zbox.filez.com/v2/delivery/data/95f00b0fc900458ba134f8b180b3f7a1/examples/yolov8/yolov8n.onnx

|文件|SHA256|
|---|---|
|yolov8n.onnx|0c8716701f471067932b797eeb67c8e5db47c693c2557c881d7679ec12e21bc5|
|yolov8n_rk3588_fp.rknn|bf3e642cea9ef902d81408b375bad575b566031ec67709cca4205d564dfe5df7|

在 WSL Ubuntu 22.04 / Python 3.10 环境：
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r conversion/requirements-lock.txt
python -m pip check
python conversion/convert.py models/yolov8n.onnx rk3588 fp models/yolov8n_rk3588_fp.rknn
sha256sum models/*.rknn
```
fp 表示不进行 INT8 量化。上游脚本含校准数据集路径，仅量化构建需要，当前复刻采用 fp。不同环境再转换的二进制哈希可能不同，需板端推理验证。
