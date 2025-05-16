"""
@file aks_A8mini_PID.py
@Description: PID制御を用いてカメラを目標位置に移動させるスクリプト
"""

import sys
import os
import time

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from siyi_sdk import SIYISDK

# PID制御のゲイン
YAW_P_GAIN = 3.0
YAW_I_GAIN = 0.0
YAW_D_GAIN = 0.0

PITCH_P_GAIN = 3.0
PITCH_I_GAIN = 0.01
PITCH_D_GAIN = 0.05

# 初期目標位置（yaw, pitch）
TARGET_YAW = 0.0  # 初期目標のyaw角度
TARGET_PITCH = 0.0  # 初期目標のpitch角度

def pid_control():
    global TARGET_YAW, TARGET_PITCH  # グローバル変数として目標角度を扱う
    cam = SIYISDK(server_ip="192.168.144.25", port=37260)
    if not cam.connect():
        print("カメラに接続できませんでした")
        return

    # PID制御用の変数
    yaw_integral = 0.0
    pitch_integral = 0.0
    prev_yaw_error = 0.0
    prev_pitch_error = 0.0
    prev_time = time.time()  # 初期時刻を取得

    try:
        while True:
            # 現在の時刻を取得
            current_time = time.time()
            dt = current_time - prev_time  # 時間差を計算

            # 現在の姿勢を取得
            current_yaw, current_pitch, _ = cam.getAttitude()

            # yawとpitchの誤差を計算
            yaw_error = TARGET_YAW - current_yaw
            pitch_error = TARGET_PITCH - current_pitch

            # 台形積分を使用して積分項を計算
            yaw_integral += (yaw_error + prev_yaw_error) * dt / 2
            pitch_integral += (pitch_error + prev_pitch_error) * dt / 2

            # 微分項の計算
            yaw_derivative = (yaw_error - prev_yaw_error) / dt
            pitch_derivative = (pitch_error - prev_pitch_error) / dt

            # PID制御による速度指令値を計算
            yaw_speed = int(
                YAW_P_GAIN * yaw_error +
                YAW_I_GAIN * yaw_integral +
                YAW_D_GAIN * yaw_derivative
            )
            pitch_speed = int(
                PITCH_P_GAIN * pitch_error +
                PITCH_I_GAIN * pitch_integral +
                PITCH_D_GAIN * pitch_derivative
            )

            # カメラに速度指令を送信
            cam.requestGimbalSpeed(yaw_speed, pitch_speed)

            # 誤差が十分小さくなったら終了
            if abs(yaw_error) < 0.5 and abs(pitch_error) < 0.5:
                print("目標位置に到達しました")

            # 前回の誤差と時刻を更新
            prev_yaw_error = yaw_error
            prev_pitch_error = pitch_error
            prev_time = current_time

            # ユーザーから新しい目標角度を入力
            try:
                new_yaw = input("新しいYaw角度を入力してください（現在の目標: {}）: ".format(TARGET_YAW))
                new_pitch = input("新しいPitch角度を入力してください（現在の目標: {}）: ".format(TARGET_PITCH))
                if new_yaw.strip():
                    TARGET_YAW = float(new_yaw)
                if new_pitch.strip():
                    TARGET_PITCH = float(new_pitch)
            except ValueError:
                print("無効な入力です。角度は数値で入力してください。")

            # 少し待機
            time.sleep(0.1)

    finally:
        # カメラとの接続を切断
        cam.disconnect()

if __name__ == "__main__":
    pid_control()