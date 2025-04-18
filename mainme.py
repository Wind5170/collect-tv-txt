import urllib.request
from urllib.parse import urlparse
import re  # 正则表达式模块，用于字符串匹配和处理
import os  # 操作系统模块，用于文件路径操作
from datetime import datetime, timedelta, timezone  # 日期和时间模块
import random  # 随机数模块
import opencc  # 简繁转换模块

# 简繁转换函数========================================
def traditional_to_simplified(text: str) -> str:
    """
    将繁体中文文本转换为简体中文。
    :param text: 繁体中文文本
    :return: 简体中文文本
    """
    # 初始化转换器，"t2s" 表示从繁体转为简体
    converter = opencc.OpenCC('t2s')
    simplified_text = converter.convert(text)
    return simplified_text

# 记录程序执行的开始时间========================================
timestart = datetime.now()
# 报时  '',
#print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")             

# 读取文本文件到数组的函数========================================
def read_txt_to_array(file_name):
    """
    从指定文件中读取文本内容，返回一个包含每行内容的列表。
    :param file_name: 文件路径
    :return: 包含每行内容的列表
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]  # 跳过空行
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# 读取 BlackList （黑名单文件）的函数========================================
def read_blacklist_from_txt(file_path):
    """
    从指定文件中读取黑名单内容，返回一个包含黑名单项的列表。
    :param file_path: 文件路径
    :return: 包含黑名单项的列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    BlackList = [line.split(',')[1].strip() for line in lines if ',' in line]
    return BlackList

# 读取黑名单文件========================================
    """
    【assets/blacklist1/blacklist_auto.txt】  自动生成的黑名单，由【assets/blacklist1/blacklist1.py】生成
    【assets/blacklist1/blacklist_manual.txt】    手工编写的黑名单
    """
blacklist_auto = read_blacklist_from_txt('assets/blacklist1/blacklist_auto.txt')
blacklist_manual = read_blacklist_from_txt('assets/blacklist1/blacklist_manual.txt')
# combined_blacklist = list(set(blacklist_auto + blacklist_manual))
combined_blacklist = set(blacklist_auto + blacklist_manual)

# 定义列表，用于存储不同频道的行文本========================================
# 示例：sh_lines 存储上海频道的内容
sh_lines = []  # 上海频道
ys_lines = []  # CCTV频道
ws_lines = []  # 卫视频道
ty_lines = []  # 体育频道
dy_lines = []  # 电影频道
dsj_lines = []  # 电视剧频道
gat_lines = []  # 港澳台频道
gj_lines = []  # 国际台频道
jlp_lines = []  # 纪录片频道
dhp_lines = []  # 动画片频道
xq_lines = []  # 戏曲频道
js_lines = []  # 解说频道
cw_lines = []  # 春晚频道
mx_lines = []  # 明星频道
ztp_lines = []  # 主题片频道
zy_lines = []  # 综艺频道
yy_lines = []  # 音乐频道
game_lines = []  # 游戏频道
radio_lines = []  # 收音机频道

zj_lines = []  # 地方台-浙江频道
jsu_lines = []  # 地方台-江苏频道
gd_lines = []  # 地方台-广东频道
hn_lines = []  # 地方台-湖南频道
ah_lines = []  # 地方台-安徽频道
hain_lines = []  # 地方台-海南频道
nm_lines = []  # 地方台-内蒙频道
hb_lines = []  # 地方台-湖北频道
ln_lines = []  # 地方台-辽宁频道
sx_lines = []  # 地方台-陕西频道
shanxi_lines = []  # 地方台-山西频道
shandong_lines = []  # 地方台-山东频道
yunnan_lines = []  # 地方台-云南频道


##################【2024-07-30 18:04:56】
bj_lines = []  # 地方台-北京频道
cq_lines = []  # 地方台-重庆频道
fj_lines = []  # 地方台-福建频道
gs_lines = []  # 地方台-甘肃频道
gx_lines = []  # 地方台-广西频道
gz_lines = []  # 地方台-贵州频道
heb_lines = []  # 地方台-河北频道
hen_lines = []  # 地方台-河南频道
hlj_lines = []  # 地方台-黑龙江频道
jl_lines = []  # 地方台-吉林频道
jx_lines = []  # 地方台-江西频道
nx_lines = []  # 地方台-宁夏频道
qh_lines = []  # 地方台-青海频道
sc_lines = []  # 地方台-四川频道
tj_lines = []  # 地方台-天津频道
xj_lines = []  # 地方台-新疆频道

##################【2025-02-12 16:50:56】
wuxi_lines = []  # 地方台-无锡频道

# 其他特殊频道
zb_lines = []  # 直播中国
mtv_lines = []  # MTV频道
# Olympics_2024_Paris_lines = []  # 2024巴黎奥运会频道
other_lines = []  # 其他频道
other_lines_url = []  # 用于记录已添加的URL，为降低other文件大小，剔除重复url添加


# 处理频道名称字符串的函数========================================
def process_name_string(input_str):
    """
    对频道名称字符串进行处理，包括拆分和单独处理每个部分。
    :param input_str: 原始频道名称字符串
    :return: 处理后的频道名称字符串
    """
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

# 处理频道名称部分的函数========================================
def process_part(part_str):
    """
    对频道名称的每个部分进行处理，包括去除特定字符和格式化。
    :param part_str: 原始频道名称部分
    :return: 处理后的频道名称部分
    """
    # 处理逻辑
    if "CCTV" in part_str and "://" not in part_str:
        part_str = part_str.replace("IPV6", "")  # 去除IPV6字样
        part_str = part_str.replace("PLUS", "+")  # 替换PLUS
        part_str = part_str.replace("1080", "")  # 替换1080
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():  # 处理特殊情况，如果发现没有找到频道数字返回原名称
            filtered_str = part_str.replace("CCTV", "")
        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):  # 特殊处理CCTV中部分4K和8K名称
           # 使用正则表达式替换，删除4K或8K后面的字符，并且保留4K或8K
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2:
                # 给4K或8K添加括号                                        
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)
        return "CCTV" + filtered_str
    elif "卫视" in part_str:
        # 定义正则表达式模式，匹配“卫视”后面的内容                                                                         
        pattern = r'卫视「.*」'  # 定义正则表达式模式
        # 使用sub函数替换匹配的内容为空字符串                                                             
        result_str = re.sub(pattern, '卫视', part_str)  # 替换匹配的内容
        return result_str
    return part_str

# 获取URL文件扩展名的函数，准备支持m3u格式========================================
def get_url_file_extension(url):
    """
    从URL中提取文件扩展名。
    :param url: URL字符串
    :return: 文件扩展名
    """
    parsed_url = urlparse(url)  # 解析URL
    path = parsed_url.path  # 获取路径部分
    extension = os.path.splitext(path)[1]  # 提取文件扩展名
    return extension

# 定义一个函数，用于将m3u格式的内容转换为txt格式========================================
def convert_m3u_to_txt(m3u_content):
    """
    将m3u格式的内容转换为txt格式。
    :param m3u_content: m3u格式的字符串内容
    :return: 转换后的txt格式内容
    """
    # 分行处理m3u内容
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http") or line.startswith("rtmp") or line.startswith("p3p"):
            txt_lines.append(f"{channel_name},{line.strip()}")
        
        # 处理后缀名为m3u，但是内容为txt的文件
        if "#genre#" not in line and "," in line and "://" in line:
            # 定义正则表达式，匹配频道名称，URL的格式，并确保URL包含 "://"
            # xxxx,http://xxxxx.xx.xx                                     
            pattern = r'^[^,]+,[^\s]+://[^\s]+$'
            if bool(re.match(pattern, line)):
                txt_lines.append(line)
    
    # 将结果合并成一个字符串，以换行符分隔
    return '\n'.join(txt_lines)

# 定义一个函数，用于检查URL是否已经存在于列表中========================================
def check_url_existence(data_list, url):
    """
    检查给定的URL是否已经存在于列表中。
    :param data_list: List of strings containing the data 包含数据的列表
    :param url: The URL to check for existence 要检查的URL
    :return: True if the URL exists in the list, otherwise False 如果URL不存在于列表中，返回True；否则返回False
    """
    # 提取列表中的URL部分
    urls = [item.split(',')[1] for item in data_list]
    return url not in urls #如果不存在则返回true，需要

