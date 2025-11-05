import requests
import base64
import logging
import json
import time

# 配置日志记录
logging.basicConfig(filename='xwlb.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeChatOfficialAccount:
    """微信公众号API封装类"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire_time = 0
    
    def get_access_token(self):
        """获取微信公众号access_token"""
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            response = requests.get(url, params=params)
            result = response.json()
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                self.token_expire_time = time.time() + result.get("expires_in", 7200) - 300  # 提前5分钟刷新
                logging.info("微信公众号access_token获取成功")
                return self.access_token
            else:
                logging.error(f"获取access_token失败: {result}")
                return None
        except Exception as e:
            logging.error(f"获取access_token异常: {str(e)}")
            return None
    
    def upload_image(self, image_path):
        """上传图片到微信公众号素材库"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = "https://api.weixin.qq.com/cgi-bin/media/upload"
        params = {
            "access_token": access_token,
            "type": "image"
        }
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files)
                result = response.json()
                
                if "media_id" in result:
                    logging.info(f"图片上传成功，media_id: {result['media_id']}")
                    return result["media_id"]
                else:
                    logging.error(f"图片上传失败: {result}")
                    return None
        except Exception as e:
            logging.error(f"图片上传异常: {str(e)}")
            return None
    
    def create_draft(self, title, content, author="新闻联播", digest=""):
        """创建图文草稿"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        
        # 构建图文消息内容
        article = {
            "title": title,
            "author": author,
            "digest": digest if digest else content[:100] + "...",
            "content": content,
            "content_source_url": "",
            "thumb_media_id": ""  # 如果需要缩略图，需要先上传图片获取media_id
        }
        
        data = {
            "articles": [article]
        }
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            if "media_id" in result:
                logging.info(f"草稿创建成功，media_id: {result['media_id']}")
                return result["media_id"]
            else:
                logging.error(f"草稿创建失败: {result}")
                return None
        except Exception as e:
            logging.error(f"草稿创建异常: {str(e)}")
            return None
    
    def publish_draft(self, media_id):
        """发布草稿"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
        
        data = {
            "media_id": media_id
        }
        
        try:
            response = requests.post(url, json=data)
            result = response.json()
            
            if result.get("errcode") == 0:
                logging.info("文章发布成功")
                return True
            else:
                logging.error(f"文章发布失败: {result}")
                return False
        except Exception as e:
            logging.error(f"文章发布异常: {str(e)}")
            return False

def send_wechat_article(title, content, app_id, app_secret, author="新闻联播"):
    """发送文章到微信公众号"""
    wechat = WeChatOfficialAccount(app_id, app_secret)
    
    # 创建草稿
    media_id = wechat.create_draft(title, content, author)
    if not media_id:
        return {"success": False, "message": "草稿创建失败"}
    
    # 发布草稿
    if wechat.publish_draft(media_id):
        return {"success": True, "message": "文章发布成功", "media_id": media_id}
    else:
        return {"success": False, "message": "文章发布失败"}

def get_wechat_subscribers(app_id, app_secret):
    """获取微信公众号关注用户列表（需要用户授权）"""
    wechat = WeChatOfficialAccount(app_id, app_secret)
    access_token = wechat.get_access_token()
    if not access_token:
        return {"success": False, "message": "获取access_token失败"}
    
    # 注意：获取用户列表需要用户授权，这里返回空列表作为示例
    # 实际使用时需要通过网页授权获取用户openid
    return {"success": True, "data": [], "message": "需要用户授权获取关注用户列表"}

def upload_image_to_wechat(image_path, app_id, app_secret):
    """上传图片到微信公众号素材库"""
    wechat = WeChatOfficialAccount(app_id, app_secret)
    
    media_id = wechat.upload_image(image_path)
    if media_id:
        return {"success": True, "media_id": media_id, "message": "图片上传成功"}
    else:
        return {"success": False, "message": "图片上传失败"}

def send_wechat_image(image_path, app_id, app_secret, title="新闻联播图片"):
    """发送图片到微信公众号素材库"""
    wechat = WeChatOfficialAccount(app_id, app_secret)
    
    # 上传图片到素材库
    media_id = wechat.upload_image(image_path)
    if not media_id:
        return {"success": False, "message": "图片上传失败"}
    
    # 创建包含图片的图文消息
    content = f"""
    <p><strong>{title}</strong></p>
    <p><img src="{{media_id}}" alt="{title}" /></p>
    <p>图片已成功上传到微信公众号素材库</p>
    """
    
    # 创建草稿
    draft_media_id = wechat.create_draft(title, content)
    if not draft_media_id:
        return {"success": False, "message": "图文草稿创建失败"}
    
    # 发布草稿
    if wechat.publish_draft(draft_media_id):
        return {"success": True, "message": "图片文章发布成功", "media_id": media_id, "draft_media_id": draft_media_id}
    else:
        return {"success": False, "message": "图片文章发布失败"}

if __name__ == "__main__":
    APP_TOKEN = "AT_yqnyoG262pwdmA6esDdvyp804v74jsrK"  # xwlb专用 APP_TOKEN
    USER_UIDS = ["UID_wKraNNh5OPgSq2kP0neChHsNC3Sd"]
    send_wxpusher_image("place_cloud.png", USER_UIDS, APP_TOKEN, [39053], "wordcloud")