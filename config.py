#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件模块
用于存储微信公众号相关配置
"""

import os

# 微信公众号配置
# 请将以下配置替换为实际的微信公众号信息
WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'your_wechat_app_id')  # 微信公众号AppID
WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', 'your_wechat_app_secret')  # 微信公众号AppSecret

# 其他配置
START_DAY = "20250101"  # 开始日期
END_DAY = "current"     # 结束日期

# 日志配置
LOG_FILE = 'xwlb.log'
LOG_LEVEL = 'INFO'

# 数据文件配置
DATA_DIR = 'data'
KEY_NAME_FILE = "key_name.json"
KEY_PLACE_FILE = "key_place.json" 
KEY_WORDS_FILE = "key_words.json"

# 图片文件配置
IMAGE_DIR = 'images'
NAME_CLOUD_FILE = "name_cloud.png"
PLACE_CLOUD_FILE = "place_cloud.png" 
WORDS_CLOUD_FILE = "words_cloud.png"

def validate_config():
    """验证配置是否有效"""
    errors = []
    
    if WECHAT_APP_ID == 'your_wechat_app_id' or not WECHAT_APP_ID:
        errors.append("请设置有效的微信公众号AppID")
    
    if WECHAT_APP_SECRET == 'your_wechat_app_secret' or not WECHAT_APP_SECRET:
        errors.append("请设置有效的微信公众号AppSecret")
    
    return errors

def print_config_info():
    """打印配置信息（隐藏敏感信息）"""
    print("=== 配置信息 ===")
    print(f"微信公众号AppID: {WECHAT_APP_ID[:8]}..." if len(WECHAT_APP_ID) > 8 else f"微信公众号AppID: {WECHAT_APP_ID}")
    print(f"微信公众号AppSecret: {'*' * len(WECHAT_APP_SECRET)}")
    print(f"开始日期: {START_DAY}")
    print(f"结束日期: {END_DAY}")
    print("================")

if __name__ == "__main__":
    print_config_info()
    errors = validate_config()
    if errors:
        print("配置错误:")
        for error in errors:
            print(f"- {error}")
    else:
        print("配置验证通过")