# 定义一个函数，用于清理URL中的$符号及其后面的内容========================================
def clean_url(url):
    """
    清理URL中的$符号及其后面的内容。
    :param url: 原始URL
    :return: 清理后的URL
    """
    last_dollar_index = url.rfind('$')  # 找到最后一个$的位置
    if last_dollar_index != -1:
        return url[:last_dollar_index]  # 返回$之前的部分
    return url

# 定义一个列表，包含需要从频道名称中移除的特定字符或字符串========================================
removal_list = ["_电信", "电信", "高清", "频道", "（HD）", "-HD", "英陆", "_ITV", "(北美)", "(HK)", "AKtv", "「IPV4」", "「IPV6」",
                "频陆", "备陆", "壹陆", "贰陆", "叁陆", "肆陆", "伍陆", "陆陆", "柒陆", "频晴", "频粤", "[超清]", "高清", "超清", "标清", "斯特",
                "粤陆", "国陆", "肆柒", "频英", "频特", "频国", "频壹", "频贰", "肆贰", "频测", "咪咕"]

# 定义一个函数，用于清理频道名称中的特定字符或字符串========================================
def clean_channel_name(channel_name, removal_list):
    """
    清理频道名称中的特定字符或字符串。
    :param channel_name: 原始频道名称
    :param removal_list: 包含需要移除的字符或字符串的列表
    :return: 清理后的频道名称
    """
    for item in removal_list:
        channel_name = channel_name.replace(item, "")  # 移除指定的字符或字符串
    
    # 检查并移除末尾的 'HD'
    if channel_name.endswith("HD"):
        channel_name = channel_name[:-2]  # 去掉最后两个字符 "HD"
    
    # 检查并移除末尾的 '台'
    if channel_name.endswith("台") and len(channel_name) > 3:
        channel_name = channel_name[:-1]  # 去掉最后一个字符 "台"
    
    return channel_name

# ================================================================================
# 定义一个函数，用于归类处理频道行，把这部分从process_url剥离出来，为以后加入whitelist源清单做准备。包括分发到不同的频道类别。
def process_channel_line(line):
    """
    处理频道行，包括分发到不同的频道类别。
    :param line: 频道行字符串，格式为"频道名称,频道地址"
    """
    if "#genre#" not in line and "#EXTINF:" not in line and "," in line and "://" in line:
        channel_name = line.split(',')[0].strip()  # 提取频道名称
        channel_name = clean_channel_name(channel_name, removal_list)  # 清理频道名称channel_name中的特定字符
        channel_name = traditional_to_simplified(channel_name)  # 将繁体字转换为简体字
        
        channel_address = clean_url(line.split(',')[1].strip())  # 清理URL中的$符号及其后面的内容
        line = f"{channel_name},{channel_address}"  # 重新组织行内容
        
        if channel_address not in combined_blacklist:  # 判断当前源是否在黑名单blacklist中
            # 根据频道名称或频道地址，将频道分发到不同的类别
            if "CCTV" in channel_name and check_url_existence(ys_lines, channel_address):  # 央视频道
                ys_lines.append(process_name_string(line.strip()))
            # （CCTV）如果频道名称中有【CCTV】，且频道地址不在【ys_lines】中，则添加到【ys_lines】中。
            # elif channel_name in Olympics_2024_Paris_dictionary and check_url_existence(Olympics_2024_Paris_lines, channel_address): #奥运频道 ADD 2024-08-05
            #     Olympics_2024_Paris_lines.append(process_name_string(line.strip()))
            elif channel_name in ws_dictionary and check_url_existence(ws_lines, channel_address): #卫视频道
                ws_lines.append(process_name_string(line.strip()))
            # (公共)如果频道名称在字典【ws_dictionary，主频道/卫视频道.txt】中，且频道地址不在【ws_lines】中，则添加到【ws_lines】中。
            elif channel_name in ty_dictionary and check_url_existence(ty_lines, channel_address):  #体育频道
                ty_lines.append(process_name_string(line.strip()))
            elif channel_name in dy_dictionary and check_url_existence(dy_lines, channel_address):  #电影频道
                dy_lines.append(process_name_string(line.strip()))
            elif channel_name in dsj_dictionary and check_url_existence(dsj_lines, channel_address):  #电视剧频道
                dsj_lines.append(process_name_string(line.strip()))
            elif channel_name in sh_dictionary and check_url_existence(sh_lines, channel_address):  #上海频道
                sh_lines.append(process_name_string(line.strip()))
            elif channel_name in gat_dictionary and check_url_existence(gat_lines, channel_address):  #港澳台
                gat_lines.append(process_name_string(line.strip()))
            elif channel_name in gj_dictionary and check_url_existence(gj_lines, channel_address):  #国际台
                gj_lines.append(process_name_string(line.strip()))
            elif channel_name in jlp_dictionary and check_url_existence(jlp_lines, channel_address):  #纪录片
                jlp_lines.append(process_name_string(line.strip()))
            elif channel_name in dhp_dictionary and check_url_existence(dhp_lines, channel_address):  #动画片
                dhp_lines.append(process_name_string(line.strip()))
            elif channel_name in xq_dictionary and check_url_existence(xq_lines, channel_address):  #戏曲
                xq_lines.append(process_name_string(line.strip()))
            elif channel_name in js_dictionary and check_url_existence(js_lines, channel_address):  #解说
                js_lines.append(process_name_string(line.strip()))
            elif channel_name in cw_dictionary and check_url_existence(cw_lines, channel_address):  #春晚
                cw_lines.append(process_name_string(line.strip()))
            elif channel_name in mx_dictionary and check_url_existence(mx_lines, channel_address):  #明星
                mx_lines.append(process_name_string(line.strip()))
            elif channel_name in ztp_dictionary and check_url_existence(ztp_lines, channel_address):  #主题片
                ztp_lines.append(process_name_string(line.strip()))
            elif channel_name in zy_dictionary and check_url_existence(zy_lines, channel_address):  #综艺频道
                zy_lines.append(process_name_string(line.strip()))
            elif channel_name in yy_dictionary and check_url_existence(yy_lines, channel_address):  #音乐频道
                yy_lines.append(process_name_string(line.strip()))
            elif channel_name in game_dictionary and check_url_existence(game_lines, channel_address):  #游戏频道
                game_lines.append(process_name_string(line.strip()))
            elif channel_name in radio_dictionary and check_url_existence(radio_lines, channel_address):  #收音机频道
                radio_lines.append(process_name_string(line.strip()))
            elif channel_name in zj_dictionary and check_url_existence(zj_lines, channel_address):  #地方台-浙江频道
                zj_lines.append(process_name_string(line.strip()))
            elif channel_name in jsu_dictionary and check_url_existence(jsu_lines, channel_address):  #地方台-江苏频道
                jsu_lines.append(process_name_string(line.strip()))
            elif channel_name in gd_dictionary and check_url_existence(gd_lines, channel_address):  #地方台-广东频道
                gd_lines.append(process_name_string(line.strip()))
            elif channel_name in hn_dictionary and check_url_existence(hn_lines, channel_address):  #地方台-湖南频道
                hn_lines.append(process_name_string(line.strip()))
            elif channel_name in hb_dictionary and check_url_existence(hb_lines, channel_address):  #地方台-湖北频道
                hb_lines.append(process_name_string(line.strip()))
            elif channel_name in ah_dictionary and check_url_existence(ah_lines, channel_address):  #地方台-安徽频道
                ah_lines.append(process_name_string(line.strip()))
            elif channel_name in hain_dictionary and check_url_existence(hain_lines, channel_address):  #地方台-海南频道
                hain_lines.append(process_name_string(line.strip()))
            elif channel_name in nm_dictionary and check_url_existence(nm_lines, channel_address):  #地方台-内蒙频道
                nm_lines.append(process_name_string(line.strip()))
            elif channel_name in ln_dictionary and check_url_existence(ln_lines, channel_address):  #地方台-辽宁频道
                ln_lines.append(process_name_string(line.strip()))
            elif channel_name in sx_dictionary and check_url_existence(sx_lines, channel_address):  #地方台-陕西频道
                sx_lines.append(process_name_string(line.strip()))
            elif channel_name in shanxi_dictionary and check_url_existence(shanxi_lines, channel_address):  #地方台-山西频道
                shanxi_lines.append(process_name_string(line.strip()))
            elif channel_name in shandong_dictionary and check_url_existence(shandong_lines, channel_address):  #地方台-山东频道
                shandong_lines.append(process_name_string(line.strip()))
            elif channel_name in yunnan_dictionary and check_url_existence(yunnan_lines, channel_address):  #地方台-云南频道
                yunnan_lines.append(process_name_string(line.strip()))
            elif channel_name in bj_dictionary and check_url_existence(bj_lines, channel_address):  #地方台-北京频道 ADD【2024-07-30 20:52:53】
                bj_lines.append(process_name_string(line.strip()))
            elif channel_name in cq_dictionary and check_url_existence(cq_lines, channel_address):  #地方台-重庆频道 ADD【2024-07-30 20:52:53】
                cq_lines.append(process_name_string(line.strip()))
            elif channel_name in fj_dictionary and check_url_existence(fj_lines, channel_address):  #地方台-福建频道 ADD【2024-07-30 20:52:53】
                fj_lines.append(process_name_string(line.strip()))
            elif channel_name in gs_dictionary and check_url_existence(gs_lines, channel_address):  #地方台-甘肃频道 ADD【2024-07-30 20:52:53】
                gs_lines.append(process_name_string(line.strip()))
            elif channel_name in gx_dictionary and check_url_existence(gx_lines, channel_address):  #地方台-广西频道 ADD【2024-07-30 20:52:53】
                gx_lines.append(process_name_string(line.strip()))
            elif channel_name in gz_dictionary and check_url_existence(gz_lines, channel_address):  #地方台-贵州频道 ADD【2024-07-30 20:52:53】
                gz_lines.append(process_name_string(line.strip()))
            elif channel_name in heb_dictionary and check_url_existence(heb_lines, channel_address):  #地方台-河北频道 ADD【2024-07-30 20:52:53】
                heb_lines.append(process_name_string(line.strip()))
            elif channel_name in hen_dictionary and check_url_existence(hen_lines, channel_address):  #地方台-河南频道 ADD【2024-07-30 20:52:53】
                hen_lines.append(process_name_string(line.strip()))
            elif channel_name in hlj_dictionary and check_url_existence(hlj_lines, channel_address):  #地方台-黑龙江频道 ADD【2024-07-30 20:52:53】
                hlj_lines.append(process_name_string(line.strip()))
            elif channel_name in jl_dictionary and check_url_existence(jl_lines, channel_address):  #地方台-吉林频道 ADD【2024-07-30 20:52:53】
                jl_lines.append(process_name_string(line.strip()))
            elif channel_name in nx_dictionary and check_url_existence(nx_lines, channel_address):  #地方台-宁夏频道 ADD【2024-07-30 20:52:53】
                nx_lines.append(process_name_string(line.strip()))
            elif channel_name in jx_dictionary and check_url_existence(jx_lines, channel_address):  #地方台-江西频道 ADD【2024-07-30 20:52:53】
                jx_lines.append(process_name_string(line.strip()))
            elif channel_name in qh_dictionary and check_url_existence(qh_lines, channel_address):  #地方台-青海频道 ADD【2024-07-30 20:52:53】
                qh_lines.append(process_name_string(line.strip()))
            elif channel_name in sc_dictionary and check_url_existence(sc_lines, channel_address):  #地方台-四川频道 ADD【2024-07-30 20:52:53】
                sc_lines.append(process_name_string(line.strip()))
            elif channel_name in tj_dictionary and check_url_existence(tj_lines, channel_address):  #地方台-天津频道 ADD【2024-07-30 20:52:53】
                tj_lines.append(process_name_string(line.strip()))
            elif channel_name in xj_dictionary and check_url_existence(xj_lines, channel_address):  #地方台-新疆频道 ADD【2024-07-30 20:52:53】
                xj_lines.append(process_name_string(line.strip()))
            elif channel_name in zb_dictionary and check_url_existence(zb_lines, channel_address):  #直播中国
                zb_lines.append(process_name_string(line.strip()))
            elif channel_name in mtv_dictionary and check_url_existence(mtv_lines, channel_address):  #MTV
                mtv_lines.append(process_name_string(line.strip()))
            else:
                if channel_address not in other_lines_url:
                    other_lines_url.append(channel_address)  # 记录已添加的URL
                    other_lines.append(line.strip())  # 将未分类的频道添加到other_lines

