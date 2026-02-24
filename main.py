"""
Author: Feynman
Date: 2025/4/21
Version: 2.0 - Modern Tech UI
Description:
通过自定义数据库中的题目和答案，来进行答案搜寻的智能答题助手。
"""
# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from rapidfuzz import process
import sys
import io

# 仅当 stdout/stderr 可用时设置 UTF-8 编码
if sys.stdout is not None:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr is not None:
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 颜色主题定义
COLORS = {
    'bg_dark': '#0f1419',      # 深黑背景
    'bg_panel': '#1a1f26',     # 面板背景
    'primary': '#00d4ff',      # 青蓝色
    'primary_hover': '#00e8ff', # 青蓝色悬停
    'secondary': '#7c3aed',    # 紫色
    'success': '#10b981',      # 绿色
    'text_primary': '#f0f4f8',  # 主要文本
    'text_secondary': '#94a3b8', # 次要文本
    'border': '#334155'        # 边框
}


class QuestionAnswerSystem:
    def __init__(self, json_file: str = "questions.json"):
        self.questions = self._load_questions(json_file)
        self.question_map = {q["question"]: q for q in self.questions}

    def _load_questions(self, json_file: str) -> list:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("Loaded JSON data:", data)  # 调试：检查加载的数据
            if not isinstance(data, list):
                messagebox.showerror("错误", f"JSON文件根节点必须是列表，实际类型为 {type(data)}")
                return []
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    messagebox.showerror("错误", f"JSON文件中第 {i+1} 个条目不是字典，找到: {item}")
                    return []
                if "question" not in item or "answer" not in item:
                    messagebox.showerror("错误", f"JSON文件中第 {i+1} 个条目缺少 'question' 或 'answer' 键: {item}")
                    return []
            return data
        except FileNotFoundError:
            messagebox.showerror("错误", f"找不到数据库文件 {json_file}")
            return []
        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"JSON文件格式不正确: {e}")
            return []

    def find_question(self, user_input: str) -> dict:
        question_texts = list(self.question_map.keys())
        match = process.extractOne(user_input, question_texts, score_cutoff=60)
        return self.question_map.get(match[0]) if match else None


