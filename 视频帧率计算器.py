
"""
# -*- coding: utf-8 -*-
Created on 03 27 15:45:00 2023
@Author: yuxi
视频帧率计算器，可以计算视频的帧率、帧数、时间长度，
还可以播放视频，计算视频清晰度，计算最清晰帧，保存最清晰帧。
其中计算视频清晰度的方法有三种，分别是Laplacian算子、Sobel算子和平均梯度。

Attempt Change

"""
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np

class FrameRateCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Frame Rate Calculator")
        master.geometry("800x600")

        self.label = tk.Label(master, text="选择视频文件路径：", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.button = tk.Button(master, text="选择视频文件", font=("Arial", 14), command=self.browse_file)
        self.button.pack(pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.calculate_button = tk.Button(master, text="计算", font=("Arial", 14), command=self.calculate)
        self.calculate_button.pack(pady=10)

        self.play_button = tk.Button(master, text="播放视频", font=("Arial", 14), command=self.play_video)
        self.play_button.pack(pady=10)

        self.clarity_button = tk.Button(master, text="计算最清晰帧", font=("Arial", 14), command=self.calculate_clarity)
        self.clarity_button.pack(pady=10)

        self.max_clarity_label = tk.Label(master, text="", font=("Arial", 14))
        self.max_clarity_label.pack(pady=10)

        self.max_clarity_frame_label = tk.Label(master, text="", font=("Arial", 14))
        self.max_clarity_frame_label.pack(pady=10)

        self.save_button = tk.Button(master, text="保存最清晰帧", font=("Arial", 14), command=self.save_max_clarity_frame)
        self.save_button.pack(pady=10)
        # 将所有按钮和标签的背景颜色、前景颜色和字体设置为红色、白色和Arial 14
        # self.button.config(bg='red', fg='white', font=("Arial", 14))
        # self.calculate_button.config(bg='red', fg='white', font=("Arial", 14))
        # self.play_button.config(bg='red', fg='white', font=("Arial", 14))
        # self.clarity_button.config(bg='red', fg='white', font=("Arial", 14))
        # self.save_button.config(bg='red', fg='white', font=("Arial", 14))
        # self.label.config(bg='red', fg='white', font=("Arial", 14))
        # self.entry.config(bg='red', fg='white', font=("Arial", 14))
        # self.result_label.config(bg='red', fg='white', font=("Arial", 14))
        # self.max_clarity_label.config(bg='red', fg='white', font=("Arial", 14))
        # self.max_clarity_frame_label.config(bg='red', fg='white', font=("Arial", 14))             

        self.master.mainloop()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, file_path)

    def calculate(self):
        video_path = self.entry.get()
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        self.result_label.config(text="帧率: {:.2f} 帧数: {} 时间长度: {:.2f}秒".format(fps, frame_count, duration), font=("Arial", 14))

    def play_video(self):
        video_path = self.entry.get()
        cap = cv2.VideoCapture(video_path)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 800, 500)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('frame',frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

     # 计算视频清晰度
    def calculate_clarity(self):
        video_path = self.entry.get()  # 获取视频路径
        cap = cv2.VideoCapture(video_path)  # 打开视频
        max_clarity = 0  # 初始化最大清晰度
        max_frame = None  # 初始化最清晰帧
        max_frame_num = 0  # 初始化最清晰帧的帧数
        while(cap.isOpened()):  # 循环读取视频帧
            ret, frame = cap.read()  # 读取视频帧
            if ret == True:
                #clarity = cv2.Laplacian(frame, cv2.CV_64F).var()  # 计算帧的清晰度
                
                # 计算帧的清晰度
                '''sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
                sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
                sobel = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
                clarity = sobel.var() 
                '''
                # 计算帧的清晰度
                sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=3)
                sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=3)
                mean_gradient = np.mean(np.sqrt(sobelx**2 + sobely**2))
                clarity = mean_gradient
 
                
                if clarity > max_clarity:  # 如果当前帧的清晰度大于最大清晰度
                    max_clarity = clarity  # 更新最大清晰度
                    max_frame = frame  # 更新最清晰帧
                    max_frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))  # 更新最清晰帧的帧数
            else:
                break
        cap.release()  # 释放视频

        self.max_clarity_label.config(text="最清晰帧的清晰度: {:.2f}".format(max_clarity), font=("Arial", 14))
        
        self.max_clarity_frame_label.config(text="最清晰帧的信息: 帧数{}".format(max_frame_num), font=("Arial", 14))
        self.max_frame = max_frame

    def save_max_clarity_frame(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("BMP Image", "*.bmp"),("TIF Image", "*.tif")])
        if file_path:
            cv2.imwrite(file_path, self.max_frame)
               

FrameRateCalculator(tk.Tk())