# 定义一个函数，用于随机获取User-Agent========================================
def get_random_user_agent():
    """
    随机获取一个User-Agent。
    :return: 随机选择的User-Agent字符串
    """
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    ]
    return random.choice(USER_AGENTS)

# 定义一个函数，用于处理URL，包括获取内容、转换格式、分发频道等========================================
def process_url(url):
    """
    处理单个URL，读取其内容并解析频道信息。
    
    参数：
    url (str): 需要处理的URL。
    """
    try:
        other_lines.append("◆◆◆　"+url)  # 将URL存入other_lines，便于后续检查 2024-08-02 10:41
        
        # 创建一个请求对象并添加自定义header
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # 打开URL并读取内容
        with urllib.request.urlopen(req) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            # channel_name=""  # 初始化频道名称变量（未使用）
            # channel_address=""  # 初始化频道地址变量（未使用）

            # 处理m3u和m3u8文件，提取频道名称和地址
            if get_url_file_extension(url)==".m3u" or get_url_file_extension(url)==".m3u8":
                text=convert_m3u_to_txt(text)  # 将m3u/m3u8内容转换为纯文本格式

            # 逐行处理内容
            lines = text.split('\n')
            print(f"行数: {len(lines)}")  # 打印总行数
            for line in lines:
                if  "#genre#" not in line and "," in line and "://" in line:
                    # 拆分成频道名和URL部分
                    channel_name, channel_address = line.split(',', 1)
                    # 处理带#号的源（加速源）
                    if "#" not in channel_address:
                        process_channel_line(line)  # 如果没有井号，则照常按照每行规则进行分发
                    else: 
                        # 如果有“#”号，则根据“#”号分隔
                        url_list = channel_address.split('#')
                        for channel_url in url_list:
                            newline=f'{channel_name},{channel_url}'
                            process_channel_line(newline)  # 处理分隔后的每一行

            other_lines.append('\n')  # 每个url处理完成后，在other_lines加个回车 2024-08-02 10:46

    except Exception as e:
        print(f"处理URL时发生错误：{e}")  # 捕获并打印异常信息



# 获取当前工作目录，准备读取txt文件========================================
current_directory = os.getcwd()   

# 读取【主频道】目录下的频道列表文件到字典中，用于后续的过滤和排序===================

ys_dictionary=read_txt_to_array('主频道/CCTV.txt')  # 仅排序用
sh_dictionary=read_txt_to_array('主频道/shanghai.txt')  # 过滤+排序
ws_dictionary=read_txt_to_array('主频道/卫视频道.txt')  # 过滤+排序
ty_dictionary=read_txt_to_array('主频道/体育频道.txt')  # 过滤
dy_dictionary=read_txt_to_array('主频道/电影.txt')  # 过滤
dsj_dictionary=read_txt_to_array('主频道/电视剧.txt')  # 过滤
gat_dictionary=read_txt_to_array('主频道/港澳台.txt')  # 过滤
gj_dictionary=read_txt_to_array('主频道/国际台.txt')  # 过滤
jlp_dictionary=read_txt_to_array('主频道/纪录片.txt')  # 过滤
dhp_dictionary=read_txt_to_array('主频道/动画片.txt')  # 过滤
xq_dictionary=read_txt_to_array('主频道/戏曲频道.txt')  # 过滤
js_dictionary=read_txt_to_array('主频道/解说频道.txt')  # 过滤
cw_dictionary=read_txt_to_array('主频道/春晚.txt')  # 过滤+排序
mx_dictionary=read_txt_to_array('主频道/明星.txt')  # 过滤
ztp_dictionary=read_txt_to_array('主频道/主题片.txt')  # 过滤
zy_dictionary=read_txt_to_array('主频道/综艺频道.txt')  # 过滤
yy_dictionary=read_txt_to_array('主频道/音乐频道.txt')  # 过滤
game_dictionary=read_txt_to_array('主频道/游戏频道.txt')  # 过滤
radio_dictionary=read_txt_to_array('主频道/收音机频道.txt')  # 过滤

