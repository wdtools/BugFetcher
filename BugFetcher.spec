# -*- mode: python ; coding: utf-8 -*-  # 指定文件编码为utf-8

block_cipher = None  # 加密块设置为None

a = Analysis(
    ['BugFetcher.py'],  # 要分析的主脚本
    pathex=['.', '/opt/homebrew/lib/python3.12/site-packages'],  # 脚本路径，添加site-packages路径
    binaries=[],  # 二进制文件
    datas=[],  # 数据文件
    hiddenimports=[  # 隐藏导入的模块
        'requests',  # HTTP请求库
        'json',  # JSON处理库
        'datetime',  # 日期时间处理库
        'threading',  # 线程处理库
        'os',  # 操作系统接口模块
        'tkinter',  # 图形用户界面库
        'tkinter.messagebox'  # Tkinter消息框模块
    ],  # 添加所有必要的模块
    hookspath=[],  # 钩子路径
    hooksconfig={},  # 钩子配置
    runtime_hooks=[],  # 运行时钩子
    excludes=[],  # 排除的模块
    win_no_prefer_redirects=False,  # Windows不优先重定向
    win_private_assemblies=False,  # Windows私有程序集
    cipher=block_cipher,  # 加密块
    noarchive=False,  # 不使用归档
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # 创建PYZ归档

exe = EXE(
    pyz,  # 使用的PYZ归档
    a.scripts,  # 脚本
    [],  # 额外的二进制文件
    exclude_binaries=True,  # 排除二进制文件
    name='BugFetcher',  # 可执行文件名称
    debug=False,  # 调试模式
    bootloader_ignore_signals=False,  # 引导程序忽略信号
    strip=False,  # 不剥离符号
    upx=True,  # 使用UPX压缩
    upx_exclude=[],  # 排除UPX压缩的文件
    runtime_tmpdir=None,  # 运行时临时目录
    console=False,  # 不使用控制台
    target_arch='arm64',  # 指定目标架构为arm64
)

coll = COLLECT(
    exe,  # 可执行文件
    a.binaries,  # 二进制文件
    a.zipfiles,  # ZIP文件
    a.datas,  # 数据文件
    strip=False,  # 不剥离符号
    upx=True,  # 使用UPX压缩
    upx_exclude=[],  # 排除UPX压缩的文件
    name='BugFetcher'  # 收集的名称
)
