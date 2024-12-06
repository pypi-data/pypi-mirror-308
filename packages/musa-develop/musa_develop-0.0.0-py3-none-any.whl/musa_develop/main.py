import os
import sys
import argparse
import subprocess
from .global_config import DRIVER

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


# ========================

def report(shell: str):
  process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

  stdout, stderr = process.communicate()

  print(stdout)

  #result = subprocess.run(shell, shell=True, capture_output=True, text=True)
  #print(result.stdout)
# ========================



def main():
    parser = argparse.ArgumentParser(
        prog="musa-develop", description="A tool for deploying and checking the musa environment.")
    parser.add_argument("--check", dest="check", action="store_true", default=False, help="check environment")
    parser.add_argument("--report", dest="report", action="store_true", default=False,
                        help="Display the software stack and hardware information of the current environment.")
    parser.add_argument("--install", dest="install", type=str, default="kuae1.3",
                        help="Deploy the musa base software stack.")
    parser.add_argument("--force_upgrade_musa", dest="force_upgrade_musa", action="store_true", default=False,
                        help="Force update the musa software stack.")
    parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="Print verbose")
    # 解析命令行参数
    args = parser.parse_args()

    if args.report:
        report("bash " + CURRENT_FOLDER + "/temp/musa_report.sh")






if __name__ == '__main__':
    main()