zb_dictionary=read_txt_to_array('主频道/直播中国.txt')  # 过滤
mtv_dictionary=read_txt_to_array('主频道/MTV.txt')  # 过滤
# Olympics_2024_Paris_dictionary=read_txt_to_array('主频道/奥运频道.txt')  # 过滤

# 读取【地方台】目录下的频道列表文件到字典中，用于后续的过滤和排序===================
zj_dictionary=read_txt_to_array('地方台/浙江频道.txt')  # 过滤
jsu_dictionary=read_txt_to_array('地方台/江苏频道.txt')  # 过滤
gd_dictionary=read_txt_to_array('地方台/广东频道.txt')  # 过滤
hn_dictionary=read_txt_to_array('地方台/湖南频道.txt')  # 过滤
ah_dictionary=read_txt_to_array('地方台/安徽频道.txt')  # 过滤
hain_dictionary=read_txt_to_array('地方台/海南频道.txt')  # 过滤
nm_dictionary=read_txt_to_array('地方台/内蒙频道.txt')  # 过滤
hb_dictionary=read_txt_to_array('地方台/湖北频道.txt')  # 过滤
ln_dictionary=read_txt_to_array('地方台/辽宁频道.txt')  # 过滤
sx_dictionary=read_txt_to_array('地方台/陕西频道.txt')  # 过滤
shanxi_dictionary=read_txt_to_array('地方台/山西频道.txt')  # 过滤
shandong_dictionary=read_txt_to_array('地方台/山东频道.txt')  # 过滤
yunnan_dictionary=read_txt_to_array('地方台/云南频道.txt')  # 过滤



# 更多地方台频道文件
bj_dictionary=read_txt_to_array('地方台/北京频道.txt')  # 过滤
cq_dictionary=read_txt_to_array('地方台/重庆频道.txt')  # 过滤
fj_dictionary=read_txt_to_array('地方台/福建频道.txt')  # 过滤
gs_dictionary=read_txt_to_array('地方台/甘肃频道.txt')  # 过滤
gx_dictionary=read_txt_to_array('地方台/广西频道.txt')  # 过滤
gz_dictionary=read_txt_to_array('地方台/贵州频道.txt')  # 过滤
heb_dictionary=read_txt_to_array('地方台/河北频道.txt')  # 过滤
hen_dictionary=read_txt_to_array('地方台/河南频道.txt')  # 过滤
hlj_dictionary=read_txt_to_array('地方台/黑龙江频道.txt')  # 过滤
jl_dictionary=read_txt_to_array('地方台/吉林频道.txt')  # 过滤
jx_dictionary=read_txt_to_array('地方台/江西频道.txt')  # 过滤
nx_dictionary=read_txt_to_array('地方台/宁夏频道.txt')  # 过滤
qh_dictionary=read_txt_to_array('地方台/青海频道.txt')  # 过滤
sc_dictionary=read_txt_to_array('地方台/四川频道.txt')  # 过滤
tj_dictionary=read_txt_to_array('地方台/天津频道.txt')  # 过滤
xj_dictionary=read_txt_to_array('地方台/新疆频道.txt')  # 过滤


# 读取纠错频道名称方法======================================
def load_corrections_name(filename):
    """
    从文件中加载频道名称的纠错信息。
    
    参数：
    filename (str): 纠错文件的路径。
    
    返回：
    corrections (dict): 包含纠错信息的字典，键为错误名称，值为正确名称。
    """
    corrections = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():  # 跳过空行
                continue
            parts = line.strip().split(',')
            correct_name = parts[0]
            for name in parts[1:]:
                corrections[name] = correct_name
    return corrections

# 读取频道名称纠错文件【assets/corrections_name.txt】=====================
corrections_name = load_corrections_name('assets/corrections_name.txt')

# 纠错频道名称
# correct_name_data(corrections_name,xxxx)
def correct_name_data(corrections, data):
    """
    对数据进行纠错处理，将错误的频道名称替换为正确的名称。
    
    参数：
    corrections (dict): 包含纠错信息的字典。
    data (list): 需要纠错的数据列表。
    
    返回：
    corrected_data (list): 纠错后的数据列表。
    """
    corrected_data = []
    for line in data:
        name, url = line.split(',', 1)
        if name in corrections and name != corrections[name]:
            name = corrections[name]
        corrected_data.append(f"{name},{url}")
    return corrected_data

# 【sort_data】函数，对数据进行排序====================
"""
def sort_data(order, data):
    # 创建一个字典来存储每行数据的索引
    order_dict = {name: i for i, name in enumerate(order)}
    
    # 定义一个排序键函数，处理不在 order_dict 中的字符串
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    # 按照 order 中的顺序对数据进行排序
    sorted_data = sorted(data, key=sort_key)
    return sorted_data
    
"""

# new 【sort_data】 函数，对数据进行排序 Update 2025.02.27====================
def sort_data(order, data):
    """
    参数：
    order (list): 指定的顺序列表。
    data (list): 需要排序的数据列表。
    
    返回：
    sorted_data (list): 排序后的数据列表。
    """
    # 创建优先级字典来存储每行数据的索引，支持大小写不敏感
    order_dict = {name.lower(): i for i, name in enumerate(order)}
    
    # 预处理数据，提取名称并计算优先级
    processed_data = []
    for line in data:
        try:
            name = line.split(',')[0].lower()
            priority = order_dict.get(name, len(order))
            processed_data.append((priority, line))
        except (IndexError, AttributeError):
            processed_data.append((len(order), line))
    
    # 按优先级排序
    sorted_data = sorted(processed_data, key=lambda x: x[0])
    
    # 提取原始数据并返回
    return [item[1] for item in sorted_data]
