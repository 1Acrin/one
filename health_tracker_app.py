import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import json
import os
from tkcalendar import DateEntry  # 需要安装：pip install tkcalendar


class HealthTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("健康追踪应用")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure(".", font=("SimHei", 10))

        self.data_file = "health_data.json"
        self.load_data()

        self.create_main_frame()

    def load_data(self):
        """加载已保存的数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'bmi_records': [],
                'calorie_intake': {},
                'bmr_records': []
            }

    def save_data(self):
        """保存数据到文件"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_main_frame(self):
        """创建主界面"""
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="健康追踪应用",
            font=("SimHei", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=30)

        # 功能按钮框架
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(expand=True)

        # 按钮样式
        button_style = {
            "font": ("SimHei", 12),
            "width": 25,
            "height": 2,
            "bg": "#4CAF50",
            "fg": "white",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2"
        }

        # BMI计算按钮
        bmi_btn = tk.Button(
            button_frame,
            text="BMI计算与记录",
            command=self.open_bmi_frame,
            **button_style
        )
        bmi_btn.grid(row=0, column=0, padx=20, pady=15)

        # 能量摄入按钮
        calorie_btn = tk.Button(
            button_frame,
            text="食物能量摄入记录",
            command=self.open_calorie_frame,
            **button_style
        )
        calorie_btn.grid(row=0, column=1, padx=20, pady=15)

        # 代谢率计算按钮
        bmr_btn = tk.Button(
            button_frame,
            text="基础代谢率计算",
            command=self.open_bmr_frame,
            **button_style
        )
        bmr_btn.grid(row=1, column=0, padx=20, pady=15)

        # 热量平衡分析按钮 - 新增
        balance_btn = tk.Button(
            button_frame,
            text="热量摄入与消耗分析",
            command=self.open_calorie_balance_frame,
            **button_style
        )
        balance_btn.grid(row=1, column=1, padx=20, pady=15)

        # 历史记录按钮
        history_btn = tk.Button(
            button_frame,
            text="查看历史记录",
            command=self.open_history_frame,
            **button_style
        )
        history_btn.grid(row=2, column=0, padx=20, pady=15, columnspan=2)

        # 退出按钮
        exit_btn = tk.Button(
            self.root,
            text="退出",
            command=self.root.quit,
            font=("SimHei", 10),
            width=10,
            bg="#f44336",
            fg="white"
        )
        exit_btn.pack(side=tk.BOTTOM, pady=20)

    # BMI相关功能
    def open_bmi_frame(self):
        """打开BMI计算界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="BMI计算与记录",
            font=("SimHei", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # 输入框架
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=20)

        # 体重输入
        tk.Label(
            input_frame,
            text="体重 (kg):",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.weight_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        # 身高输入
        tk.Label(
            input_frame,
            text="身高 (cm):",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.height_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        # 结果显示
        self.bmi_result_var = tk.StringVar()
        result_label = tk.Label(
            self.root,
            textvariable=self.bmi_result_var,
            font=("SimHei", 14),
            bg="#f0f0f0",
            fg="#2196F3"
        )
        result_label.pack(pady=20)

        # 按钮框架
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        # 计算按钮
        calc_btn = tk.Button(
            btn_frame,
            text="计算BMI",
            command=self.calculate_and_record_bmi,
            font=("SimHei", 12),
            width=15,
            bg="#2196F3",
            fg="white"
        )
        calc_btn.grid(row=0, column=0, padx=10)

        # 返回按钮
        back_btn = tk.Button(
            btn_frame,
            text="返回主菜单",
            command=self.create_main_frame,
            font=("SimHei", 12),
            width=15,
            bg="#f44336",
            fg="white"
        )
        back_btn.grid(row=0, column=1, padx=10)

    def calculate_and_record_bmi(self):
        """计算并记录BMI"""
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("输入错误", "体重和身高必须为正数")
                return

            # 计算BMI
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 1)

            # 确定BMI类别
            if bmi < 18.5:
                category = "偏瘦"
            elif 18.5 <= bmi < 24:
                category = "正常"
            elif 24 <= bmi < 28:
                category = "超重"
            else:
                category = "肥胖"

            # 显示结果
            self.bmi_result_var.set(f"BMI值: {bmi} ({category})")

            # 记录数据
            record = {
                'date': datetime.date.today().isoformat(),
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'category': category
            }

            self.data['bmi_records'].append(record)
            self.save_data()
            messagebox.showinfo("成功", "BMI记录已保存")

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    # 能量摄入相关功能
    def open_calorie_frame(self):
        """打开能量摄入记录界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="食物能量摄入记录",
            font=("SimHei", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # 日期选择
        date_frame = tk.Frame(self.root, bg="#f0f0f0")
        date_frame.pack(pady=10)

        tk.Label(
            date_frame,
            text="选择日期:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        self.calorie_date = DateEntry(
            date_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.calorie_date.pack(side=tk.LEFT, padx=10)

        # 输入框架
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # 食物名称输入
        tk.Label(
            input_frame,
            text="食物名称:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.food_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=20
        )
        self.food_entry.grid(row=0, column=1, padx=10, pady=10)

        # 卡路里输入
        tk.Label(
            input_frame,
            text="能量 (卡路里):",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.calorie_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.calorie_entry.grid(row=1, column=1, padx=10, pady=10)

        # 按钮框架
        btn_frame1 = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame1.pack(pady=10)

        # 添加按钮
        add_btn = tk.Button(
            btn_frame1,
            text="添加记录",
            command=self.add_calorie_record,
            font=("SimHei", 12),
            width=15,
            bg="#2196F3",
            fg="white"
        )
        add_btn.pack(side=tk.LEFT, padx=10)

        # 查看按钮
        view_btn = tk.Button(
            btn_frame1,
            text="查看当日记录",
            command=self.view_calorie_records,
            font=("SimHei", 12),
            width=15,
            bg="#4CAF50",
            fg="white"
        )
        view_btn.pack(side=tk.LEFT, padx=10)

        # 记录列表
        tk.Label(
            self.root,
            text="当日记录:",
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0"
        ).pack(pady=5, anchor="w", padx=50)

        self.calorie_listbox = tk.Listbox(
            self.root,
            width=70,
            height=8,
            font=("SimHei", 10)
        )
        self.calorie_listbox.pack(pady=10)

        # 热量平衡显示 - 新增
        self.calorie_balance_var = tk.StringVar()
        balance_label = tk.Label(
            self.root,
            textvariable=self.calorie_balance_var,
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0",
            fg="#FF5722"
        )
        balance_label.pack(pady=5)

        # 总计显示
        self.calorie_total_var = tk.StringVar()
        total_label = tk.Label(
            self.root,
            textvariable=self.calorie_total_var,
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0",
            fg="#FF9800"
        )
        total_label.pack(pady=5)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="返回主菜单",
            command=self.create_main_frame,
            font=("SimHei", 12),
            width=15,
            bg="#f44336",
            fg="white"
        )
        back_btn.pack(side=tk.BOTTOM, pady=20)

        # 初始加载记录
        self.view_calorie_records()

    def add_calorie_record(self):
        """添加食物能量记录"""
        try:
            food = self.food_entry.get().strip()
            calories = int(self.calorie_entry.get())
            date = self.calorie_date.get()

            if not food:
                messagebox.showerror("输入错误", "请输入食物名称")
                return

            if calories <= 0:
                messagebox.showerror("输入错误", "卡路里必须为正数")
                return

            if date not in self.data['calorie_intake']:
                self.data['calorie_intake'][date] = []

            self.data['calorie_intake'][date].append({
                'food': food,
                'calories': calories
            })

            self.save_data()
            messagebox.showinfo("成功", f"已添加：{food} ({calories} 卡路里)")

            # 清空输入框
            self.food_entry.delete(0, tk.END)
            self.calorie_entry.delete(0, tk.END)

            # 刷新列表和热量平衡
            self.view_calorie_records()

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的卡路里数值")

    def view_calorie_records(self):
        """查看当日能量摄入记录，并计算热量平衡"""
        date = self.calorie_date.get()

        # 清空列表
        self.calorie_listbox.delete(0, tk.END)

        if date not in self.data['calorie_intake'] or not self.data['calorie_intake'][date]:
            self.calorie_listbox.insert(tk.END, "当日暂无记录")
            self.calorie_total_var.set("总计：0 卡路里")
            self.calorie_balance_var.set("热量平衡：暂无数据（请先计算代谢率）")
            return

        records = self.data['calorie_intake'][date]
        total_intake = sum(item['calories'] for item in records)

        for item in records:
            self.calorie_listbox.insert(tk.END, f"{item['food']}: {item['calories']} 卡路里")

        self.calorie_total_var.set(f"总计摄入：{total_intake} 卡路里")

        # 计算热量平衡
        self.calculate_calorie_balance(date, total_intake)

    # 新增：热量平衡分析功能
    def open_calorie_balance_frame(self):
        """打开热量摄入与消耗分析界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="热量摄入与消耗分析",
            font=("SimHei", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # 日期选择
        date_frame = tk.Frame(self.root, bg="#f0f0f0")
        date_frame.pack(pady=20)

        tk.Label(
            date_frame,
            text="选择日期:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        self.balance_date = DateEntry(
            date_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.balance_date.pack(side=tk.LEFT, padx=10)

        # 分析按钮
        analyze_btn = tk.Button(
            date_frame,
            text="分析热量平衡",
            command=self.analyze_calorie_balance,
            font=("SimHei", 12),
            bg="#2196F3",
            fg="white"
        )
        analyze_btn.pack(side=tk.LEFT, padx=10)

        # 结果显示框架
        result_frame = tk.Frame(self.root, bg="#f0f0f0")
        result_frame.pack(pady=30, fill=tk.X, padx=50)

        # 摄入热量
        tk.Label(
            result_frame,
            text="当日摄入热量：",
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.intake_result_var = tk.StringVar(value="-- 卡路里")
        tk.Label(
            result_frame,
            textvariable=self.intake_result_var,
            font=("SimHei", 12),
            bg="#f0f0f0",
            fg="#4CAF50"
        ).grid(row=0, column=1, sticky="w", pady=5)

        # 消耗热量
        tk.Label(
            result_frame,
            text="当日消耗热量(TDEE)：",
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.expenditure_result_var = tk.StringVar(value="-- 卡路里")
        tk.Label(
            result_frame,
            textvariable=self.expenditure_result_var,
            font=("SimHei", 12),
            bg="#f0f0f0",
            fg="#2196F3"
        ).grid(row=1, column=1, sticky="w", pady=5)

        # 热量缺口
        tk.Label(
            result_frame,
            text="热量缺口：",
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.balance_result_var = tk.StringVar(value="-- 卡路里")
        tk.Label(
            result_frame,
            textvariable=self.balance_result_var,
            font=("SimHei", 12, "bold"),
            bg="#f0f0f0",
            fg="#FF5722"
        ).grid(row=2, column=1, sticky="w", pady=5)

        # 说明文字
        self.balance_note_var = tk.StringVar(value="请选择日期并点击分析按钮")
        note_label = tk.Label(
            self.root,
            textvariable=self.balance_note_var,
            font=("SimHei", 11),
            bg="#f0f0f0",
            fg="#666666",
            wraplength=600,
            justify=tk.LEFT
        )
        note_label.pack(pady=20, padx=50, anchor="w")

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="返回主菜单",
            command=self.create_main_frame,
            font=("SimHei", 12),
            width=15,
            bg="#f44336",
            fg="white"
        )
        back_btn.pack(side=tk.BOTTOM, pady=20)

    def calculate_calorie_balance(self, date, total_intake):
        """计算并显示热量平衡"""
        # 获取当天的TDEE（使用最近的代谢率记录）
        tdee = self.get_latest_tdee(date)

        if tdee is None:
            self.calorie_balance_var.set("热量平衡：暂无代谢率数据（请先计算代谢率）")
            return

        # 计算热量缺口（消耗 - 摄入）
        balance = tdee - total_intake

        # 显示热量平衡
        if balance > 0:
            self.calorie_balance_var.set(f"热量缺口：+{balance} 卡路里（处于热量赤字状态）")
        elif balance < 0:
            self.calorie_balance_var.set(f"热量缺口：{balance} 卡路里（处于热量盈余状态）")
        else:
            self.calorie_balance_var.set("热量缺口：0 卡路里（热量平衡）")

    def analyze_calorie_balance(self):
        """分析指定日期的热量平衡"""
        date = self.balance_date.get()

        # 获取当日摄入热量
        if date in self.data['calorie_intake'] and self.data['calorie_intake'][date]:
            total_intake = sum(item['calories'] for item in self.data['calorie_intake'][date])
            self.intake_result_var.set(f"{total_intake} 卡路里")
        else:
            total_intake = 0
            self.intake_result_var.set("0 卡路里（无记录）")

        # 获取当日的TDEE（使用最近的代谢率记录）
        tdee = self.get_latest_tdee(date)

        if tdee is None:
            self.expenditure_result_var.set("无代谢率数据")
            self.balance_result_var.set("无法计算")
            self.balance_note_var.set("请先计算并记录您的基础代谢率，才能进行热量平衡分析。")
            return

        self.expenditure_result_var.set(f"{tdee} 卡路里")

        # 计算热量缺口
        balance = tdee - total_intake

        # 显示热量缺口
        if balance > 0:
            self.balance_result_var.set(f"+{balance} 卡路里")
            self.balance_note_var.set(
                f"热量缺口为+{balance}卡路里，您处于热量赤字状态。\n"
                "这有助于减轻体重，因为身体会消耗储存的能量来弥补缺口。"
            )
        elif balance < 0:
            self.balance_result_var.set(f"{balance} 卡路里")
            self.balance_note_var.set(
                f"热量缺口为{balance}卡路里，您处于热量盈余状态。\n"
                "多余的热量会被身体储存为脂肪，可能导致体重增加。"
            )
        else:
            self.balance_result_var.set("0 卡路里")
            self.balance_note_var.set(
                "热量摄入与消耗达到平衡，这有助于维持当前体重。"
            )

    def get_latest_tdee(self, target_date):
        """获取目标日期当天或最近的TDEE值"""
        if not self.data['bmr_records']:
            return None

        # 筛选出不晚于目标日期的记录
        valid_records = [
            record for record in self.data['bmr_records']
            if record['date'] <= target_date
        ]

        if not valid_records:
            return None

        # 按日期排序，取最近的一条
        latest_record = sorted(valid_records, key=lambda x: x['date'], reverse=True)[0]
        return latest_record['tdee']

    # 基础代谢率相关功能
    def open_bmr_frame(self):
        """打开基础代谢率计算界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="基础代谢率计算",
            font=("SimHei", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # 输入框架
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # 体重输入
        tk.Label(
            input_frame,
            text="体重 (kg):",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.bmr_weight_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.bmr_weight_entry.grid(row=0, column=1, padx=10, pady=10)

        # 身高输入
        tk.Label(
            input_frame,
            text="身高 (cm):",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.bmr_height_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.bmr_height_entry.grid(row=1, column=1, padx=10, pady=10)

        # 年龄输入
        tk.Label(
            input_frame,
            text="年龄:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.age_entry = tk.Entry(
            input_frame,
            font=("SimHei", 12),
            width=15
        )
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        # 性别选择
        tk.Label(
            input_frame,
            text="性别:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.gender_var = tk.StringVar(value="男")
        gender_frame = tk.Frame(input_frame, bg="#f0f0f0")
        gender_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Radiobutton(
            gender_frame,
            text="男",
            variable=self.gender_var,
            value="男",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            gender_frame,
            text="女",
            variable=self.gender_var,
            value="女",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        # 活动水平选择
        tk.Label(
            input_frame,
            text="活动水平:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.activity_level = tk.IntVar(value=1)
        activity_frame = tk.Frame(input_frame, bg="#f0f0f0")
        activity_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        activities = [
            "1. 几乎不运动或久坐不动",
            "2. 轻度活动（每周1-3天）",
            "3. 中度活动（每周3-5天）",
            "4. 高度活动（每周6-7天）",
            "5. 极高度活动（每天）"
        ]

        for i, activity in enumerate(activities):
            tk.Radiobutton(
                activity_frame,
                text=activity,
                variable=self.activity_level,
                value=i + 1,
                font=("SimHei", 10),
                bg="#f0f0f0"
            ).pack(anchor="w")

        # 结果显示
        self.bmr_result_var = tk.StringVar()
        result_label = tk.Label(
            self.root,
            textvariable=self.bmr_result_var,
            font=("SimHei", 12),
            bg="#f0f0f0",
            fg="#2196F3",
            justify=tk.LEFT
        )
        result_label.pack(pady=10, padx=50, anchor="w")

        # 按钮框架
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        # 计算按钮
        calc_btn = tk.Button(
            btn_frame,
            text="计算代谢率",
            command=self.calculate_and_record_bmr,
            font=("SimHei", 12),
            width=15,
            bg="#2196F3",
            fg="white"
        )
        calc_btn.grid(row=0, column=0, padx=10)

        # 返回按钮
        back_btn = tk.Button(
            btn_frame,
            text="返回主菜单",
            command=self.create_main_frame,
            font=("SimHei", 12),
            width=15,
            bg="#f44336",
            fg="white"
        )
        back_btn.grid(row=0, column=1, padx=10)

    def calculate_and_record_bmr(self):
        """计算并记录基础代谢率"""
        try:
            weight = float(self.bmr_weight_entry.get())
            height = float(self.bmr_height_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            activity_level = self.activity_level.get()

            if weight <= 0 or height <= 0 or age <= 0:
                messagebox.showerror("输入错误", "体重、身高和年龄必须为正数")
                return

            # 计算BMR (Mifflin-St Jeor公式)
            if gender == "男":
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            bmr = round(bmr)

            # 计算TDEE
            activity_factors = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
            tdee = round(bmr * activity_factors[activity_level])

            # 活动水平描述
            activity_descriptions = {
                1: "几乎不运动或久坐不动",
                2: "轻度活动（每周1-3天）",
                3: "中度活动（每周3-5天）",
                4: "高度活动（每周6-7天）",
                5: "极高度活动（每天）"
            }

            # 显示结果
            result_text = (f"基础代谢率(BMR): {bmr} 卡路里/天\n"
                           f"总能量消耗(TDEE): {tdee} 卡路里/天\n"
                           f"活动水平: {activity_descriptions[activity_level]}")
            self.bmr_result_var.set(result_text)

            # 记录数据
            record = {
                'date': datetime.date.today().isoformat(),
                'weight': weight,
                'height': height,
                'age': age,
                'gender': gender,
                'activity_level': activity_level,
                'activity_description': activity_descriptions[activity_level],
                'bmr': bmr,
                'tdee': tdee
            }

            self.data['bmr_records'].append(record)
            self.save_data()
            messagebox.showinfo("成功", "基础代谢率记录已保存")

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

    # 历史记录功能
    def open_history_frame(self):
        """打开历史记录界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title_label = tk.Label(
            self.root,
            text="历史记录",
            font=("SimHei", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)

        # 记录类型选择
        self.history_type = tk.StringVar(value="bmi")
        type_frame = tk.Frame(self.root, bg="#f0f0f0")
        type_frame.pack(pady=10)

        tk.Label(
            type_frame,
            text="选择记录类型:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            type_frame,
            text="BMI记录",
            variable=self.history_type,
            value="bmi",
            font=("SimHei", 12),
            bg="#f0f0f0",
            command=self.update_history_list
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            type_frame,
            text="代谢率记录",
            variable=self.history_type,
            value="bmr",
            font=("SimHei", 12),
            bg="#f0f0f0",
            command=self.update_history_list
        ).pack(side=tk.LEFT, padx=10)

        tk.Radiobutton(
            type_frame,
            text="能量摄入记录",
            variable=self.history_type,
            value="calorie",
            font=("SimHei", 12),
            bg="#f0f0f0",
            command=self.update_history_list
        ).pack(side=tk.LEFT, padx=10)

        # 日期选择（仅用于能量摄入）
        self.history_date_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.history_date_frame.pack(pady=10)

        tk.Label(
            self.history_date_frame,
            text="选择日期:",
            font=("SimHei", 12),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT, padx=10)

        self.history_date = DateEntry(
            self.history_date_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.history_date.pack(side=tk.LEFT, padx=10)

        view_btn = tk.Button(
            self.history_date_frame,
            text="查看该日记录",
            command=self.update_history_list,
            font=("SimHei", 10),
            bg="#4CAF50",
            fg="white"
        )
        view_btn.pack(side=tk.LEFT, padx=10)

        # 初始隐藏日期选择（仅能量摄入需要）
        self.history_date_frame.pack_forget()

        # 记录列表
        self.history_listbox = tk.Listbox(
            self.root,
            width=80,
            height=15,
            font=("SimHei", 10)
        )
        self.history_listbox.pack(pady=10)

        # 返回按钮
        back_btn = tk.Button(
            self.root,
            text="返回主菜单",
            command=self.create_main_frame,
            font=("SimHei", 12),
            width=15,
            bg="#f44336",
            fg="white"
        )
        back_btn.pack(side=tk.BOTTOM, pady=20)

        # 初始加载BMI记录
        self.update_history_list()

    def update_history_list(self):
        """更新历史记录列表"""
        # 清空列表
        self.history_listbox.delete(0, tk.END)

        record_type = self.history_type.get()

        # 显示或隐藏日期选择框
        if record_type == "calorie":
            self.history_date_frame.pack(pady=10)
        else:
            self.history_date_frame.pack_forget()

        if record_type == "bmi":
            # 显示BMI记录
            if not self.data['bmi_records']:
                self.history_listbox.insert(tk.END, "暂无BMI记录")
                return

            # 按日期排序，最近的在前
            sorted_records = sorted(
                self.data['bmi_records'],
                key=lambda x: x['date'],
                reverse=True
            )

            for record in sorted_records:
                self.history_listbox.insert(
                    tk.END,
                    f"{record['date']} - 体重: {record['weight']}kg, 身高: {record['height']}cm, "
                    f"BMI: {record['bmi']}, 类别: {record['category']}"
                )

        elif record_type == "bmr":
            # 显示代谢率记录
            if not self.data['bmr_records']:
                self.history_listbox.insert(tk.END, "暂无代谢率记录")
                return

            # 按日期排序，最近的在前
            sorted_records = sorted(
                self.data['bmr_records'],
                key=lambda x: x['date'],
                reverse=True
            )

            for record in sorted_records:
                self.history_listbox.insert(
                    tk.END,
                    f"{record['date']} - 年龄: {record['age']}岁, 性别: {record['gender']}, "
                    f"活动水平: {record['activity_description']}"
                )
                self.history_listbox.insert(
                    tk.END,
                    f"   BMR: {record['bmr']} 卡路里/天, TDEE: {record['tdee']} 卡路里/天"
                )
                self.history_listbox.insert(tk.END, "")

        elif record_type == "calorie":
            # 显示能量摄入记录
            date = self.history_date.get()

            if date not in self.data['calorie_intake'] or not self.data['calorie_intake'][date]:
                self.history_listbox.insert(tk.END, f"{date} 暂无能量摄入记录")
                return

            records = self.data['calorie_intake'][date]
            total = sum(item['calories'] for item in records)

            self.history_listbox.insert(tk.END, f"{date} 的能量摄入记录：")
            self.history_listbox.insert(tk.END, "")

            for item in records:
                self.history_listbox.insert(tk.END, f"{item['food']}: {item['calories']} 卡路里")

            self.history_listbox.insert(tk.END, "")
            self.history_listbox.insert(tk.END, f"总计：{total} 卡路里")


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTrackerApp(root)
    root.mainloop()
