import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import subprocess
import os
import webbrowser


class YouGetGui:
    def __init__(self, window):
        self.new_window_var_old = None
        self.root = window

        # 下载Frame
        self.download_frame = tk.Frame(self.root)
        # 下载地址
        self.url_label = tk.Label(self.download_frame, text='下载地址：')
        self.url_label.grid(row=0, column=0)
        self.url_entry = tk.Entry(self.download_frame, width=48)
        self.url_entry.grid(row=0, column=1, columnspan=6)
        self.url_entry_hint = tk.Label(self.download_frame, text='')
        self.url_entry_hint.grid(row=0, column=1, columnspan=6,sticky='w')
        # 清除下载地址
        self.clean = tk.Button(self.download_frame, text='清空', width=8,
                               command=self.clean_url_entry)
        self.clean.grid(row=0, column=7)

        # 下载路径
        self.path_label = tk.Label(self.download_frame, text='下载路径：')
        self.path_label.grid(row=1, column=0)
        self.path_entry = tk.Entry(self.download_frame, width=42)
        self.path_entry.grid(row=1, column=1, columnspan=5)
        self.clean_path = tk.Button(self.download_frame, text='清空', width=6,
                                    command=lambda: self.path_entry.delete(0, tk.END))
        self.clean_path.grid(row=1, column=6)
        self.path_button = tk.Button(self.download_frame, text='选择路径', width=8, command=self.select_path)
        self.path_button.grid(row=1, column=7)

        # 保存文件名
        self.new_name_label = tk.Label(self.download_frame, text='新文件名：')
        self.new_name_label.grid(row=2, column=0)
        self.new_name_entry = tk.Entry(self.download_frame, width=50)
        self.new_name_entry.grid(row=2, column=1, columnspan=6)
        # 清除下载地址
        self.clean_new_name = tk.Button(self.download_frame, text='清空', width=8,
                                        command=lambda: self.new_name_entry.delete(0, tk.END))
        self.clean_new_name.grid(row=2, column=7)

        # 解析更多信息
        self.print_info_frame = tk.Frame(self.download_frame)
        self.more_info_button = tk.Button(self.print_info_frame, text='解析更多信息', width=10, command=self.more_info)
        self.more_info_button.grid(row=0, column=0)
        # 用json格式打印解析的信息
        self.print_info_as_json_var = tkinter.BooleanVar()
        self.print_info_as_json_var.set(False)
        self.print_info_as_json_checkbutton = tk.Checkbutton(self.print_info_frame, text='用json格式打印',
                                                             variable=self.print_info_as_json_var)
        self.print_info_as_json_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
        self.print_info_frame.grid(row=3, column=0, columnspan=3, sticky=tk.E)
        # 解析视频真实地址
        self.real_link_button = tk.Button(self.download_frame, text='解析真实地址', width=10, command=self.real_link)
        self.real_link_button.grid(row=3, column=3)
        # 开始下载按钮
        self.download_button = tk.Button(self.download_frame, text='开始下载', width=7, command=self.lunch_download)
        self.download_button.grid(row=3, column=5)

        # 状态提示
        self.status_label = tk.Label(self.download_frame, text='')
        self.status_label.grid(row=3, column=6, columnspan=2)

        self.download_frame.grid(row=0, column=0, columnspan=8, sticky=tk.W + tk.N)

        # 设置
        self.settings_frame = tk.LabelFrame(self.root, text='设置')
        # 不要下载字幕(字幕，歌词，弹幕，…)
        self.no_download_captions_var = tkinter.BooleanVar()
        self.no_download_captions_var.set(False)
        self.no_download_captions_checkbutton = tk.Checkbutton(self.settings_frame, text='不下载字幕(字幕，歌词，弹幕，…)',
                                                               variable=self.no_download_captions_var)
        self.no_download_captions_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        # 不合并视频片段
        self.merge_video_parts_var = tkinter.BooleanVar()
        self.merge_video_parts_var.set(False)
        self.merge_video_parts_checkbutton = tk.Checkbutton(self.settings_frame, text='不合并视频片段',
                                                            variable=self.merge_video_parts_var)
        self.merge_video_parts_checkbutton.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        # 使用m3u8 url下载视频
        self.download_m3u8_var = tkinter.BooleanVar()
        self.download_m3u8_var.set(False)
        self.download_m3u8_checkbutton = tk.Checkbutton(self.settings_frame, text='使用m3u8 url下载视频',
                                                        variable=self.download_m3u8_var)
        self.download_m3u8_checkbutton.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        # 忽略SSL错误
        self.ignore_ssl_errors_var = tkinter.BooleanVar()
        self.ignore_ssl_errors_var.set(False)
        self.ignore_ssl_errors_checkbutton = tk.Checkbutton(self.settings_frame, text='忽略SSL错误',
                                                            variable=self.ignore_ssl_errors_var)
        self.ignore_ssl_errors_checkbutton.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        # 强制重新下载
        self.forced_download_var = tkinter.BooleanVar()
        self.forced_download_var.set(False)
        self.forced_download_checkbutton = tk.Checkbutton(self.settings_frame,
                                                          text='强制重新下载（覆盖同名文件或临时文件）',
                                                          variable=self.forced_download_var)
        self.forced_download_checkbutton.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        # 自动重命名相同名称的不同文件
        self.auto_rename_var = tkinter.BooleanVar()
        self.auto_rename_var.set(True)
        self.auto_rename_checkbutton = tk.Checkbutton(self.settings_frame, text='自动重命名相同名称的不同文件',
                                                      variable=self.auto_rename_var)
        self.auto_rename_checkbutton.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        # 下载整个播放列表
        self.download_all_var = tkinter.BooleanVar()
        self.download_all_var.set(False)
        self.download_all_checkbutton = tk.Checkbutton(self.settings_frame, text='下载整个播放列表',
                                                       variable=self.download_all_var)
        self.download_all_checkbutton.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        # 开启调试模式
        self.debug_var = tkinter.BooleanVar()
        self.debug_var.set(False)
        self.debug_checkbutton = tk.Checkbutton(self.settings_frame, text='开启调试模式（--debug）', variable=self.debug_var)
        self.debug_checkbutton.grid(row=7, column=0, columnspan=1, sticky=tk.W)
        # 下载标签
        self.download_itag_frame = tk.Frame(self.settings_frame)
        self.download_itag_var = tkinter.BooleanVar()
        self.download_itag_var.set(False)
        self.download_itag_checkbutton = tk.Checkbutton(self.download_itag_frame, text='下载选定标签（itag）',
                                                        variable=self.download_itag_var, command=self.download_itag)
        self.download_itag_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.download_itag_entry = tk.Entry(self.download_itag_frame, width=10, state='disabled')
        self.download_itag_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.download_itag_frame.grid(row=7, column=2, columnspan=3, sticky=tk.W)
        # 使用Cookies
        self.use_cookies_var = tkinter.BooleanVar()
        self.use_cookies_var.set(False)
        self.use_cookies_checkbutton = tk.Checkbutton(self.settings_frame, text='使用Cookies',
                                                      variable=self.use_cookies_var, command=self.use_cookies)
        self.use_cookies_checkbutton.grid(row=8, column=0, columnspan=1, sticky=tk.W)
        self.use_cookies_entry = tk.Entry(self.settings_frame, width=35, state='disabled')
        self.use_cookies_entry.grid(row=8, column=0, columnspan=4)
        self.use_cookies_button = tk.Button(self.settings_frame, text='选择代理文件', command=self.select_cookies_file,
                                            state='disabled')
        self.use_cookies_button.grid(row=8, column=3, sticky=tk.E)
        # 播放视频/音乐
        self.play_var = tkinter.BooleanVar()
        self.play_var.set(False)
        self.play_checkbutton = tk.Checkbutton(self.settings_frame, text='播放视频/音乐',
                                               variable=self.play_var, command=self.use_player)
        self.play_checkbutton.grid(row=9, column=0, columnspan=1, sticky=tk.W)
        self.player_entry = tk.Entry(self.settings_frame, width=30, state='disabled')
        self.player_entry.grid(row=9, column=0, columnspan=4)
        self.play_button = tk.Button(self.settings_frame, text='选择播放器可执行文件', command=self.select_player_file,
                                     state='disabled')
        self.play_button.grid(row=9, column=3, sticky=tk.E)
        # 在新的窗口运行所有命令
        self.new_window_var = tkinter.BooleanVar()
        self.new_window_var.set(True)
        self.new_window_checkbutton = tk.Checkbutton(self.settings_frame,
                                                     text='在新的窗口运行所有命令（推荐）不建议在批量下载中取消勾选，因为没做多'
                                                          '\n线程所以只会在you-get程序执行结束后程序才会接受新的指令（俗称：卡住）',
                                                     height=2,
                                                     variable=self.new_window_var,
                                                     command=self.new_window_var_update)
        self.new_window_checkbutton.grid(row=10, column=0, columnspan=8, sticky=tk.W)
        self.new_window_var_update()

        # 代理选项
        self.proxy_setting = tk.LabelFrame(self.settings_frame, text='代理')
        self.no_proxy_var = tkinter.BooleanVar()
        self.no_proxy_var.set(False)
        self.no_proxy_checkbutton = tk.Checkbutton(self.proxy_setting, text='不使用任何代理（包括系统代理）',
                                                   variable=self.no_proxy_var, command=self.no_proxy_button_check)
        self.no_proxy_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.proxy_setting_var = tkinter.BooleanVar()
        self.proxy_setting_var.set(False)
        self.proxy_setting_checkbutton = tk.Checkbutton(self.proxy_setting, text='使用代理',
                                                        variable=self.proxy_setting_var,
                                                        command=self.proxy_setting_button_check)
        self.proxy_setting_checkbutton.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        self.proxy_path_label = tk.Label(self.proxy_setting, text='代理地址：', fg='gray')
        self.proxy_path_label.grid(row=2, column=0, sticky=tk.W)
        self.proxy_path_entry = tk.Entry(self.proxy_setting, width=20, state='disabled')
        self.proxy_path_entry.grid(row=2, column=0, columnspan=3, sticky=tk.E)

        self.proxy_login_frame = tk.LabelFrame(self.proxy_setting, text='登录', fg='gray')
        self.proxy_login_var = tkinter.BooleanVar()
        self.proxy_login_var.set(False)
        self.proxy_login_checkbutton = tk.Checkbutton(self.proxy_login_frame, text='用户名登录',
                                                      variable=self.proxy_login_var,
                                                      command=self.proxy_login_button_check, state='disabled')
        self.proxy_login_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.proxy_user_name_label = tk.Label(self.proxy_login_frame, text='用户名：', fg='gray')
        self.proxy_user_name_label.grid(row=1, column=0)
        self.proxy_user_name_entry = tk.Entry(self.proxy_login_frame, width=21, state='disabled')
        self.proxy_user_name_entry.grid(row=1, column=1, columnspan=6)
        self.proxy_password_label = tk.Label(self.proxy_login_frame, text='密码：', fg='gray')
        self.proxy_password_label.grid(row=2, column=0)
        self.proxy_password_entry = tk.Entry(self.proxy_login_frame, width=21, state='disabled')
        self.proxy_password_entry.grid(row=2, column=1, columnspan=6)
        self.proxy_login_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        self.proxy_setting.grid(row=0, column=3, rowspan=8, sticky=tk.W + tk.N)
        # 批量下载
        self.batch_download_frame = tk.LabelFrame(self.settings_frame, text='批量功能')
        self.batch_download_power_var = tkinter.BooleanVar()
        self.batch_download_power_var.set(False)
        self.batch_download_power_checkbutton = tk.Checkbutton(self.batch_download_frame, text='使用批量功能',
                                                               variable=self.batch_download_power_var,
                                                               command=self.batch_download_power)
        self.batch_download_power_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.batch_download_parallel_var = tkinter.BooleanVar()
        self.batch_download_parallel_var.set(True)
        self.batch_download_parallel_checkbutton = tk.Checkbutton(self.batch_download_frame, text='同时进行',
                                                                  state='disabled',
                                                                  variable=self.batch_download_parallel_var,
                                                                  command=self.batch_download_parallel)
        self.batch_download_parallel_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
        self.batch_download_from_file_frame = tk.Frame(self.batch_download_frame)
        self.batch_download_from_file_var = tkinter.BooleanVar()
        self.batch_download_from_file_var.set(False)
        self.batch_download_from_file_checkbutton = tk.Checkbutton(self.batch_download_from_file_frame,
                                                                   text='从文件中获取视频地址列表',
                                                                   state='disabled',
                                                                   variable=self.batch_download_from_file_var,
                                                                   command=self.batch_download_from_file_check)
        self.batch_download_from_file_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.batch_download_from_file_select_button = tk.Button(self.batch_download_from_file_frame, text='选择文件',
                                                                state='disabled',
                                                                command=self.batch_download_from_file_select)
        self.batch_download_from_file_select_button.grid(row=0, column=1, columnspan=1)
        self.batch_download_from_file_frame.grid(row=0, column=2, columnspan=6, sticky=tk.W)

        self.batch_download_links_frame = tk.LabelFrame(self.batch_download_frame, text='下载地址列表（一行一个）',
                                                        fg='gray')
        self.batch_download_links_text = tk.Text(self.batch_download_links_frame, wrap='none', fg='gray', height=10,
                                                 width=65, state='disabled')
        self.batch_download_links_scrollbar_x = tk.Scrollbar(self.batch_download_links_frame, orient='horizontal',
                                                             command=self.batch_download_links_text.xview)
        self.batch_download_links_scrollbar_y = tk.Scrollbar(self.batch_download_links_frame, orient='vertical',
                                                             command=self.batch_download_links_text.yview)
        self.batch_download_links_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.batch_download_links_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.batch_download_links_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.batch_download_links_text.config(xscrollcommand=self.batch_download_links_scrollbar_x.set)
        self.batch_download_links_text.config(yscrollcommand=self.batch_download_links_scrollbar_y.set)
        self.batch_download_links_frame.grid(row=2, column=0, rowspan=1, columnspan=8, sticky='nw')

        self.batch_download_frame.grid(row=11, column=0, columnspan=8, sticky=tk.W)
        self.settings_frame.grid(row=1, column=0, columnspan=8, rowspan=999, sticky=tk.W + tk.N)

        # 输出
        self.output_frame = tk.LabelFrame(self.root, text='日志')
        self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, height=40, width=80)
        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)
        self.output_frame.grid(row=0, column=8, rowspan=20, sticky='ne')
        self.output_text_clean = tk.Button(self.root, text='清空日志内容',
                                           command=lambda: self.output_text.delete('1.0', tk.END))
        self.output_text_clean.grid(row=0, column=8, sticky='ne')

        # 提示栏
        self.tips_label = tk.Label(self.root, text='※注意：本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。'
                                                   '\n若无下载路径，则默认下载到"C:/Users/[用户名]"文件夹中。'
                                                   '\n新文件名只要填写名称，无需填写后缀（填写了也没用）。'
                                                   '\n若无新文件名，则程序自动保存为视频原始名称。'
                                                   '\n代理地址必须要同时填写主机地址与端口号。（如：127.0.0.1:00000）'
                                                   '\n若出现报错，请检查你的网络以及填入的参数是否正确并且符合you-get的要求。'
                                                   '\n有的时候软件看上去是卡住了，但其实是在等待you-get程序的反馈，耐心等待即可。'
                                                   '\n若下载时中断，可从重新填入相同的视频地址点击开始下载按键即可继续下载。'
                                                   '\n下载地址列表文件中只能一行一个网址。')
        self.tips_label.grid(row=20, column=8, columnspan=8)

        tk.Label(self.root, text='(c)hunyanjie（魂魇桀） 2024', font=(None, 12, 'bold')).grid(row=21, column=0, columnspan=16)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.about_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="关于", command=self.about)

        self.install_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="一键安装/更新You-Get", command=self.install_you_get)

        self.exit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="退出程序", command=self.exit_program)

    def lunch_download(self, download=True, cmd=''):
        if download:
            cmd = 'you-get'
            if self.path_entry.get() != "":
                cmd += f' -o "{self.path_entry.get()}"'
            if self.new_name_entry.get() != "":
                cmd += f' -O "{self.new_name_entry.get()}"'
            if self.download_itag_var.get():
                if ' --json' not in cmd or ' -i' not in cmd:
                    if self.download_itag_entry.get() != "":
                        cmd += f' --itag {self.download_itag_entry.get()}'
                    else:
                        print('Please enter the itag number!!!')
                        self.status_label.config(text='未填入itag！', fg='red')
                        return
            if self.no_download_captions_var.get():
                cmd += ' --no-merge'
            if self.merge_video_parts_var.get():
                cmd += ' --no-caption'
            if self.download_m3u8_var.get():
                cmd += ' --m3u8'
            if self.ignore_ssl_errors_var.get():
                cmd += ' --insecure'
            if self.forced_download_var.get():
                cmd += ' --force'
            if self.auto_rename_var.get():
                cmd += ' --auto-rename'
            if self.download_all_var.get():
                cmd += ' --playlist'
        if self.debug_var.get():
            cmd += ' --debug'
        if self.use_cookies_var.get():
            if self.use_cookies_entry.get() != '':
                cmd += f' --cookies "{self.use_cookies_entry.get()}"'
            else:
                self.status_label.config(text='未填入cookies路径！', fg='red')
                return
        if self.no_proxy_var.get():
            cmd += ' --no-proxy'
        else:
            if self.proxy_setting_var.get():
                if self.proxy_path_entry.get() != '':
                    if self.proxy_login_var.get():
                        if self.proxy_user_name_entry.get() != '' and self.proxy_password_entry.get() != '':
                            cmd += (f' --socks-proxy {self.proxy_user_name_entry.get()}:'
                                    f'{self.proxy_password_entry.get()}@{self.proxy_path_entry.get()}')
                        else:
                            self.status_label.config(text='请输入代理主机的登入用户名与密码!!', fg='red')
                            return
                    else:
                        cmd += f' --socks-proxy {self.proxy_path_entry.get()}'
                else:
                    self.status_label.config(text='请输入代理主机地址与端口号!!', fg='red')
                    return
        self.start_download(cmd)

    def start_download(self, cmd):
        # 如果使用批量功能
        if self.batch_download_power_var.get():
            # 如果从文件中获取下载连接
            if self.batch_download_from_file_var.get():
                # 检测文件连接是否存在
                if self.url_entry.get() != '':
                    # 如果勾选同时显示
                    if self.batch_download_parallel_var.get():
                        try:
                            with open(f'{self.url_entry.get()}', "r") as file:
                                for line in file:
                                    if line.strip() != '':
                                        self.downloading(f'{cmd} "{line.strip()}"')
                        except FileNotFoundError:
                            print('File does not exist!!!')
                            self.status_label.config(text='文件不存在！', fg='red')
                            return
                    else:
                        self.downloading(f'{cmd} -I "{self.url_entry.get()}"')
                else:
                    print('Please enter the download URL collection file address!!!')
                    self.status_label.config(text='未填入下载网址集合文件地址！', fg='red')
                    return
            else:
                text = self.batch_download_links_text.get("1.0", tk.END)
                if text.strip() != '':
                    # 如果同时下载
                    if self.batch_download_parallel_var.get():
                        for line in text.split('\n'):
                            if line.strip() != '':
                                self.downloading(f'{cmd} "{line.strip()}"')
                    else:
                        open("%TEMP%/YouGetGuiTmpData.tmp", "w").close()
                        with open("%TEMP%/YouGetGuiTmpData.tmp", "w") as file:
                            for line in text:
                                if line.strip() != '':
                                    file.write(line + "\n")
                        self.downloading(f'{cmd} -I "%TEMP%/YouGetGuiTmpData.tmp"')
                        os.remove("%TEMP%/YouGetGuiTmpData.tmp")
                else:
                    print('Please enter the download URL or file path!!!')
                    self.status_label.config(text='未填入下载地址或下载网址集合文件地址！', fg='red')
                    return
        else:
            if self.url_entry.get() == '':
                print('Please enter the download URL!!!')
                self.status_label.config(text='未填入下载地址！', fg='red')
                return
            else:
                cmd += f' "{self.url_entry.get()}"'
                self.downloading(cmd)

    def downloading(self, cmd):
        self.status_label.config(text='已发送下载请求！请等待......', fg='blue')
        if self.new_window_var.get():
            cmd = 'start cmd /k ' + cmd
            print('输入:\n', cmd)
            output_info = f'输入:\n{cmd}\n'
            self.output_text.insert(tk.END, output_info)
            subprocess.Popen(cmd, shell=True)
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, error = process.communicate()
            out = out.decode('utf-8')
            error = error.decode('utf-8')
            print('输出:\n', out)
            print('错误:\n', error)
            output_info = f'输入:\n{cmd}\n输出:\n{out}\n错误:\n{error}\n-------------------------------------\n'
            self.output_text.insert(tk.END, output_info)

    def clean_url_entry(self):
        if self.batch_download_power_var.get() is False and self.batch_download_from_file_checkbutton.cget(
                "state") != 'normal':
            self.url_label.config(text='下载地址：')
        self.url_entry.delete(0, tk.END)

    def select_path(self):
        path = tk.filedialog.askdirectory()
        print(path)
        if path != '':
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def more_info(self):
        if self.print_info_as_json_var.get():
            cmd = f'you-get --json'
        else:
            cmd = f'you-get -i'
        print(cmd)
        self.lunch_download(False, cmd)

    def real_link(self):
        cmd = f'you-get -u'
        print(cmd)
        self.lunch_download(False, cmd)

    def no_proxy_button_check(self):
        if self.no_proxy_var.get():
            self.proxy_setting_checkbutton.config(fg='gray', state='disabled')
            self.proxy_path_label.config(fg='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(fg='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')
        else:
            self.proxy_setting_checkbutton.config(fg='black', state='normal')
            if self.proxy_setting_var.get():
                self.proxy_path_label.config(fg='black')
                self.proxy_path_entry.config(state='normal')
                self.proxy_login_frame.config(fg='black')
                self.proxy_login_checkbutton.config(state='normal')
                if self.proxy_login_var.get():
                    self.proxy_user_name_label.config(fg='black')
                    self.proxy_user_name_entry.config(state='normal')
                    self.proxy_password_label.config(fg='black')
                    self.proxy_password_entry.config(state='normal')
            else:
                self.proxy_path_label.config(fg='gray')
                self.proxy_path_entry.config(state='disabled')
                self.proxy_login_frame.config(fg='gray')
                self.proxy_login_checkbutton.config(state='disabled')
                self.proxy_user_name_label.config(fg='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(fg='gray')
                self.proxy_password_entry.config(state='disabled')

    def proxy_setting_button_check(self):
        if self.proxy_setting_var.get():
            self.proxy_path_label.config(fg='black')
            self.proxy_path_entry.config(state='normal')
            self.proxy_login_frame.config(fg='black')
            self.proxy_login_checkbutton.config(state='normal')
            if self.proxy_login_var.get():
                self.proxy_user_name_label.config(fg='black')
                self.proxy_user_name_entry.config(state='normal')
                self.proxy_password_label.config(fg='black')
                self.proxy_password_entry.config(state='normal')
        else:
            self.proxy_path_label.config(fg='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(fg='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')

    def proxy_login_button_check(self):
        if self.proxy_login_var.get():
            self.proxy_user_name_label.config(fg='black')
            self.proxy_user_name_entry.config(state='normal')
            self.proxy_password_label.config(fg='black')
            self.proxy_password_entry.config(state='normal')
        else:
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')

    def download_itag(self):
        if self.download_itag_var.get():
            self.download_itag_entry.config(state='normal')
        else:
            self.download_itag_entry.config(state='disabled')

    def use_cookies(self):
        if self.use_cookies_var.get():
            self.use_cookies_entry.config(state='normal')
            self.use_cookies_button.config(state='normal')
        else:
            self.use_cookies_entry.config(state='disabled')
            self.use_cookies_button.config(state='disabled')

    def use_player(self):
        if self.play_var.get():
            self.player_entry.config(state='normal')
            self.play_button.config(state='normal')
            self.download_button.config(text='播放', command=self.play)
        else:
            self.player_entry.config(state='disabled')
            self.play_button.config(state='disabled')
            self.download_button.config(text='开始下载', command=self.lunch_download)

    def select_player_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[('播放器EXE文件', ['*.exe']), ('所有文件', '.*')])
        if path != '':
            self.player_entry.delete(0, tk.END)
            self.player_entry.insert(0, path)

    def play(self):
        if self.url_entry.get() != '':
            if self.player_entry.get():
                if self.use_cookies_var.get():
                    if self.use_cookies_entry.get() != '':
                        cmd = (f'you-get --player {self.player_entry.get()} -u {self.url_entry.get()} --cookies '
                               f'{self.use_cookies_var.get()}')
                    else:
                        self.status_label.config(text='未填入Cookie文件地址！', fg='red')
                        return
                else:
                    cmd = f'you-get --player {self.player_entry.get()} -u {self.url_entry.get()}'
            else:
                self.status_label.config(text='未填入播放器可执行程序地址！', fg='red')
                return
        else:
            self.status_label.config(text='未填入视频地址！', fg='red')
            return
        print(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.status_label.config(text='已发送播放请求！请等待......', fg='blue')
        out, error = process.communicate()
        out = out.decode('utf-8')
        error = error.decode('utf-8')
        print('输出:\n', out)
        print('错误：\n', error)
        output_info = f'输出:\n{out}\n错误：\n{error}'
        self.output_text.delete(0.0, tk.END)
        self.output_text.insert(0.0, output_info)

    def select_cookies_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[('Cookies文件', ['*.txt', '*.sqlite']), ('所有文件', '.*')])
        if path != '':
            self.use_cookies_entry.delete(0, tk.END)
            self.use_cookies_entry.insert(0, path)

    def new_window_var_update(self):
        self.new_window_var_old = self.new_window_var.get()

    def batch_download_power(self):
        if self.batch_download_power_var.get():
            self.batch_download_parallel_checkbutton.config(state='normal')
            self.batch_download_from_file_checkbutton.config(state='normal')
            self.batch_download_parallel()
            if self.batch_download_from_file_var.get():
                self.url_entry_hint.config(text='')
                self.url_label.config(text='文件地址：', fg='black')
                self.url_entry.config(state='normal')
                self.batch_download_from_file_select_button.config(state='normal')
            else:
                self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')
                self.url_label.config(text='下载地址：', fg='gray')
                self.url_entry.config(state='disabled')
                self.batch_download_links_frame.config(fg='black')
                self.batch_download_links_text.config(fg='black', state='normal')
        else:
            self.url_entry_hint.config(text='')
            self.url_label.config(text='下载地址：')
            self.url_entry.config(state='normal')
            self.batch_download_from_file_checkbutton.config(state='disabled')
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_parallel_checkbutton.config(state='disabled')
            self.batch_download_parallel()
            self.batch_download_links_frame.config(fg='gray')
            self.batch_download_links_text.config(fg='gray', state='disabled')

    def batch_download_from_file_check(self):
        if self.batch_download_from_file_var.get():
            self.url_entry_hint.config(text='')
            self.url_label.config(text='文件地址：', fg='black')
            self.url_entry.config(state='normal')
            self.batch_download_from_file_select_button.config(state='normal')
            self.batch_download_links_frame.config(fg='gray')
            self.batch_download_links_text.config(fg='gray', state='disabled')
        else:
            self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')
            self.url_label.config(text='下载地址：', fg='gray')
            self.url_entry.config(state='disabled')
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_links_frame.config(fg='black')
            self.batch_download_links_text.config(fg='black', state='normal')

    def batch_download_parallel(self):
        if self.batch_download_parallel_var.get() and self.batch_download_power_var.get():
            self.new_window_var_old = self.new_window_var.get()
            self.new_window_var.set(True)
            self.new_window_checkbutton.config(fg='gray', state='disabled')
        else:
            self.new_window_var.set(self.new_window_var_old)
            self.new_window_checkbutton.config(fg='black', state='normal')

    def batch_download_from_file_select(self):
        path = tk.filedialog.askopenfilename(filetypes=[('网址集合文件', ['*.txt']), ('所有文件', '.*')])
        if path != '':
            self.url_entry_hint.config(text='')
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, path)
        else:
            self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')

    def about(self):

        def open_url(event):
            webbrowser.open('https://github.com/hunyanjie/You-Get-Gui', new=0)

        about_page = tk.Toplevel()
        about_page.title('关于 You-Get GUI v1.0')
        tk.Label(about_page, text='关于', font=(None, 25, 'bold')).pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='注意事项', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, justify=tk.LEFT,
                 text='1、本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。'
                      '\n2、若无下载路径，则默认下载到软件本体所在的文件夹中。'
                      '\n3、新文件名只要填写名称，无需填写后缀（填写了也没用）。'
                      '\n4、若无新文件名，则程序自动保存为视频原始名称。'
                      '\n5、代理地址必须要同时填写主机地址与端口号。（如：127.0.0.1:00000）'
                      '\n6、若出现报错，请检查你的网络以及填入的参数是否正确并且符合you-get的要求。'
                      '\n7、有的时候软件看上去是卡住了，但其实是在等待you-get程序的反馈，耐心等待即可。'
                      '\n8、若下载时中断，可从重新填入相同的视频地址点击开始下载按键即可继续下载。'
                      '\n9、下载地址列表文件中只能一行一个网址。'
                      '\n').pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='更新内容', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, text='初代程序面世').pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='版权', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, text='(c)hunyanjie（魂魇桀） 2024').pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='链接', font=(None, 18, 'bold')).pack()
        link_frame = tk.Frame(about_page)
        tk.Label(link_frame, text='GitHub').grid(row=0, column=0)
        a = tk.StringVar()
        a.set('https://github.com/hunyanjie/You-Get-Gui')
        tk.Entry(link_frame, textvariable=a, state='readonly', width=40).grid(row=0, column=1)
        url = tk.Button(link_frame, text='点击跳转')
        url.grid(row=0, column=2)
        url.bind('<1>', open_url)
        link_frame.pack()

    def install_you_get(self):
        os.system("start cmd /k pip install --upgrade you-get")
        tk.messagebox.showinfo("提示", "已调起You-Get安装程序，请稍等...\n若出现报错，请尝试手动安装You-Get或者在网络上搜索解决方案。")

    def exit_program(self):
        if tk.messagebox.askyesno("提示", "是否退出程序？"):
            self.root.destroy()
            exit()


root = tk.Tk()
root.title('You-get GUI v1.0')
app = YouGetGui(root)
root.mainloop()
