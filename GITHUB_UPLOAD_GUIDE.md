# GitHub 上传指南

## 前置准备

### 1. 安装 Git
- **Windows**: 下载 [Git for Windows](https://git-scm.com/download/win) 并安装
- **macOS**: `brew install git`
- **Linux**: `sudo apt-get install git`

### 2. 配置 Git
首次使用需要设置用户信息（全局配置）：

```bash
# 设置用户名（使用你的 GitHub 用户名）
git config --global user.name "你的GitHub用户名"

# 设置邮箱（使用注册 GitHub 的邮箱）
git config --global user.email "你的邮箱@example.com"

# 验证配置
git config --global --list
```

### 3. 在 GitHub 上创建仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Repository name**: `zrbzf` (或其他名称)
   - **Description**: `AI 问答助手 - 智能搜题系统`
   - **Public/Private**: 选择公开或私有
   - **Initialize this repository with**: **不勾选**（我们本地已有代码）
4. 点击 `Create repository`

## 上传步骤

### 方法一：本地已有项目（推荐）

进入项目目录后，依次执行以下命令：

```bash
# 1. 初始化本地 Git 仓库
git init

# 2. 添加所有文件（会自动忽略 .gitignore 列出的文件）
git add .

# 3. 创建首个提交
git commit -m "初始化项目：AI问答助手"

# 4. 添加远程仓库地址（替换 USERNAME 和 REPO_NAME）
git remote add origin https://github.com/USERNAME/zrbzf.git

# 5. 重命名默认分支为 main（GitHub 新仓库默认分支）
git branch -M main

# 6. 推送到 GitHub
git push -u origin main
```

**完整示例**（假设 GitHub 用户名是 `feynman`）：
```bash
git init
git add .
git commit -m "初始化项目：AI问答助手"
git remote add origin https://github.com/feynman/zrbzf.git
git branch -M main
git push -u origin main
```

### 方法二：使用 SSH（更安全，推荐有 SSH 基础的用户）

**1. 生成 SSH 密钥**（如未生成过）：
```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
```
按回车键，保持默认位置，不设密码（或设密码）。

**2. 添加公钥到 GitHub**（Windows 查看）：
```bash
# PowerShell 中查看公钥
type $env:USERPROFILE\.ssh\id_rsa.pub
```
复制内容，在 GitHub 设置 → SSH keys → New SSH key → 粘贴并保存

**3. 上传到 GitHub**：
```bash
git init
git add .
git commit -m "初始化项目：AI问答助手"
git remote add origin git@github.com:USERNAME/zrbzf.git
git branch -M main
git push -u origin main
```

## 日常操作

### 提交新的改动

```bash
# 查看改动状态
git status

# 添加所有改动
git add .

# 提交（使用有意义的信息）
git commit -m "功能：添加新的搜索算法"

# 推送到 GitHub
git push
```

### 常用命令

```bash
# 查看提交历史
git log --oneline

# 查看当前分支
git branch -a

# 从 GitHub 拉取最新代码
git pull

# 查看改动差异
git diff

# 回退到上一次提交
git reset --hard HEAD~1
```

## 常见问题

### Q: 推送时提示 "authentication failed"？

**解决方案**：
1. **HTTPS 方式**：使用个人访问令牌 (Personal Access Token)
   - GitHub 设置 → Developer settings → Personal access tokens → Generate new token
   - 生成令牌，第一次推送时使用令牌作为密码
   
2. **SSH 方式**：确保 SSH 密钥已正确添加到 GitHub

### Q: 如何删除已提交的文件？

```bash
# 删除文件但保留本地副本
git rm --cached filename

# 删除 .venv 文件夹（虽然 .gitignore 应该已防止）
git rm -r --cached .venv

# 提交删除
git commit -m "移除虚拟环境文件"
git push
```

### Q: 本地和远程冲突怎么办？

```bash
# 查看冲突
git status

# 选择保留远程版本
git checkout --theirs <filename>

# 或保留本地版本
git checkout --ours <filename>

# 提交解决
git add .
git commit -m "解决合并冲突"
git push
```

### Q: 如何修改最后一次提交？

```bash
# 修改提交信息
git commit --amend -m "新的提交信息"

# 如果已推送到 GitHub（谨慎使用）
git push --force
```

## 推荐的提交信息规范

使用清晰、有意义的提交信息：

```
功能: 添加用户搜索功能
修复: 修正答案显示错误
优化: 提升搜索速度
文档: 更新 README 说明
重构: 改进代码结构
```

## 项目上传完成后

1. ✅ 在 GitHub 个人资料中展示项目
2. ✅ 添加项目链接到简历/作品集
3. ✅ 邀请他人贡献（开源社区）
4. ✅ 定期提交和更新

---

**需要帮助？** 如果遇到问题，执行以下命令获取详细错误信息后再联系我。
