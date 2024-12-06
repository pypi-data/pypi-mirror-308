import subprocess

def ping(url):
    # 参数解析：'-n' 表示发送的echo请求的次数，'-w' 表示等待回复的超时时间（毫秒）
    # 这些参数在不同的操作系统中可能有所不同，这里以Windows为例
    parameter = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', parameter, '1', url]  # 对URL执行一次ping操作

    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # ping命令执行成功，返回码为0
        if response.returncode == 0:
            print(f"Ping {url} successful")
            return True
        else:
            print(f"Ping {url} failed")
            return False
    except Exception as e:
        print(f"Error pinging {url}: {e}")
        return False

# 使用示例
ping_result = ping("google.com")
print(f"Can ping google.com: {ping_result}")