"""
1. 代码功能
该代码的主要功能是根据指定的顺序列表 order 对数据列表 data 进行排序。data 中的每个元素是一个以逗号分隔的字符串（CSV 格式），排序的依据是每个字符串的第一个字段（即名称）。如果某个名称不在 order 列表中，则将其排在最后。

2. 代码实现细节
2.1 order_dict 的创建
order_dict = {name: i for i, name in enumerate(order)}
这里使用字典推导式创建了一个字典 order_dict。

字典的键是 order 列表中的名称，值是该名称在 order 列表中的索引。

例如，如果 order = ['Alice', 'Bob', 'Charlie']，则 order_dict = {'Alice': 0, 'Bob': 1, 'Charlie': 2}。

这样做的目的是为了快速查找每个名称的排序优先级。

2.2 sort_key 函数
def sort_key(line):
    name = line.split(',')[0]
    return order_dict.get(name, len(order))
sort_key 是一个辅助函数，用于为 sorted 函数提供排序依据。

它从每一行数据中提取第一个字段（即名称），例如 'Bob,25,Engineer' 提取出 'Bob'。

然后通过 order_dict.get(name, len(order)) 查找该名称在 order_dict 中的优先级：

如果名称存在于 order_dict 中，则返回其对应的值（即优先级）。

如果名称不存在，则返回 len(order)，确保未列出的名称排在最后。

2.3 排序
sorted_data = sorted(data, key=sort_key)
使用 Python 内置的 sorted 函数对 data 进行排序。

key=sort_key 指定了排序的依据，即根据 sort_key 函数的返回值进行排序。

2.4 返回结果
return sorted_data
返回排序后的列表 sorted_data。

3. 代码的潜在问题
3.1 输入数据的格式问题
如果 data 中的某一行不符合 CSV 格式（例如没有逗号），line.split(',')[0] 会引发 IndexError。

如果某一行不是字符串类型（例如是 None 或其他类型），split 方法会引发 AttributeError。

3.2 大小写敏感问题
代码默认是大小写敏感的。例如，order 列表中的 'Alice' 和 data 中的 'alice' 会被视为不同的名称。

这可能导致排序结果不符合预期。

3.3 性能问题
如果 data 列表非常大，sort_key 函数会被频繁调用，可能会影响性能。

每次调用 sort_key 时都会执行 split 操作，这在数据量较大时可能会成为性能瓶颈。

4. 改进建议
4.1 增加错误处理
在 sort_key 函数中增加错误处理逻辑，确保代码的健壮性。

例如：
def sort_key(line):
    try:
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    except (IndexError, AttributeError):
        return len(order)  # 默认将格式错误的数据排在最后
4.2 支持大小写不敏感
在创建 order_dict 和提取名称时，将名称统一转换为小写（或大写）。

例如：
order_dict = {name.lower(): i for i, name in enumerate(order)}
def sort_key(line):
    try:
        name = line.split(',')[0].lower()
        return order_dict.get(name, len(order))
    except (IndexError, AttributeError):
        return len(order)
4.3 优化性能
如果 data 列表非常大，可以考虑对 data 进行预处理，避免在每次调用 sort_key 时重复执行 split 操作。

例如：
def sort_data(order, data):
    order_dict = {name.lower(): i for i, name in enumerate(order)}
    processed_data = []
    for line in data:
        try:
            name = line.split(',')[0].lower()
            priority = order_dict.get(name, len(order))
            processed_data.append((priority, line))
        except (IndexError, AttributeError):
            processed_data.append((len(order), line))
    # 按优先级排序
    sorted_data = sorted(processed_data, key=lambda x: x[0])
    # 提取原始数据
    return [item[1] for item in sorted_data]
5. 改进后的完整代码
"""

    
    
    
    
    


# 处理将检索的直播源列表【assets/urls-daily.txt】，将默认 MMDD 格式日期替换为实际日期===================
urls = read_txt_to_array('assets/urls-daily.txt')

for url in urls:
    if url.startswith("http"):
        if "{MMdd}" in url:  # 特别处理frxz751113/IPTVzb1
            current_date_str = datetime.now().strftime("%m%d")
            url=url.replace("{MMdd}", current_date_str)

        if "{MMdd-1}" in url:  # 特别处理frxz751113/IPTVzb1
            yesterday_date_str = (datetime.now() - timedelta(days=1)).strftime("%m%d")
            url=url.replace("{MMdd-1}", yesterday_date_str)
            
        print(f"处理URL: {url}")
        process_url(url)

# 定义一个函数，提取每行中逗号前面的数字部分作为排序的依据===================
def extract_number(s):
    """
    提取字符串中逗号前面的数字部分。
    
    参数：
    s (str): 输入字符串。
    
    返回：
    int: 提取的数字，如果没有数字则返回999。
    """
    num_str = s.split(',')[0].split('-')[1]  # 提取逗号前面的数字部分
    numbers = re.findall(r'\d+', num_str)   # 因为有+和K
    return int(numbers[-1]) if numbers else 999

# 定义一个自定义排序函数===================
def custom_sort(s):
    """
    自定义排序函数，用于处理特定的排序需求。
    
    参数：
    s (str): 输入字符串。
    
    返回：
    int: 排序依据的值。
    """
    if "CCTV-4K" in s:
        return 2  # 将包含 "4K" 的字符串排在后面
    elif "CCTV-8K" in s:
        return 3  # 将包含 "8K" 的字符串排在后面 
    elif "(4K)" in s:
        return 1  # 将包含 " (4K)" 的字符串排在后面
    else:
        return 0  # 其他字符串保持原顺序

# 读取白名单文件【assets/blacklist1/whitelist_auto.txt】，把高响应源从白名单中抽出加入merged_output===

print(f"ADD whitelist_auto.txt")
# 提示信息，表示正在处理 whitelist_auto.txt 文件

whitelist_auto_lines = read_txt_to_array('assets/blacklist1/whitelist_auto.txt')
# 读取 whitelist_auto.txt 文件内容，并将其按行存储到数组 whitelist_auto_lines 中
# read_txt_to_array 是一个自定义函数，用于读取文件并返回行数组

for whitelist_line in whitelist_auto_lines:
# 遍历 whitelist_auto_lines 数组中的每一行
    if "#genre#" not in whitelist_line and "," in whitelist_line and "://" in whitelist_line:
    # 检查当前行是否满足以下条件：
    # 1. 不包含 "#genre#" 字符串
    # 2. 包含逗号 ","
    # 3. 包含 "://"（通常是 URL 的协议部分，如 http:// 或 https://）
        whitelist_parts = whitelist_line.split(",")
        # 如果满足条件，将当前行按逗号分割成多个部分，存储到 whitelist_parts 数组中
        try:
        # 尝试将第一个部分（假设是响应时间）转换为浮点数
        # 例如，如果 whitelist_parts[0] 是 "100ms"，则替换 "ms" 后转换为 100.0
            response_time = float(whitelist_parts[0].replace("ms", ""))
        except ValueError:
            print(f"response_time转换失败: {whitelist_line}")
            # 如果转换失败（例如，格式不正确），输出错误信息，并将 response_time 设置为 60000 毫秒（60 秒）
            response_time = 60000  # 单位毫秒，转换失败给个默认值 60 秒

        if response_time < 2000:
        # 检查响应时间是否小于 2000 毫秒（2 秒）
            # 如果响应时间小于 2 秒，表示这是一个高响应源
            process_channel_line(",".join(whitelist_parts[1:]))
            # 将 whitelist_parts 数组中除第一个部分（响应时间）之外的部分重新用逗号连接成一个字符串
            # 并调用 process_channel_line 函数处理该字符串

# 随机取得URL，加入今日推荐===================
def get_random_url(file_path):
    """
    从文件中随机获取一个URL。
    
    参数：
    file_path (str): 文件路径。
    
    返回：
    str: 随机获取的URL，如果没有URL则返回None。
    """
    urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 查找逗号后面的部分，即URL
            url = line.strip().split(',')[-1]
            urls.append(url)    
    # 随机返回一个URL
    return random.choice(urls) if urls else None

# (新)每日一首MTV推荐列表文件【assets/今日推荐.txt】==================
daily_mtv="(新)每日一首,"+get_random_url('assets/今日推荐.txt')

# 获取当前的 UTC 时间
utc_time = datetime.now(timezone.utc)
# 北京时间
beijing_time = utc_time + timedelta(hours=8)
# 格式化为所需的格式
formatted_time = beijing_time.strftime("%Y%m%d %H:%M:%S")

# 关于信息对应的源地址URL=================================
about_video1=""  # 未使用的变量
about_video2=""  # 未使用的变量
version=formatted_time+","+about_video1  # 版本信息
about="关于本源,"+about_video2  # 关于信息