class QuestionAnswerGUI:
    def __init__(self, root):
        self.qa_system = QuestionAnswerSystem()
        self.root = root
        self.root.title("智能答题助手-定制联系q3553303315")
        self.root.geometry("1200x800")
        
        # 设置全局背景
        self.root.configure(bg=COLORS['bg_dark'])
        
        # ===== 顶部标题栏 =====
        self.header_frame = tk.Frame(root, bg=COLORS['bg_panel'], height=80)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            self.header_frame,
            text="🔍 智能答题助手",
            font=("Microsoft YaHei UI", 28, "bold"),
            bg=COLORS['bg_panel'],
            fg=COLORS['primary']
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            self.header_frame,
            text="快速搜索、智能匹配",
            font=("Microsoft YaHei UI", 11),
            bg=COLORS['bg_panel'],
            fg=COLORS['text_secondary']
        )
        subtitle_label.pack()
        
        # ===== 主容器 =====
        main_container = tk.Frame(root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ===== 输入区域 =====
        input_section = tk.Frame(main_container, bg=COLORS['bg_panel'], bd=0)
        input_section.pack(fill=tk.X, pady=(0, 20))
        self._create_rounded_frame(input_section, COLORS['bg_panel'], padx=20, pady=20)
        
        input_label = tk.Label(
            input_section,
            text="输入您的问题",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg=COLORS['bg_panel'],
            fg=COLORS['primary']
        )
        input_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 输入框容器
        entry_frame = tk.Frame(input_section, bg=COLORS['bg_panel'])
        entry_frame.pack(fill=tk.X)
        
        self.entry = tk.Text(
            entry_frame,
            height=3,
            width=50,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 12),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['primary'],
            border=0,
            relief=tk.FLAT,
            padx=15,
            pady=12
        )
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.search_question() if not e.state & 0x1 else "break")
        self.entry.bind("<Shift-Return>", lambda e: "break")
        self.entry.bind("<<Paste>>", self.handle_paste)
        
        # 快捷键提示
        hint_label = tk.Label(
            input_section,
            text="💡 按 Enter 搜索 | Shift + Enter 换行",
            font=("Microsoft YaHei UI", 9),
            bg=COLORS['bg_panel'],
            fg=COLORS['text_secondary']
        )
        hint_label.pack(anchor=tk.E, pady=(10, 0))
        
        # ===== 按钮区域 =====
        btn_section = tk.Frame(main_container, bg=COLORS['bg_dark'])
        btn_section.pack(fill=tk.X, pady=(0, 20))
        
        self.search_btn = tk.Button(
            btn_section,
            text="🔎 搜索答案",
            command=self.search_question,
            font=("Microsoft YaHei UI", 12, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['bg_dark'],
            activebackground=COLORS['primary_hover'],
            activeforeground=COLORS['bg_dark'],
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor="hand2",
            border=0
        )
        self.search_btn.pack(side=tk.LEFT)
        
        clear_btn = tk.Button(
            btn_section,
            text="🗑 清空",
            command=self.clear_content,
            font=("Microsoft YaHei UI", 11),
            bg=COLORS['bg_panel'],
            fg=COLORS['text_secondary'],
            activebackground=COLORS['border'],
            activeforeground=COLORS['primary'],
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor="hand2",
            border=0,
            highlightthickness=0
        )
        clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # ===== 结果区域 =====
        result_label = tk.Label(
            main_container,
            text="搜索结果",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['primary']
        )
        result_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 结果面板
        result_section = tk.Frame(main_container, bg=COLORS['bg_panel'], bd=0)
        result_section.pack(fill=tk.BOTH, expand=True)
        self._create_rounded_frame(result_section, COLORS['bg_panel'], padx=20, pady=20)
        
        self.result_area = scrolledtext.ScrolledText(
            result_section,
            wrap=tk.WORD,
            font=("Microsoft YaHei UI", 14),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['primary'],
            border=0,
            relief=tk.FLAT,
            padx=15,
            pady=12
        )
        self.result_area.pack(fill=tk.BOTH, expand=True)
        
        # 配置文本标签的样式 - 居中对齐
        self.result_area.tag_config("question", font=("Microsoft YaHei UI", 16, "bold"), foreground=COLORS['primary'], justify=tk.CENTER)
        self.result_area.tag_config("answer", font=("Microsoft YaHei UI", 14, "bold"), foreground=COLORS['success'], justify=tk.CENTER)
        self.result_area.tag_config("label", foreground=COLORS['secondary'], font=("Microsoft YaHei UI", 15, "bold"), justify=tk.CENTER)
        self.result_area.tag_config("explanation", foreground=COLORS['text_secondary'], font=("Microsoft YaHei UI", 13, "italic"), justify=tk.CENTER)
        self.result_area.tag_config("default", justify=tk.CENTER)
        
        # 显示欢迎信息
        self._show_welcome_message()
    
    def _create_rounded_frame(self, frame, bg_color, padx=10, pady=10):
        """给框架添加视觉样式"""
        frame.configure(bg=bg_color, relief=tk.FLAT, bd=1, highlightthickness=1, highlightbackground=COLORS['border'])
    
    def _show_welcome_message(self):
        """显示欢迎信息"""
        self.result_area.config(state=tk.NORMAL)
        self.result_area.delete("1.0", tk.END)
        
        self.result_area.insert(tk.END, "AI 问答助手\n", "question")
        self.result_area.insert(tk.END, "\n", "default")
        
        self.result_area.insert(tk.END, "快速搜索 · 智能匹配\n\n", "explanation")
        
        self.result_area.insert(tk.END, "使用说明\n", "label")
        self.result_area.insert(tk.END, "• 在上方输入框输入您的问题\n", "default")
        self.result_area.insert(tk.END, "• 系统将自动匹配最相关的答案\n", "default")
        self.result_area.insert(tk.END, "• 支持模糊搜索，无需完全匹配\n\n", "default")
        
        self.result_area.insert(tk.END, "快捷键\n", "label")
        self.result_area.insert(tk.END, "• Enter - 快速搜索\n", "default")
        self.result_area.insert(tk.END, "• Shift + Enter - 输入框换行\n", "default")
        self.result_area.insert(tk.END, "• Ctrl + V - 自动清理粘贴内容\n\n", "default")
        
        self.result_area.insert(tk.END, "开始提问吧！", "answer")
        self.result_area.config(state=tk.DISABLED)
    
    def clear_content(self):
        """清空所有内容"""
        self.entry.delete("1.0", tk.END)
        self._show_welcome_message()

    def handle_paste(self, event):
        try:
            clipboard = self.root.clipboard_get()
            print("Clipboard content:", clipboard)
            cleaned_text = ''.join(c for c in clipboard if c.isprintable())
            cleaned_text = cleaned_text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", cleaned_text)
            print("Cleaned text:", cleaned_text)
            return "break"
        except tk.TclError:
            messagebox.showwarning("提示", "无法获取剪贴板内容")
            return "break"
        except UnicodeDecodeError:
            messagebox.showwarning("提示", "粘贴内容包含无效字符，已忽略")
            return "break"

    def search_question(self):
        query = self.entry.get("1.0", tk.END).strip()
        try:
            query = query.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            messagebox.showwarning("提示", "输入包含无效字符，请检查粘贴内容")
            return
        if not query:
            messagebox.showwarning("提示", "请输入有效问题")
            return

        result = self.qa_system.find_question(query)
        self.result_area.config(state=tk.NORMAL)
        self.result_area.delete("1.0", tk.END)

        if not result:
            self.result_area.insert(tk.END, "未找到相关问题\n\n", "label")
            self.result_area.insert(tk.END, "提示：请尝试使用不同的关键词或已知的题目内容。", "explanation")
            self.result_area.config(state=tk.DISABLED)
            return

        # 格式化显示结果 - 简洁设计
        self.result_area.insert(tk.END, "问题\n", "label")
        self.result_area.insert(tk.END, result['question'] + "\n\n", "question")
        
        self.result_area.insert(tk.END, "答案\n", "label")
        answers = result['answer'].split(';')
        for i, answer in enumerate(answers, 1):
            self.result_area.insert(tk.END, f"{i}. {answer.strip()}\n", "answer")
        
        self.result_area.insert(tk.END, "\n")
        
        if "explanation" in result:
            self.result_area.insert(tk.END, "解析\n", "label")
            self.result_area.insert(tk.END, result['explanation'] + "\n", "explanation")
        
        self.result_area.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionAnswerGUI(root)
    root.mainloop()