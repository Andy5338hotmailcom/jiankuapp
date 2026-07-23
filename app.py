import webview
import os

# 核心：加载同目录下的index.html（外部文件）
if __name__ == '__main__':
    # 获取index.html的绝对路径（确保能找到同目录的外部HTML）
    html_path = os.path.join(os.path.dirname(__file__), 'start.html')
    
    # 创建窗口并加载外部HTML文件
    webview.create_window(
        title='简库资源网',
        url=html_path,  # 关键：加载外部HTML文件，而非字符串
        width=800,
        height=600
    )
    webview.start()