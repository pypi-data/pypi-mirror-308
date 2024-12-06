import os
import sys
import argparse
import subprocess
#from .global_config import DRIVER

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


# ========================

def report(shell: str):
  process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

  stdout, stderr = process.communicate()

  print(stdout)

  #result = subprocess.run(shell, shell=True, capture_output=True, text=True)
  #print(result.stdout)
# ========================
from urllib.request import urlretrieve
# 文件的URL
driver_url = "https://oss.mthreads.com/product-release/release_kuae1.3.0_musa3.1.0/External/musa_2.7.0-rc3-0822_Ubuntu_amd64.deb"
sgpu_url = "https://oss.mthreads.com/product-release/release_kuae1.3.0_musa3.1.0/External/sgpu-dkms_1.2.1_amd64.deb"
gmi_url = "https://oss.mthreads.com/product-release/release_kuae1.3.0_musa3.1.0/External/429b0f7c0_mthreads-gmi_1.14.0.tar.gz"
mtml_url = "https://oss.mthreads.com/product-release/release_kuae1.3.0_musa3.1.0/External/384c16a70_mtml_1.14.0-linux-R_amd64.deb"

def download(file_url: str, file_name: str):
    DOWNLOAD_DIR="/tmp/"
    # 下载文件
    file_path = DOWNLOAD_DIR + file_name

    if os.path.exists(file_path):
        os.remove(file_path)

    print(f"start downloading " + file_name + " ......")
    try:
        urlretrieve(file_url, file_path)
        print(Style.GREEN + "downloading " + file_name + " to /tmp done!" + Style.RESET)
    except Exception as e:
        print(f"下载失败：{e}")
# ========================
def exec_shell(command):
  import subprocess
  #process = subprocess.Popen("sudo dpkg -r musa && sudo dpkg -P musa && sudo dpkg -i /tmp/musa_2.7.0-rc3-0822_Ubuntu_amd64.deb", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
          break
      if output:
          print(output.strip())
  process.wait()
  

class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GREEN = "\033[32m"
    RED = "\033[31m"

# ========================

def main():
    parser = argparse.ArgumentParser(
        prog="musa-develop", description="A tool for deploying and checking the musa environment.")
    parser.add_argument("--check", dest="check", action="store_true", default=False, help="check environment")
    parser.add_argument("--report", dest="report", action="store_true", default=False,
                        help="Display the software stack and hardware information of the current environment.")
    parser.add_argument("--install", dest="install", type=str, default="",
                        help="Deploy the musa base software stack.")
    parser.add_argument("--force_upgrade_musa", dest="force_upgrade_musa", action="store_true", default=False,
                        help="Force update the musa software stack.")
    parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="Print verbose")
    # 解析命令行参数
    args = parser.parse_args()

    if args.report:
        report("bash " + CURRENT_FOLDER + "/temp/musa_report.sh")
        
    if args.install == "kuae1.3":
        # download
        download(driver_url, "musa_2.7.0-rc3-0822_Ubuntu_amd64.deb")
        download(sgpu_url, "sgpu-dkms_1.2.1_amd64.deb")
        download(gmi_url, "429b0f7c0_mthreads-gmi_1.14.0.tar.gz")
        download(mtml_url, "384c16a70_mtml_1.14.0-linux-R_amd64.deb")

        print("===== start install DRIVER =====")
        exec_shell("sudo dpkg -r musa && sudo dpkg -P musa && sudo dpkg -i /tmp/musa_2.7.0-rc3-0822_Ubuntu_amd64.deb")
        print(Style.GREEN + "===== installation of DRIVER is done!=====" + Style.RESET)
        print("===== start install SGPU =====")
        exec_shell("sudo dpkg -i /tmp/sgpu-dkms_1.2.1_amd64.deb")
        print(Style.GREEN + "===== installation of SGPU is done!=====" + Style.RESET)
        print("===== start install MTML =====")
        exec_shell("sudo dpkg -i /tmp/384c16a70_mtml_1.14.0-linux-R_amd64.deb")
        print(Style.GREEN + "===== installation of MTML is done!=====" + Style.RESET)





if __name__ == '__main__':
    main()
