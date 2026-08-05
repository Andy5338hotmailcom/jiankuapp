import webview
import os
import sys
from urllib.parse import urlparse
import webbrowser

def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def on_page_loaded(window):
    # 每次页面加载完成自动执行，跳转后新页面也会自动注入
    js_code = r"""
    (function(){
        const allowHosts = ["jiankuapp.com","www.jiankuapp.com","appshop.shaoxiaoj.com"];

        // 1.劫持 window.open()
        const originalOpen = window.open;
        window.open = function(url){
            if(!url) return originalOpen.apply(this, arguments);
            try{
                const u = new URL(url, window.location);
                const host = u.hostname.toLowerCase();
                if(allowHosts.includes(host)){
                    window.location.href = url;
                    return null;
                }else{
                    window.pywebview.api.open_external(url);
                    return null;
                }
            }catch(e){
                window.location.href = url;
                return null;
            }
        };

        // 2.劫持全部 <a target="_blank"> 链接点击
        document.addEventListener('click', function(e){
            let el = e.target.closest('a');
            if(!el) return;
            const target = el.getAttribute('target');
            const href = el.getAttribute('href');
            if(target !== '_blank' || !href) return;

            e.preventDefault();
            try{
                const u = new URL(href, window.location);
                const host = u.hostname.toLowerCase();
                if(allowHosts.includes(host)){
                    window.location.href = href;
                }else{
                    window.pywebview.api.open_external(href);
                }
            }catch(err){
                //相对路径
                window.location.href = href;
            }
        }, true);
    })();
    """
    window.evaluate_js(js_code)


class Api:
    def open_external(self, url):
        webbrowser.open(url)


if __name__ == '__main__':
    base = get_base_dir()
    html_path = os.path.join(base, 'start.html')

    appdata = os.getenv("APPDATA")
    storage_dir = os.path.join(appdata, r"wg\jiankuapp\cookie")
    os.makedirs(storage_dir, exist_ok=True)

    api = Api()
    window = webview.create_window(
        title='简库资源网',
        url=html_path,
        width=800,
        height=600,
        js_api=api
    )

    # ✅每一次页面加载完成（跳转、打开新页面）都会触发，自动注入JS
    window.events.loaded += on_page_loaded

    webview.start(
        private_mode=False,
        storage_path=storage_dir
    )
