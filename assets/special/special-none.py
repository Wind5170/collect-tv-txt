import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone

# 读取文本文件并将其内容转换为数组的方法
def read_txt_to_array(file_name):
    try:
        # 打开文件并读取所有行
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # 去除每行的空白字符（如换行符）
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        # 如果文件未找到，打印错误信息并返回空数组
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        # 如果发生其他错误，打印错误信息并返回空数组
        print(f"An error occurred: {e}")
        return []

# 初始化一个空数组，用于存储所有处理后的行
all_lines = []

# 读取排除列表文件内容
excudelist_lines = read_txt_to_array('assets/special/ExcludeList.txt')

# 将 M3U 格式内容转换为 TXT 格式的方法
def convert_m3u_to_txt(m3u_content):
    lines = m3u_content
    txt_lines = []
    channel_name = ""

    # 解析 M3U 格式内容
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTM3U"):
            # 如果行以 "#EXTM3U" 开头，跳过（这是 M3U 文件的标识）
            continue
        if line.startswith("#EXTINF"):
            # 如果行以 "#EXTINF" 开头，提取频道名称
            channel_name = line.split(",")[-1].strip()
        elif line.startswith(("http", "https", "rtmp", "p3p", "p2p")):
            # 如果行以 URL 协议开头，将频道名称和 URL 组合成一行并添加到结果中
            txt_lines.append(f"{channel_name},{line}")

    # 将结果数组转换为字符串并返回
    return "\n".join(txt_lines)

# 处理 URL 的方法
def process_url(url):
    try:
        # 创建一个请求对象并添加自定义 header
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # 打开 URL 并读取内容
        with urllib.request.urlopen(req) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            # 将字符串按行拆分为数组
            lines = text.split('\n')

            # 判断是否是 M3U 格式，如果是则特别处理
            if lines[0].strip().startswith("#EXTM3U"):
                # 如果是 M3U 格式，调用转换方法
                newlines = convert_m3u_to_txt(lines)
                # 使用转换后的内容重新赋值给 lines
                lines = newlines.split('\n')

            # 打印处理后的行数
            print(f"行数: {len(lines)}")
            for line in lines:
                line = line.strip()
                # 过滤掉不符合条件的行
                if "#genre#" not in line and "," in line and "://" in line and line not in excudelist_lines:
                    # 将符合条件的行添加到 all_lines 数组中
                    all_lines.append(line.strip())

    except Exception as e:
        # 如果处理 URL 时发生错误，打印错误信息
        print(f"处理URL时发生错误：{e}")

# 定义需要处理的 URL 列表
urls = [
    "https://ua.fongmi.eu.org/box.php?url=https://xn--dkw0c.v.nxog.top/m/tv",
    "https://ua.fongmi.eu.org/box.php?url=http://%E6%88%91%E4%B8%8D%E6%98%AF.%E6%91%B8%E9%B1%BC%E5%84%BF.com/live.php",
    "https://ua.fongmi.eu.org/box.php?url=http://sinopacifichk.com/tv/live",
    "https://ua.fongmi.eu.org/box.php?url=https://tv.iill.top/m3u/Gather",
]

# 遍历 URL 列表并处理每个 URL
for url in urls:
    if url.startswith("http"):
        # 打印当前处理的 URL
        print(f"处理URL: {url}")
        # 调用 process_url 方法处理 URL
        process_url(url)

# 将合并后的文本写入文件
output_file = "assets/special/special.txt"

try:
    # 打开文件并写入所有处理后的行
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    # 打印保存成功的提示信息
    print(f"合并后的文本已保存到文件: {output_file}")
except Exception as e:
    # 如果保存文件时发生错误，打印错误信息
    print(f"保存文件时发生错误：{e}")