"""
["☘️山东频道,#genre#"] + sort_data(shandong_dictionary,set(correct_name_data(corrections_name,shandong_lines))) + ['\n'] + \

功能：
构建一个列表，包含山东频道的标题、处理后的数据以及一个换行符。
组成部分：
["☘️山东频道,#genre#"]：一个列表，包含山东频道的标题和分类标签。
sort_data(shandong_dictionary, set(correct_name_data(corrections_name, shandong_lines)))：
correct_name_data(corrections_name, shandong_lines)：对 shandong_lines 数据进行名称校正。
set(...)：将校正后的数据转换为集合，去重。
sort_data(shandong_dictionary, ...)：根据 shandong_dictionary 对去重后的数据进行排序。
['\n']：在列表末尾添加一个换行符。


["☘️江苏频道,#genre#"] + sorted(set(correct_name_data(corrections_name, jsu_lines))) + ['\n']
功能：
构建一个列表，包含江苏频道的标题、处理后的数据以及一个换行符。
组成部分：
["☘️江苏频道,#genre#"]：一个列表，包含江苏频道的标题和分类标签。
sorted(set(correct_name_data(corrections_name, jsu_lines)))：
correct_name_data(corrections_name, jsu_lines)：对 jsu_lines 数据进行名称校正。
set(...)：将校正后的数据转换为集合，去重。
sorted(...)：对去重后的数据进行排序。
['\n']：在列表末尾添加一个换行符。

【代码对比】
【相似点】：
两行代码的结构相似，都是通过列表拼接的方式构建最终结果。
都包含频道标题、数据处理（校正、去重、排序）以及换行符。
都使用了 correct_name_data 函数对数据进行名称校正。
【不同点】：
数据处理方式：
第一行代码使用了 sort_data(shandong_dictionary, ...)，可能是根据 shandong_dictionary 对数据进行自定义排序。
第二行代码直接使用了 sorted(...)，可能是对数据进行默认的字典序排序。
数据来源：
第一行代码处理的是 shandong_lines（山东频道的数据）。
第二行代码处理的是 jsu_lines（江苏频道的数据）。
【潜在问题】：
如果 sort_data 和 sorted 的排序逻辑不一致，可能会导致最终结果的顺序不一致。
如果 correct_name_data 函数的实现有问题，可能会导致数据校正不准确。



【优化建议】
统一排序逻辑：

如果希望两行代码的排序逻辑一致，可以将 sort_data 替换为 sorted，或者确保 sort_data 的实现与 sorted 的行为一致。

代码复用：

可以将重复的逻辑提取为一个函数，例如：

def build_channel_data(title, lines, corrections_name, dictionary=None):
    corrected_data = correct_name_data(corrections_name, lines)
    unique_data = set(corrected_data)
    sorted_data = sort_data(dictionary, unique_data) if dictionary else sorted(unique_data)
    return [title] + sorted_data + ['\n']

result = build_channel_data("☘️山东频道,#genre#", shandong_lines, corrections_name, shandong_dictionary) + \
         build_channel_data("☘️江苏频道,#genre#", jsu_lines, corrections_name)
         
换行符处理：

如果换行符是用于格式化输出，可以考虑在最终输出时统一添加，而不是在每个频道数据后单独添加。         

"""


# 瘦身版直播源===========================================
# 
# 【专区/about.txt】文件，显示在每日一首MTV推荐之后
# 合并所有对象中的行文本（去重，排序后拼接）

all_lines_simple =  ["更新时间,#genre#"] +[version] +[about] +[daily_mtv]+read_txt_to_array('专区/about.txt')+ ['\n'] +\
             ["🧨2025春晚🧨,#genre#"] + read_txt_to_array('专区/2025春晚.txt') + ['\n'] + \
             ["💓专享源🅰️,#genre#"] + read_txt_to_array('专区/♪专享源①.txt') + ['\n'] + \
             ["💓专享源🅱️,#genre#"] + read_txt_to_array('专区/♪专享源②.txt') + ['\n'] + \
             ["💓专享央视,#genre#"] + read_txt_to_array('专区/♪优质央视.txt') + ['\n'] + \
             ["💓专享卫视,#genre#"] + read_txt_to_array('专区/♪优质卫视.txt') + ['\n'] + \
             ["💓港澳台📶,#genre#"] + read_txt_to_array('专区/♪港澳台.txt') + ['\n'] + \
             ["💓AKTV🚀📶,#genre#"] + read_txt_to_array('专区/AKTV.txt') + ['\n'] + \
             ["💓台湾台📶,#genre#"] + read_txt_to_array('专区/♪台湾台.txt') + ['\n'] + \
             ["💓电视剧🔁,#genre#"] + read_txt_to_array('专区/♪电视剧.txt') + ['\n'] + \
             ["💓优质个源,#genre#"] + read_txt_to_array('专区/♪优质源.txt') + ['\n'] + \
             ["💓儿童专享,#genre#"] + read_txt_to_array('专区/♪儿童专享.txt') + ['\n'] + \
             ["💓咪咕直播,#genre#"] + read_txt_to_array('专区/♪咪咕直播.txt') + ['\n'] + \
             ["🏀SPORTS⚽️,#genre#"] + read_txt_to_array('专区/♪sports.txt') + ['\n'] + \
             ["🍹定制台☕️,#genre#"] + read_txt_to_array('专区/♪定制源.txt') + ['\n'] + \
             ["🍹定制P3P☕️,#genre#"] + read_txt_to_array('专区/p3p.txt') + ['\n'] + \
             ["💓英语频道,#genre#"] + read_txt_to_array('专区/♪英语频道.txt') + ['\n'] + \
             ["💓4K(Test),#genre#"] + read_txt_to_array('专区/4K.txt') + ['\n'] + \
             ["💓无锡频道,#genre#"] + read_txt_to_array('专区/无锡.txt') + ['\n'] + \
             ["☘️江苏频道,#genre#"] + sorted(set(correct_name_data(corrections_name,jsu_lines))) + ['\n'] + \
             ["☘️湖南频道,#genre#"] + sort_data(hn_dictionary,set(correct_name_data(corrections_name,hn_lines))) + ['\n'] + \
             ["☘️湖北频道,#genre#"] + sort_data(hb_dictionary,set(correct_name_data(corrections_name,hb_lines))) + ['\n'] + \
             ["☘️广东频道,#genre#"] + sort_data(gd_dictionary,set(correct_name_data(corrections_name,gd_lines))) + ['\n'] + \
             ["☘️浙江频道,#genre#"] + sort_data(zj_dictionary,set(correct_name_data(corrections_name,zj_lines))) + ['\n'] + \
             ["☘️山东频道,#genre#"] + sort_data(shandong_dictionary,set(correct_name_data(corrections_name,shandong_lines))) + ['\n'] + \
             ["上海频道,#genre#"] + sort_data(sh_dictionary,set(correct_name_data(corrections_name,sh_lines))) + ['\n'] + \
             ["体育频道,#genre#"] + sort_data(ty_dictionary,set(correct_name_data(corrections_name,ty_lines))) + ['\n']

# ["奥运频道,#genre#"] + sort_data(Olympics_2024_Paris_dictionary,set(correct_name_data(corrections_name,Olympics_2024_Paris_lines))) + ['\n'] + \

