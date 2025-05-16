"""
@file test_maxspeed.py
@Description: カメラを最高速度で動作させるスクリプト
"""

import sys
import os

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from siyi_sdk import SIYISDK
from time import sleep

def move_gimbal_max_speed():
    # SIYISDKインスタンスを作成
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)
    
    # カメラに接続
    if not cam.connect():
        print("カメラに接続できませんでした")
        return

    try:
        print("カメラを最高速度で動作させます")

        # YawとPitchを最高速度で動作させる
        cam.requestGimbalSpeed(100, 100)  # Yaw: 100, Pitch: 100
        sleep(3)  # 3秒間動作

        # 動作を停止
        cam.requestGimbalSpeed(0, 0)  # 停止
        print("カメラの動作を停止しました")

    finally:
        # カメラとの接続を切断
        cam.disconnect()

if __name__ == "__main__":
    move_gimbal_max_speed()