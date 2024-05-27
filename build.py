import PyInstaller.__main__

if __name__ == "__main__":
    PyInstaller.__main__.run([
        'main.py',  # 要打包的 Python 脚本文件名
        '--onefile',  # 打包为单个 .exe 文件
        '--console',  # 隐藏控制台窗口
        '--clean',    # 优化代码
        '--exclude-module', 'pyinstaller',  # 排除某些模块
        '--upx-dir', 'E:\\download\\edge\\upx-4.2.4-win64\\upx-4.2.4-win64'  # UPX 工具的路径
    ])