# 全集版直播源===========================================
# 
all_lines =  ["更新时间,#genre#"] +[version]  +[about] +[daily_mtv]+read_txt_to_array('专区/about.txt') + ['\n'] +\
             ["🧨2025春晚🧨,#genre#"] + read_txt_to_array('专区/2025春晚.txt') + ['\n'] + \
             ["💓专享源🅰️,#genre#"] + read_txt_to_array('专区/♪专享源①.txt') + ['\n'] + \
             ["💓专享源🅱️,#genre#"] + read_txt_to_array('专区/♪专享源②.txt') + ['\n'] + \
             ["💓专享央视,#genre#"] + read_txt_to_array('专区/♪优质央视.txt') + ['\n'] + \
             ["💓专享卫视,#genre#"] + read_txt_to_array('专区/♪优质卫视.txt') + ['\n'] + \
             ["💓港澳台📶,#genre#"] + read_txt_to_array('专区/♪港澳台.txt') + ['\n'] + \
             ["💓AKTV🚀📶,#genre#"] + read_txt_to_array('专区/AKTV.txt') + ['\n'] + \
             ["💓台湾台📶,#genre#"] + read_txt_to_array('专区/♪台湾台.txt') + ['\n'] + \
             ["💓电视剧🔁,#genre#"] + read_txt_to_array('专区/♪电视剧.txt') + ['\n'] + \
             ["💓优质个源,#genre#"] + read_txt_to_array('专区/♪优质源.txt') + ['\n'] + \
             ["💓儿童专享,#genre#"] + read_txt_to_array('专区/♪儿童专享.txt') + ['\n'] + \
             ["💓咪咕直播,#genre#"] + read_txt_to_array('专区/♪咪咕直播.txt') + ['\n'] + \
             ["🏀SPORTS⚽️,#genre#"] + read_txt_to_array('专区/♪sports.txt') + ['\n'] + \
             ["🍹定制台☕️,#genre#"] + read_txt_to_array('专区/♪定制源.txt') + ['\n'] + \
             ["🍹定制P3P☕️,#genre#"] + read_txt_to_array('专区/p3p.txt') + ['\n'] + \
             ["💓英语频道,#genre#"] + read_txt_to_array('专区/♪英语频道.txt') + ['\n'] + \
             ["💓4K(Test),#genre#"] + read_txt_to_array('专区/4K.txt') + ['\n'] + \
             ["💓无锡频道,#genre#"] + read_txt_to_array('专区/无锡.txt') + ['\n'] + \
             ["🌐央视频道,#genre#"] + sort_data(ys_dictionary,correct_name_data(corrections_name,ys_lines)) + ['\n'] + \
             ["📡卫视频道,#genre#"] + sort_data(ws_dictionary,correct_name_data(corrections_name,ws_lines)) + ['\n'] + \
             ["上海频道,#genre#"] + sort_data(sh_dictionary,correct_name_data(corrections_name,sh_lines)) + ['\n'] + \
             ["体育频道,#genre#"] + sort_data(ty_dictionary,correct_name_data(corrections_name,ty_lines)) + ['\n'] + \
             ["电影频道,#genre#"] + sort_data(dy_dictionary,correct_name_data(corrections_name,dy_lines)) + ['\n'] + \
             ["电视剧频道,#genre#"] + sort_data(dsj_dictionary,correct_name_data(corrections_name,dsj_lines)) + ['\n'] + \
             ["明星,#genre#"] + sort_data(mx_dictionary,correct_name_data(corrections_name,mx_lines)) + ['\n'] + \
             ["主题片,#genre#"] + sort_data(ztp_dictionary,correct_name_data(corrections_name,ztp_lines)) + ['\n'] + \
             ["港澳台,#genre#"] + sort_data(gat_dictionary,correct_name_data(corrections_name,gat_lines)) + ['\n'] + \
             ["国际台,#genre#"] + sort_data(gj_dictionary,set(correct_name_data(corrections_name,gj_lines))) + ['\n'] + \
             ["纪录片,#genre#"] + sort_data(jlp_dictionary,set(correct_name_data(corrections_name,jlp_lines)))+ ['\n'] + \
             ["动画片,#genre#"] + sort_data(dhp_dictionary,set(correct_name_data(corrections_name,dhp_lines)))+ ['\n'] + \
             ["戏曲频道,#genre#"] + sort_data(xq_dictionary,set(correct_name_data(corrections_name,xq_lines))) + ['\n'] + \
             ["综艺频道,#genre#"] + sorted(set(correct_name_data(corrections_name,zy_lines))) + ['\n'] + \
             ["音乐频道,#genre#"] + sorted(set(yy_lines)) + ['\n'] + \
             ["游戏频道,#genre#"] + sorted(set(game_lines)) + ['\n'] + \
             ["☘️湖南频道,#genre#"] + sort_data(hn_dictionary,set(correct_name_data(corrections_name,hn_lines))) + ['\n'] + \
             ["☘️湖北频道,#genre#"] + sort_data(hb_dictionary,set(correct_name_data(corrections_name,hb_lines))) + ['\n'] + \
             ["☘️广东频道,#genre#"] + sort_data(gd_dictionary,set(correct_name_data(corrections_name,gd_lines))) + ['\n'] + \
             ["☘️浙江频道,#genre#"] + sort_data(zj_dictionary,set(correct_name_data(corrections_name,zj_lines))) + ['\n'] + \
             ["☘️山东频道,#genre#"] + sort_data(shandong_dictionary,set(correct_name_data(corrections_name,shandong_lines))) + ['\n'] + \
             ["☘️江苏频道,#genre#"] + sorted(set(correct_name_data(corrections_name,jsu_lines))) + ['\n'] + \
             ["☘️安徽频道,#genre#"] + sorted(set(correct_name_data(corrections_name,ah_lines))) + ['\n'] + \
             ["☘️海南频道,#genre#"] + sorted(set(correct_name_data(corrections_name,hain_lines))) + ['\n'] + \
             ["☘️内蒙频道,#genre#"] + sorted(set(correct_name_data(corrections_name,nm_lines))) + ['\n'] + \
             ["☘️辽宁频道,#genre#"] + sorted(set(correct_name_data(corrections_name,ln_lines))) + ['\n'] + \
             ["☘️陕西频道,#genre#"] + sorted(set(correct_name_data(corrections_name,sx_lines))) + ['\n'] + \
             ["☘️山西频道,#genre#"] + sorted(set(correct_name_data(corrections_name,shanxi_lines))) + ['\n'] + \
             ["☘️云南频道,#genre#"] + sorted(set(correct_name_data(corrections_name,yunnan_lines))) + ['\n'] + \
             ["☘️北京频道,#genre#"] + sorted(set(correct_name_data(corrections_name,bj_lines))) + ['\n'] + \
             ["☘️重庆频道,#genre#"] + sorted(set(correct_name_data(corrections_name,cq_lines))) + ['\n'] + \
             ["☘️福建频道,#genre#"] + sorted(set(correct_name_data(corrections_name,fj_lines))) + ['\n'] + \
             ["☘️甘肃频道,#genre#"] + sorted(set(correct_name_data(corrections_name,gs_lines))) + ['\n'] + \
             ["☘️广西频道,#genre#"] + sorted(set(correct_name_data(corrections_name,gx_lines))) + ['\n'] + \
             ["☘️贵州频道,#genre#"] + sorted(set(correct_name_data(corrections_name,gz_lines))) + ['\n'] + \
             ["☘️河北频道,#genre#"] + sorted(set(correct_name_data(corrections_name,heb_lines))) + ['\n'] + \
             ["☘️河南频道,#genre#"] + sorted(set(correct_name_data(corrections_name,hen_lines))) + ['\n'] + \
             ["☘️黑龙江频道,#genre#"] + sorted(set(correct_name_data(corrections_name,hlj_lines))) + ['\n'] + \
             ["☘️吉林频道,#genre#"] + sorted(set(correct_name_data(corrections_name,jl_lines))) + ['\n'] + \
             ["☘️江西频道,#genre#"] + sorted(set(correct_name_data(corrections_name,jx_lines))) + ['\n'] + \
             ["☘️宁夏频道,#genre#"] + sorted(set(correct_name_data(corrections_name,nx_lines))) + ['\n'] + \
             ["☘️青海频道,#genre#"] + sorted(set(correct_name_data(corrections_name,qh_lines))) + ['\n'] + \
             ["☘️四川频道,#genre#"] + sorted(set(correct_name_data(corrections_name,sc_lines))) + ['\n'] + \
             ["☘️天津频道,#genre#"] + sorted(set(correct_name_data(corrections_name,tj_lines))) + ['\n'] + \
             ["☘️新疆频道,#genre#"] + sorted(set(correct_name_data(corrections_name,xj_lines))) + ['\n'] + \
             ["解说频道,#genre#"] + sorted(set(js_lines)) + ['\n'] + \
             ["春晚,#genre#"] + sort_data(cw_dictionary,set(cw_lines))  + ['\n'] + \
             ["直播中国,#genre#"] + sorted(set(correct_name_data(corrections_name,zb_lines))) + ['\n'] + \
             ["MTV,#genre#"] + sorted(set(correct_name_data(corrections_name,mtv_lines))) + ['\n'] + \
             ["收音机频道,#genre#"] + sort_data(radio_dictionary,set(radio_lines))  + ['\n'] + \
             ["❤️与凤行,#genre#"] + read_txt_to_array('专区/特供频道/♪与凤行.txt')  + ['\n'] + \
             ["❤️以家人之名,#genre#"] + read_txt_to_array('专区/特供频道/♪以家人之名.txt')

# 定制内容的输出文件（注释掉了，未启用）
# custom_lines_wang =  ["更新时间,#genre#"] +[version] + ['\n'] +\
#             ["港澳台,#genre#"] + sort_data(gat_dictionary,set(correct_name_data(corrections_name,gat_lines))) + ['\n'] 


# ========================================写入TXT格式直播源列表文件========================================
# 定义输出直播源文件名
output_file = "merged_output.txt"
output_file_simple = "merged_output_simple.txt"
others_file = "others_output.txt"

