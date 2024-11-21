import os
import sys

# 获取当前文件的目录路径
BaseDir = os.path.dirname(os.path.abspath(__file__))
# 将当前文件的目录路径添加到系统路径中
sys.path.append(BaseDir)

import tkinter as tk
from tkinter import messagebox
import requests
import json
import datetime
import threading
import os

class BugFetcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bug Fetcher")

        # 配置文件路径
        self.config_file = "config.json"

        # 初始化配置变量
        self.zentao_url = tk.StringVar()
        self.zentao_username = tk.StringVar()
        self.zentao_password = tk.StringVar()
        self.feishu_webhook_url = tk.StringVar()
        self.fetch_interval = tk.IntVar(value=60)  # 默认每60分钟
        self.zentao_token = tk.StringVar()
        self.selected_product = tk.StringVar()
        self.selected_product_id = tk.StringVar()
        self.user_realname = tk.StringVar()

        # 创建UI
        self.create_widgets()

        # 加载配置
        self.load_config()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        # 创建并布局各个输入框和标签
        tk.Label(frame, text="ZenTao URL:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.zentao_url_entry = tk.Entry(frame, textvariable=self.zentao_url)
        self.zentao_url_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="ZenTao Username:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.zentao_username_entry = tk.Entry(frame, textvariable=self.zentao_username)
        self.zentao_username_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="ZenTao Password:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.zentao_password_entry = tk.Entry(frame, textvariable=self.zentao_password, show="*")
        self.zentao_password_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)
        self.show_password_var = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_checkbutton.grid(row=2, column=2, sticky=tk.W, pady=2)

        tk.Label(frame, text="Feishu Webhook URL:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.feishu_webhook_url_entry = tk.Entry(frame, textvariable=self.feishu_webhook_url)
        self.feishu_webhook_url_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="Fetch Interval (minutes):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.fetch_interval_entry = tk.Entry(frame, textvariable=self.fetch_interval)
        self.fetch_interval_entry.grid(row=4, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="ZenTao Token:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.zentao_token_entry = tk.Entry(frame, textvariable=self.zentao_token)
        self.zentao_token_entry.grid(row=5, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="User Realname:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.user_realname_entry = tk.Entry(frame, textvariable=self.user_realname, state='readonly')
        self.user_realname_entry.grid(row=6, column=1, sticky=tk.EW, pady=2)

        tk.Label(frame, text="Selected Product:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.selected_product_entry = tk.Entry(frame, textvariable=self.selected_product, state='readonly')
        self.selected_product_entry.grid(row=7, column=1, sticky=tk.EW, pady=2)

        self.login_button = tk.Button(frame, text="Login to ZenTao", command=self.login_to_zentao)
        self.login_button.grid(row=8, column=0, columnspan=2, pady=5)
        self.start_fetch_button = tk.Button(frame, text="Start Fetching", command=self.toggle_fetching)
        self.start_fetch_button.grid(row=9, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Save Config", command=self.save_config).grid(row=10, column=0, columnspan=2, pady=5)

        # 日志显示框
        self.log_text = tk.Text(frame, height=10, state='disabled')
        self.log_text.grid(row=11, column=0, columnspan=2, pady=5)

        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

    def toggle_password_visibility(self):
        # 切换密码可见性
        if self.show_password_var.get():
            self.zentao_password_entry.config(show="")
        else:
            self.zentao_password_entry.config(show="*")

    def log_message(self, message):
        # 记录日志信息
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{datetime.datetime.now()}: {message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def load_config(self):
        # 加载配置文件
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.zentao_url.set(config.get("zentao_url", ""))
                self.zentao_username.set(config.get("zentao_username", ""))
                self.zentao_password.set(config.get("zentao_password", ""))
                self.feishu_webhook_url.set(config.get("feishu_webhook_url", ""))
                self.fetch_interval.set(config.get("fetch_interval", 60))
                self.zentao_token.set(config.get("zentao_token", ""))
                self.selected_product.set(config.get("selected_product", ""))
                self.selected_product_id.set(config.get("selected_product_id", ""))
        self.log_message("配置已加载")

    def save_config(self):
        # 保存配置文件
        config = {
            "zentao_url": self.zentao_url.get(),
            "zentao_username": self.zentao_username.get(),
            "zentao_password": self.zentao_password.get(),
            "feishu_webhook_url": self.feishu_webhook_url.get(),
            "fetch_interval": self.fetch_interval.get(),
            "zentao_token": self.zentao_token.get(),
            "selected_product": self.selected_product.get(),
            "selected_product_id": self.selected_product_id.get()
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        self.log_message("配置已保存")

    def login_to_zentao(self):
        # 登录到ZenTao
        self.zentao_url_value = self.zentao_url.get()
        self.zentao_username_value = self.zentao_username.get()
        self.zentao_password_value = self.zentao_password.get()
        self.zentao_token_value = self.zentao_token.get()

        if not self.zentao_url_value or not self.zentao_username_value or not self.zentao_password_value:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.zentao_token_value:
            self.zentao_token_value = self.get_zentao_token()
            if not self.zentao_token_value:
                messagebox.showerror("Error", "Failed to login to ZenTao!")
                return

        self.zentao_token.set(self.zentao_token_value)
        self.save_config()
        self.login_button.grid_remove()
        self.log_message("Login successful!")
        self.fetch_user_info()
        self.fetch_products()

    def fetch_user_info(self):
        # 获取用户信息
        headers = {
            "Content-Type": "application/json",
            "Token": f"{self.zentao_token_value}"
        }
        response = requests.get(f"{self.zentao_url_value}/api.php/v1/user", headers=headers)
        self.log_message(f"获取用户信息: {response.text} code: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json().get("profile", {})
            self.user_realname.set(user_info.get("realname", ""))
            self.log_message(f"获取用户信息: {self.user_realname.get()}")
        else:
            self.log_message(f"Failed to fetch user info: {response.text}")
            messagebox.showerror("Error", f"Failed to fetch user info: {response.text}")

    def fetch_products(self):
        # 获取产品列表
        headers = {
            "Content-Type": "application/json",
            "Token": f"{self.zentao_token_value}"
        }
        response = requests.get(f"{self.zentao_url_value}/api.php/v1/products", headers=headers)
        if response.status_code == 200:
            products = response.json().get("products", [])
            self.show_product_selection(products)
        else:
            if response.status_code == 401 and response.json().get("error") == "Unauthorized":
                self.zentao_token_value = self.get_zentao_token()
                if self.zentao_token_value:
                    self.zentao_token.set(self.zentao_token_value)
                    self.save_config()
                    self.fetch_products()
                else:
                    messagebox.showerror("Error", "Failed to login to ZenTao!")
            else:
                self.log_message(f"Failed to fetch products: {response.text}")
                messagebox.showerror("Error", f"Failed to fetch products: {response.text}")

    def show_product_selection(self, products):
        # 显示产品选择窗口
        product_names = [product['name'] for product in products]
        self.product_selection_window = tk.Toplevel(self.root)
        self.product_selection_window.title("Select Product")
        tk.Label(self.product_selection_window, text="Select a product:").pack(pady=5)
        self.product_listbox = tk.Listbox(self.product_selection_window)
        self.product_listbox.pack(pady=5)
        for name in product_names:
            self.product_listbox.insert(tk.END, name)
        tk.Button(self.product_selection_window, text="Confirm", command=lambda: self.confirm_product_selection(products)).pack(pady=5)

    def confirm_product_selection(self, products):
        # 确认产品选择
        selected_index = self.product_listbox.curselection()
        if selected_index:
            selected_product_name = self.product_listbox.get(selected_index)
            self.selected_product.set(selected_product_name)
            for product in products:
                if product['name'] == selected_product_name:
                    self.selected_product_id.set(product['id'])
                    break
            self.product_selection_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a product!")

    def toggle_fetching(self):
        # 切换获取状态
        if self.start_fetch_button["text"] == "Start Fetching":
            self.start_fetching()
        else:
            self.stop_fetching()

    def start_fetching(self):
        # 开始获取新Bug
        self.feishu_webhook_url_value = self.feishu_webhook_url.get()
        self.fetch_interval_value = self.fetch_interval.get()

        if not self.feishu_webhook_url_value:
            messagebox.showerror("Error", "Feishu Webhook URL is required!")
            return

        if not hasattr(self, 'zentao_token_value') or not self.zentao_token_value:
            self.zentao_token_value = self.zentao_token.get()
            if not self.zentao_token_value:
                messagebox.showerror("Error", "Please login to ZenTao first!")
                return

        if not self.selected_product.get():
            messagebox.showerror("Error", "Please select a product first!")
            return

        self.save_config()
        self.log_message("开始获取新Bug")
        self.fetch_new_bugs()
        self.schedule_next_fetch()

        # 禁用所有输入框
        self.zentao_url_entry.config(state='disabled')
        self.zentao_username_entry.config(state='disabled')
        self.zentao_password_entry.config(state='disabled')
        self.feishu_webhook_url_entry.config(state='disabled')
        self.fetch_interval_entry.config(state='disabled')
        self.zentao_token_entry.config(state='disabled')
        self.user_realname_entry.config(state='disabled')
        self.selected_product_entry.config(state='disabled')

        # 更改按钮文本
        self.start_fetch_button.config(text="Stop Fetching")

    def stop_fetching(self):
        # 停止获取新Bug
        if hasattr(self, 'fetching_job'):
            self.root.after_cancel(self.fetching_job)
            self.log_message("停止获取新Bug")

        # 启用所有输入框
        self.zentao_url_entry.config(state='normal')
        self.zentao_username_entry.config(state='normal')
        self.zentao_password_entry.config(state='normal')
        self.feishu_webhook_url_entry.config(state='normal')
        self.fetch_interval_entry.config(state='normal')
        self.zentao_token_entry.config(state='normal')
        self.user_realname_entry.config(state='normal')
        self.selected_product_entry.config(state='normal')

        # 更改按钮文本
        self.start_fetch_button.config(text="Start Fetching")

    def get_zentao_token(self):
        # 获取ZenTao Token
        self.log_message("开始获取Token")
        login_url = f"{self.zentao_url_value}/api.php/v1/tokens"
        payload = {
            "account": self.zentao_username_value,
            "password": self.zentao_password_value
        }
        response = requests.post(login_url, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            return response.json().get('token')
        else:
            self.log_message(f"Failed to get token: {response.text} code: {response.status_code}")
            return None

    def fetch_new_bugs(self):
        # 获取新Bug
        self.log_message("开始获取新Bug")
        headers = {
            "Content-Type": "application/json",
            "Token": f"{self.zentao_token_value}"
        }
        product_id = self.selected_product_id.get()
        response = requests.get(f"{self.zentao_url_value}/api.php/v1/products/{product_id}/bugs", headers=headers)
        if response.status_code == 200:
            # 从返回的 JSON 中提取 bugs 字段
            bugs = response.json().get("bugs", [])
            self.log_message(f"获取到的Bug数量: {len(bugs)}")
            # 筛选指派给当前用户的未解决的 bug
            unresolved_bugs = [bug for bug in bugs if bug['status'] != 'resolved' and bug['assignedTo']['account'] == self.zentao_username_value]
            self.log_message(f"未解决的Bug数量: {len(unresolved_bugs)}")
            if unresolved_bugs:
                self.send_to_feishu(unresolved_bugs)
        else:
            if response.status_code == 401 and response.json().get("error") == "Unauthorized":
                self.zentao_token_value = self.get_zentao_token()
                if self.zentao_token_value:
                    self.zentao_token.set(self.zentao_token_value)
                    self.save_config()
                    self.fetch_new_bugs()
                else:
                    self.log_message(f"Failed to fetch bugs: {response.text}")
            else:
                self.log_message(f"Failed to fetch bugs: {response.text}")

    def send_to_feishu(self, bugs):
        # 发送Bug信息到飞书
        if not self.feishu_webhook_url_value:
            self.log_message("Feishu Webhook URL is not set. Here are the bugs:")
            for bug in bugs:
                self.log_message(f"Bug ID: {bug['id']}, Title: {bug['title']}, Assigned To: {bug['assignedTo']}")
            return
        
        bug_details = "\n".join([f"{bug['id']}: {bug['title']}" for bug in bugs])
        product_id = self.selected_product_id.get()
        zentao_url = self.zentao_url_value
        message = {
            "msg_type": "text",
            "content": {
                "text": f"新Bug报告:\n{bug_details}\n\n查看我的Bug: [点击这里]({zentao_url}/index.php?m=bug&f=browse&product={product_id}&branch=all&browseType=assigntome&param=0&orderBy=status_asc)"
            }
        }
        response = requests.post(self.feishu_webhook_url_value, headers={"Content-Type": "application/json"}, data=json.dumps(message))
        if response.status_code != 200:
            self.log_message(f"Failed to send message to Feishu: {response.text}")

    def schedule_next_fetch(self):
        # 安排下次获取
        interval_ms = self.fetch_interval_value * 60000  # 转换为毫秒
        self.log_message(f"下次获取将在 {self.fetch_interval_value} 分钟后进行")
        self.fetching_job = self.root.after(interval_ms, self.fetch_new_bugs)  # 根据用户设置的间隔时间运行

if __name__ == "__main__":
    root = tk.Tk()
    app = BugFetcherApp(root)
    root.mainloop()