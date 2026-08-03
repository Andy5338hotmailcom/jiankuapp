import webview
import os

if __name__ == '__main__':
    html_path = os.path.join(os.path.dirname(__file__), 'start.html')
    # 持久化目录
    appdata = os.getenv("APPDATA")
    storage_dir = os.path.join(appdata, r"wg\jiankuapp\cookie")
    os.makedirs(storage_dir, exist_ok=True)

    # 创建窗口
    webview.create_window(
        title='简库资源网',
        url=html_path,
        width=800,
        height=600
    )

    # 关键：private_mode=False 关闭隐私模式，启用持久存储
    webview.start(
        storage_path=storage_dir,
        private_mode=False
    )
