# BugFetcher
定时自动从禅道获取到指给你的bug并发送一条消息到你的飞书机器人
# BugFetcher

## 简介
BugFetcher 是一个定时自动从禅道获取指派给你的未解决的 bug 并发送消息到你的飞书机器人的工具。

## 功能
- 从禅道获取未解决的 bug
- 发送 bug 信息到飞书
- 定时获取新 bug

## 安装
1. 克隆此仓库到本地：
    ```bash
    git clone <repository_url>
    cd BugFetcher
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

## 使用
1. 配置禅道和飞书信息：
    - 启动应用程序：
        ```bash
        python BugFetcher.py
        ```
    - 在应用程序界面中输入禅道 URL(只需要这一部分：https://zentao.example.com, 注意末尾不要有'/')、用户名、密码、飞书 Webhook URL 和获取间隔时间（分钟）。
    - 点击 "Save Config" 按钮保存配置。

2. 登录禅道：
    - 点击 "Login to ZenTao" 按钮登录禅道。
    - 登录成功后，选择一个产品。

3. 开始获取 bug：
    - 点击 "Start Fetching" 按钮开始定时获取 bug 并发送到飞书。

## 文件说明
- `BugFetcher.py`：主程序文件，包含 UI 和逻辑实现。
- `setup.py`：py2app用于打包应用程序的脚本。
- `BugFetcher.spec`：用于 PyInstaller 打包的配置文件。
- `.gitignore`：Git 忽略文件配置。

## 依赖
- `tkinter`：图形用户界面库
- `requests`：HTTP 请求库
- `json`：JSON 处理库
- `datetime`：日期时间处理库
- `threading`：线程处理库
- `os`：操作系统接口模块

## 打包
1. 使用 PyInstaller 打包：
    ```bash
    pyinstaller BugFetcher.spec
    ```

2. 打包完成后，在 `dist` 目录下会生成可执行文件。

## 使用 py2app 打包
1. 安装 py2app：
    ```bash
    pip install py2app
    ```

2. 使用 setup.py 打包：
    ```bash
    python setup.py py2app
    ```

3. 打包完成后，在 `dist` 目录下会生成 `.app` 文件。
    
4. 将生成的 `.app` 文件复制到应用程序目录或其他合适的位置进行分发和使用。


## 注意事项
- 确保禅道和飞书的配置信息正确无误。
- 获取间隔时间建议设置为 60 分钟以上，以避免频繁请求导致的服务器压力。

## 许可证
此项目使用 MIT 许可证，详情请参阅 LICENSE 文件。
