import os
import shutil
import subprocess
from pathlib import Path

def package_health_tracker():
    """将健康追踪应用打包为独立的Windows可执行文件"""
    # 确保打包工具已安装
    try:
        import pyinstaller
    except ImportError:
        print("正在安装pyinstaller...")
        subprocess.check_call(["pip", "install", "pyinstaller"])
    
    # 确保应用依赖已安装
    print("正在安装应用依赖...")
    subprocess.check_call(["pip", "install", "tkcalendar"])
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # 应用主文件名称（确保与你的脚本文件名一致）
    app_script = "health_tracker_app.py"
    app_script_path = current_dir / app_script
    
    # 检查主文件是否存在
    if not app_script_path.exists():
        print(f"错误：未找到应用主文件 {app_script}")
        print("请确保此打包脚本与应用主文件在同一目录下")
        return
    
    # 清理之前的打包文件
    for folder in ["build", "dist", "__pycache__"]:
        folder_path = current_dir / folder
        if folder_path.exists():
            print(f"清理目录: {folder_path}")
            shutil.rmtree(folder_path, ignore_errors=True)
    
    # 打包命令
    # -F: 打包成单个文件
    # -w: 不显示控制台窗口
    # --name: 应用名称
    # --add-data: 添加必要的数据文件（如果有的话）
    print("开始打包应用...")
    command = [
        "pyinstaller",
        "-F",
        "-w",
        "--name", "健康追踪应用",
        str(app_script_path)
    ]
    
    try:
        subprocess.check_call(command)
        print("\n打包完成！")
        print(f"可执行文件位置: {current_dir / 'dist' / '健康追踪应用.exe'}")
        print("\n使用说明：")
        print("1. 找到dist文件夹中的'健康追踪应用.exe'")
        print("2. 可以直接运行，或发送给他人")
        print("3. 首次运行可能会有安全提示，选择'更多信息'->'仍要运行'")
        print("4. 数据会保存在与exe同一目录下的health_data.json文件中")
    except Exception as e:
        print(f"打包过程出错: {str(e)}")

if __name__ == "__main__":
    package_health_tracker()
    