# NEW定义输出直播源文件名
new_output_file = "live.txt"
new_output_file_simple = "live_lite.txt"

# # custom定制
# output_file_custom_wang = "custom/wang.txt"

try:
    # 将“瘦身版”内容写入文件【merged_output_simple.txt】================================================
    # """
    with open(output_file_simple, 'w', encoding='utf-8') as f:
        for line in all_lines_simple:  # 遍历 all_lines_simple 列表
            f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"合并后的文本已保存到文件: {output_file_simple}")
   # """

    # 将“瘦身版”内容写入新文件【live_lite.txt】================================================
    with open(new_output_file_simple, 'w', encoding='utf-8') as f:
        for line in all_lines_simple:  # 遍历 all_lines_simple 列表
            f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"合并后的文本已保存到文件: {new_output_file_simple}")

    # 将“全集版”内容写入文件【merged_output.txt】================================================
    # """
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:  # 遍历 all_lines 列表
            f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"合并后的文本已保存到文件: {output_file}")
    #"""

    # 将“全集版”内容写入新文件【live.txt】================================================
    with open(new_output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:  # 遍历 all_lines 列表
            f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"合并后的文本已保存到文件: {new_output_file}")

    # 将“其他”内容写入文件【others_output.txt】================================================
    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:  # 遍历 other_lines 列表
            f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"Others已保存到文件: {others_file}")

    # 定制内容的写入【custom/wang.txt】==========================================
    """
    with open(output_file_custom_wang, 'w', encoding='utf-8') as f:
        for line in custom_lines_wang:  # 遍历 custom_lines_wang 列表
             f.write(line + '\n')  # 将每一行写入文件，添加换行符
    print(f"合并后的文本已保存到文件: {output_file_custom_wang}")
    """

except Exception as e:
    print(f"保存文件时发生错误：{e}")  # 捕获异常并打印错误信息

# ========================================写入m3u格式直播源列表文件========================================
# 报时
#print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")

# 从【assets/logo.txt】读取频道图标logo信息======================================
channels_logos = read_txt_to_array('assets/logo.txt')  # 从文件中读取logo库

# 定义函数：根据频道名称获取logo
def get_logo_by_channel_name(channel_name):
    """
    根据频道名称获取对应的logo URL。
    :param channel_name: 频道名称
    :return: logo URL，如果未找到则返回 None
    """
    # 遍历 logo 库
    for line in channels_logos:
        # 去除首尾空白并检查是否为空行
        if not line.strip():
            continue
        name, url = line.split(',')  # 分割频道名称和 logo URL
        if name == channel_name:  # 如果找到匹配的频道名称
            return url  # 返回对应的 logo URL
    return None  # 如果未找到，返回 None


# #output_text = '#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml,https://epg.112114.xyz/pp.xml.gz,https://assets.livednow.com/epg.xml"\n'
# output_text = '#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n'

# with open(output_file, "r", encoding='utf-8') as file:
#     input_text = file.read()

# lines = input_text.strip().split("\n")
# group_name = ""
# for line in lines:
#     parts = line.split(",")
#     if len(parts) == 2 and "#genre#" in line:
#         group_name = parts[0]
#     elif len(parts) == 2:
#         channel_name = parts[0]
#         channel_url = parts[1]
#         logo_url=get_logo_by_channel_name(channel_name)
#         if logo_url is None:  #not found logo
#             output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{channel_name}\n"
#             output_text += f"{channel_url}\n"
#         else:
#             output_text += f"#EXTINF:-1  tvg-name=\"{channel_name}\" tvg-logo=\"{logo_url}\"  group-title=\"{group_name}\",{channel_name}\n"
#             output_text += f"{channel_url}\n"

# with open("merged_output.m3u", "w", encoding='utf-8') as file:
#     file.write(output_text)

# print("merged_output.m3u文件已生成。")

# 定义函数：生成 M3U 文件
def make_m3u(txt_file, m3u_file, m3u_file_copy):
    """
    根据给定的文本文件生成 M3U 文件。
    :param txt_file: 输入的文本文件
    :param m3u_file: 输出的 M3U 文件
    :param m3u_file_copy: 输出的 M3U 文件副本
    """
    try:
        # 定义 M3U 文件的头部信息
        #output_text = '#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml,https://epg.112114.xyz/pp.xml.gz,https://assets.livednow.com/epg.xml"\n'
        output_text = '#EXTM3U x-tvg-url="https://live.fanmingming.cn/e.xml"\n'

        # # 打开txt文件读取
        # with open(txt_file, 'r', encoding='utf-8') as txt:
        #     lines = txt.readlines()

        # # 创建m3u文件并写入
        # with open(m3u_file, 'w', encoding='utf-8') as m3u:
        #     # 写入m3u文件的头部信息
        #     m3u.write('#EXTM3U\n')

        #     # 写入音频文件路径
        #     for line in lines:
        #         line = line.strip()
        #         if line:  # 忽略空行
        #             m3u.write(f'{line}\n')
        with open(txt_file, "r", encoding='utf-8') as file:
            input_text = file.read()

        # 按行分割输入内容
        lines = input_text.strip().split("\n")
        group_name = ""  # 初始化组名称
        for line in lines:
            parts = line.split(",")  # 分割每一行的内容
            if len(parts) == 2 and "#genre#" in line:  # 如果是组标题行
                group_name = parts[0]  # 提取组名称
            elif len(parts) == 2:  # 如果是频道行
                channel_name = parts[0]  # 频道名称
                channel_url = parts[1]  # 频道 URL
                logo_url = get_logo_by_channel_name(channel_name)  # 获取频道 logo
                if logo_url is None:  # 如果未找到 logo
                    output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{channel_name}\n"
                    output_text += f"{channel_url}\n"
                else:  # 如果找到 logo
                    output_text += f"#EXTINF:-1  tvg-name=\"{channel_name}\" tvg-logo=\"{logo_url}\"  group-title=\"{group_name}\",{channel_name}\n"
                    output_text += f"{channel_url}\n"

        # 将生成的内容写入 M3U 文件
        with open(f"{m3u_file}", "w", encoding='utf-8') as file:
            file.write(output_text)
        with open(f"{m3u_file_copy}", "w", encoding='utf-8') as file:
            file.write(output_text)

        print(f"M3U文件 '{m3u_file}' 生成成功。")
        print(f"M3U文件 '{m3u_file_copy}' 生成成功。")
    except Exception as e:
        print(f"发生错误: {e}")  # 捕获异常并打印错误信息

# 调用函数生成 M3U 文件
make_m3u(output_file, "merged_output.m3u", "live.m3u")
# make_m3u(new_output_file, "live1.m3u")
make_m3u(output_file_simple, "merged_output_simple.m3u", "live_lite.m3u")
# make_m3u(new_output_file_simple, "live_lite1.m3u")



# ========================================其他========================================


# 执行结束时间
timeend = datetime.now()

# 计算时间差
elapsed_time = timeend - timestart
total_seconds = elapsed_time.total_seconds()

# 转换为分钟和秒
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

# 格式化开始和结束时间
timestart_str = timestart.strftime("%Y%m%d_%H_%M_%S")
timeend_str = timeend.strftime("%Y%m%d_%H_%M_%S")

# 打印执行时间信息
print(f"开始时间: {timestart_str}")
print(f"结束时间: {timeend_str}")
print(f"执行时间: {minutes} 分 {seconds} 秒")

# 打印行数统计信息
combined_blacklist_hj = len(combined_blacklist)  # 黑名单行数
all_lines_hj = len(all_lines)  # 全集版行数
other_lines_hj = len(other_lines)  # 其他内容行数
print(f"blacklist行数: {combined_blacklist_hj} ")
print(f"merged_output.txt行数: {all_lines_hj} ")
print(f"others_output.txt行数: {other_lines_hj} ")



#备用1：http://tonkiang.us
#备用2：https://www.zoomeye.hk,https://www.shodan.io,https://tv.cctv.com/live/
#备用3：(BlackList检测对象)http,rtmp,p3p,rtp（rtsp，p2p）

