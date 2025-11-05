import logging
import xwlb
import contextBrief
import jsonFile
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import wxPusher
import contextAnalyze
import config

# 配置日志记录器
logging.basicConfig(filename=config.LOG_FILE, level=getattr(logging, config.LOG_LEVEL), format='%(asctime)s - %(levelname)s - %(message)s')

# 从配置文件获取参数
start_day = config.START_DAY
end_day = config.END_DAY
WECHAT_APP_ID = config.WECHAT_APP_ID
WECHAT_APP_SECRET = config.WECHAT_APP_SECRET
# 创建一个锁对象
lock = threading.Lock()


def join_list_with_newline(items):
    """
    将列表中的每个元素拼接成一个字符串，每个元素之间由换行符连接。
    如果元素是列表，则递归处理。
    
    :param items: 包含字符串或列表的列表
    :return: 拼接后的字符串
    """
    result = []
    for item in items:
        if isinstance(item, list):
            result.append(join_list_with_newline(item))
        else:
            result.append(item)
    return "\n".join(result)


def process_xwlb(date_str):
    # 获取新闻联播的 URL
    url = xwlb.get_xwlb_url_byDate(date_str)
    if url:
        # 获取新闻联播的内容摘要
        result = xwlb.get_xwlb_contextBrief(url)
        
        # 解析结构化文本
        structured_text = contextBrief.parse_structured_text(result)
        
        # 保存到 JSON 文件时加锁
        with lock:
            jsonFile.save_to_json(structured_text, date_str)
    else:
        logging.info(f"无法获取新闻联播URL，日期: {date_str}")


def is_start_of_month():
    """
    判断当前日期是否是月初。
    
    :return: 如果是月初返回 True，否则返回 False
    """
    today = datetime.now()
    return today.day == 1

def get_last_month_date_range():
    today = datetime.now()
    last_month_last_day = today.replace(day=1) - timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)
    return last_month_first_day, last_month_last_day

def perform_keyword_analysis_and_send_images(app_id, app_secret, input_files, image_filenames):
    logging.info("今天是月初，进行关键字分析总结")
    contextAnalyze.analyze_json_file()
    last_month_first_day, last_month_last_day = get_last_month_date_range()

    # 获取当前月份信息
    current_month = last_month_first_day.strftime("%Y%m")
    
    keyword_counts_list = []
    for input_file, image_filename in zip(input_files, image_filenames):
        # 修改图片名称，添加月份信息
        image_filename_with_month = f"{image_filename.split('.')[0]}_{current_month}.png"
        titleName = {"name_cloud.png": "关键人名", "place_cloud.png": "关键地点", "words_cloud.png": "关键词"}
        
        keyword_counts = contextAnalyze.count_keywords_in_period(
            input_file=input_file, 
            start_date=last_month_first_day.strftime("%Y%m%d"), 
            end_date=last_month_last_day.strftime("%Y%m%d")
        )
        keyword_counts_list.append(keyword_counts)
        try:
            contextAnalyze.plot_wordcloud(keyword_counts, image_filename_with_month)
            # 使用微信公众号API发送图片
            result = wxPusher.send_wechat_image(image_filename_with_month, app_id, app_secret, current_month + titleName[image_filename])
            if result["success"]:
                logging.info(f"图片文章发布成功: {image_filename_with_month}")
            else:
                logging.error(f"图片文章发布失败: {result['message']}")
        except Exception as e:
            logging.info(f"生成或推送图片异常：{str(e) + image_filename_with_month}")


if __name__ == "__main__":
    # 记录程序开始时间
    start_time = datetime.now()
    logging.info(f"程序开始时间: {start_time}")
    
    # 将开始日期和结束日期转换为 datetime 对象
    start_date = datetime.strptime(start_day, "%Y%m%d")
    if end_day == "current":
        current_hour = datetime.now().hour
        if current_hour > 22:
            end_day = datetime.now().strftime("%Y%m%d")
        else:
            end_day = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    end_date = datetime.strptime(end_day, "%Y%m%d")
    
    current_date = start_date
    
    dates = []
    while current_date <= end_date:
        # 将当前日期转换为字符串格式 "YYYYMMDD"
        date_str = current_date.strftime("%Y%m%d")
        dates.append(date_str)
        # 递增一天
        current_date += timedelta(days=1)
    
    # 使用线程池来并行处理每个日期
    with ThreadPoolExecutor() as executor:
        future_to_date = {executor.submit(process_xwlb, date_str): date_str for date_str in dates}
        for future in as_completed(future_to_date):
            date_str = future_to_date[future]
            try:
                future.result()
            except Exception as exc:
                logging.error(f'{date_str} generated an exception: {exc}')
    
    # 记录程序结束时间
    end_time = datetime.now()
    logging.info(f"程序结束时间: {end_time}")
    
    # 计算并打印程序运行时间
    elapsed_time = end_time - start_time
    logging.info(f"程序运行总时间: {elapsed_time}")

    readNews = jsonFile.load_from_json(end_day)
    # 新增：将readNews列表中的每个元素拼接成一个字符串
    readNews_str = join_list_with_newline(readNews)
    
    # 使用微信公众号API发送文章
    title = f"{end_day}新闻联播内容"
    result = wxPusher.send_wechat_article(title, readNews_str, WECHAT_APP_ID, WECHAT_APP_SECRET)
    if result["success"]:
        logging.info(f"文章发布成功: {title}")
    else:
        logging.error(f"文章发布失败: {result['message']}")

    # 每个月初进行一次关键字分析总结
    if is_start_of_month():
        input_files = [config.KEY_NAME_FILE, config.KEY_PLACE_FILE, config.KEY_WORDS_FILE]
        image_filenames = [config.NAME_CLOUD_FILE, config.PLACE_CLOUD_FILE, config.WORDS_CLOUD_FILE]
        perform_keyword_analysis_and_send_images(WECHAT_APP_ID, WECHAT_APP_SECRET, input_files, image_filenames)
