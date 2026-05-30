<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> | 
  <a href="#繁體中文">繁體中文</a> | 
  <a href="#english">English</a>
</p>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**MailPulse-Server** 是一款轻量级邮件服务器健康监控与诊断CLI工具，专为系统管理员和开发者设计。它能够快速检测邮件服务器的运行状态、安全配置和送达性能，帮助您确保邮件系统的稳定运行。

### 💡 解决的用户痛点

- 🔍 **服务器状态不明**：不知道邮件服务器是否正常运行
- 🛡️ **安全配置复杂**：SPF/DKIM/DMARC配置难以验证
- 📊 **问题排查困难**：邮件发送失败时难以定位原因
- ⏱️ **监控成本高**：需要专业工具和大量时间

### ✨ 自研差异化亮点

- 🚀 **零依赖部署**：纯Python实现，安装即用
- 🔒 **全面安全审计**：一键检测SPF/DKIM/DMARC配置
- 📈 **实时健康检测**：支持SMTP/IMAP/POP3协议
- 💻 **美观CLI界面**：基于Rich库的彩色表格输出
- ⚡ **快速响应**：毫秒级连接检测

---

## ✨ 核心特性

### 🔌 协议健康检测
- **SMTP检测**：支持端口25/587/465，自动识别STARTTLS
- **IMAP检测**：支持端口143/993，SSL/TLS自动适配
- **POP3检测**：支持端口110/995，完整连接测试

### 🛡️ 安全配置审计
- **SPF记录检测**：验证发件人策略框架配置
- **DKIM记录检测**：检查域名密钥识别邮件签名
- **DMARC记录检测**：确认域名消息认证报告策略

### 📊 综合诊断
- **MX记录分析**：解析邮件交换记录优先级
- **连通性测试**：检测邮件服务器端口可达性
- **智能建议**：自动生成优化建议

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

### 安装步骤

```bash
# 方式一：通过pip安装（推荐）
pip install mailpulse-server

# 方式二：从源码安装
git clone https://github.com/yourusername/mailpulse-server.git
cd mailpulse-server
pip install -r requirements.txt
pip install -e .
```

### 本地启动

```bash
# 查看帮助信息
mailpulse --help

# 检查SMTP服务器
mailpulse smtp mail.example.com --port 587 --tls

# 检查IMAP服务器
mailpulse imap mail.example.com --port 993 --ssl

# 安全配置审计
mailpulse security example.com --full

# 综合诊断
mailpulse diagnose example.com
```

---

## 📖 详细使用指南

### SMTP健康检测

```bash
# 基本检测（端口25）
mailpulse smtp smtp.gmail.com

# 指定端口和超时
mailpulse smtp mail.example.com --port 587 --timeout 15

# 使用TLS加密
mailpulse smtp mail.example.com --port 465 --tls
```

### 安全配置审计

```bash
# 基础检查（SPF + DMARC）
mailpulse security example.com

# 完整检查（SPF + DKIM + DMARC）
mailpulse security example.com --full
```

**输出示例：**

```
╭──────────────────────────────────────────────────────────────────────────────╮
│ 🔒 Security Audit for example.com                                            │
╰──────────────────────────────────────────────────────────────────────────────╯

                        Security Configuration Results
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Record Type ┃ Status     ┃ Details                                          ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ SPF         │ ✅ PASS    │ SPF record found with hardfail (-all)            │
│ DKIM        │ ✅ PASS    │ DKIM record found with 2048-bit key              │
│ DMARC       │ ✅ PASS    │ DMARC policy set to reject (recommended)          │
└─────────────┴────────────┴──────────────────────────────────────────────────┘
```

### 综合诊断

```bash
# 一键诊断域名邮件配置
mailpulse diagnose example.com
```

### MX记录分析

```bash
# 分析MX记录
mailpulse mx example.com
```

---

## 💡 设计思路与迭代规划

### 设计理念

MailPulse-Server 的设计遵循以下原则：

1. **简洁至上**：CLI工具应该简单易用，一个命令完成一项任务
2. **输出友好**：使用Rich库提供美观、可读性强的输出
3. **零配置**：开箱即用，无需复杂配置文件
4. **跨平台**：纯Python实现，支持所有主流操作系统

### 技术选型原因

| 技术 | 选型原因 |
|------|---------|
| Python 3.8+ | 广泛兼容性，丰富的网络库 |
| Click | 业界标准CLI框架，装饰器语法简洁 |
| Rich | 美观的终端输出，支持表格、进度条 |
| dnspython | 成熟的DNS查询库，支持各种记录类型 |

### 后续迭代计划

- [ ] 📧 邮件发送测试功能
- [ ] 📈 送达率统计分析
- [ ] 🔔 黑名单检测
- [ ] 📊 Web Dashboard
- [ ] 🐳 Docker镜像支持
- [ ] 📱 REST API接口

---

## 📦 打包与部署指南

### 打包为可执行文件

```bash
# 安装打包工具
pip install pyinstaller

# 打包为单文件
pyinstaller --onefile --name mailpulse mailpulse/cli.py

# 打包产物位于 dist/ 目录
```

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "mailpulse.cli"]
```

```bash
# 构建镜像
docker build -t mailpulse-server .

# 运行容器
docker run --rm mailpulse-server security example.com
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交PR

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### Issue反馈

- 🐛 Bug报告：请提供复现步骤和环境信息
- 💡 功能建议：请描述使用场景和预期效果
- 📖 文档改进：欢迎指出文档中的错误或不足

---

## 📄 开源协议说明

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2025 SOLO Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<p align="center">
  Made with ❤️ by SOLO Agent
</p>

---
---

<a name="繁體中文"></a>
## 🎉 專案介紹

**MailPulse-Server** 是一款輕量級郵件伺服器健康監控與診斷CLI工具，專為系統管理員和開發者設計。它能夠快速檢測郵件伺服器的運行狀態、安全配置和送達性能，幫助您確保郵件系統的穩定運行。

### 💡 解決的使用者痛點

- 🔍 **伺服器狀態不明**：不知道郵件伺服器是否正常運行
- 🛡️ **安全配置複雜**：SPF/DKIM/DMARC配置難以驗證
- 📊 **問題排查困難**：郵件發送失敗時難以定位原因
- ⏱️ **監控成本高**：需要專業工具和大量時間

### ✨ 自研差異化亮點

- 🚀 **零依賴部署**：純Python實現，安裝即用
- 🔒 **全面安全稽核**：一鍵檢測SPF/DKIM/DMARC配置
- 📈 **即時健康檢測**：支援SMTP/IMAP/POP3協定
- 💻 **美觀CLI介面**：基於Rich庫的彩色表格輸出
- ⚡ **快速響應**：毫秒級連接檢測

---

## ✨ 核心特性

### 🔌 協定健康檢測
- **SMTP檢測**：支援埠25/587/465，自動識別STARTTLS
- **IMAP檢測**：支援埠143/993，SSL/TLS自動適配
- **POP3檢測**：支援埠110/995，完整連接測試

### 🛡️ 安全配置稽核
- **SPF記錄檢測**：驗證發件人策略框架配置
- **DKIM記錄檢測**：檢查網域名稱金鑰識別郵件簽名
- **DMARC記錄檢測**：確認網域名稱訊息認證報告策略

### 📊 綜合診斷
- **MX記錄分析**：解析郵件交換記錄優先級
- **連通性測試**：檢測郵件伺服器埠可達性
- **智慧建議**：自動生成優化建議

---

## 🚀 快速開始

### 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows / macOS / Linux

### 安裝步驟

```bash
# 方式一：透過pip安裝（推薦）
pip install mailpulse-server

# 方式二：從原始碼安裝
git clone https://github.com/yourusername/mailpulse-server.git
cd mailpulse-server
pip install -r requirements.txt
pip install -e .
```

### 本地啟動

```bash
# 查看幫助資訊
mailpulse --help

# 檢查SMTP伺服器
mailpulse smtp mail.example.com --port 587 --tls

# 檢查IMAP伺服器
mailpulse imap mail.example.com --port 993 --ssl

# 安全配置稽核
mailpulse security example.com --full

# 綜合診斷
mailpulse diagnose example.com
```

---

## 📖 詳細使用指南

### SMTP健康檢測

```bash
# 基本檢測（埠25）
mailpulse smtp smtp.gmail.com

# 指定埠和逾時
mailpulse smtp mail.example.com --port 587 --timeout 15

# 使用TLS加密
mailpulse smtp mail.example.com --port 465 --tls
```

### 安全配置稽核

```bash
# 基礎檢查（SPF + DMARC）
mailpulse security example.com

# 完整檢查（SPF + DKIM + DMARC）
mailpulse security example.com --full
```

### 綜合診斷

```bash
# 一鍵診斷網域名稱郵件配置
mailpulse diagnose example.com
```

### MX記錄分析

```bash
# 分析MX記錄
mailpulse mx example.com
```

---

## 💡 設計思路與迭代規劃

### 設計理念

MailPulse-Server 的設計遵循以下原則：

1. **簡潔至上**：CLI工具應該簡單易用，一個命令完成一項任務
2. **輸出友善**：使用Rich庫提供美觀、可讀性強的輸出
3. **零配置**：開箱即用，無需複雜配置檔案
4. **跨平台**：純Python實現，支援所有主流作業系統

### 技術選型原因

| 技術 | 選型原因 |
|------|---------|
| Python 3.8+ | 廣泛相容性，豐富的網路函式庫 |
| Click | 業界標準CLI框架，裝飾器語法簡潔 |
| Rich | 美觀的終端輸出，支援表格、進度條 |
| dnspython | 成熟的DNS查詢函式庫，支援各種記錄類型 |

### 後續迭代計劃

- [ ] 📧 郵件發送測試功能
- [ ] 📈 送達率統計分析
- [ ] 🔔 黑名單檢測
- [ ] 📊 Web Dashboard
- [ ] 🐳 Docker映像檔支援
- [ ] 📱 REST API介面

---

## 📦 打包與部署指南

### 打包為可執行檔案

```bash
# 安裝打包工具
pip install pyinstaller

# 打包為單一檔案
pyinstaller --onefile --name mailpulse mailpulse/cli.py

# 打包產物位於 dist/ 目錄
```

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "mailpulse.cli"]
```

```bash
# 建構映像檔
docker build -t mailpulse-server .

# 執行容器
docker run --rm mailpulse-server security example.com
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交PR

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### Issue回饋

- 🐛 Bug報告：請提供重現步驟和環境資訊
- 💡 功能建議：請描述使用場景和預期效果
- 📖 文檔改進：歡迎指出文檔中的錯誤或不足

---

## 📄 開源協議說明

本專案採用 [MIT License](LICENSE) 開源協議。

---

<p align="center">
  Made with ❤️ by SOLO Agent
</p>

---
---

<a name="english"></a>
## 🎉 Introduction

**MailPulse-Server** is a lightweight email server health monitoring and diagnostics CLI tool, designed for system administrators and developers. It can quickly detect the running status, security configuration, and delivery performance of email servers, helping you ensure the stable operation of your email system.

### 💡 Problems We Solve

- 🔍 **Unclear Server Status**: Don't know if your email server is running properly
- 🛡️ **Complex Security Configuration**: SPF/DKIM/DMARC configurations are hard to verify
- 📊 **Difficult Troubleshooting**: Hard to locate the cause when email sending fails
- ⏱️ **High Monitoring Costs**: Requires professional tools and significant time

### ✨ Key Differentiators

- 🚀 **Zero-Dependency Deployment**: Pure Python implementation, install and run
- 🔒 **Comprehensive Security Audit**: One-click SPF/DKIM/DMARC configuration check
- 📈 **Real-time Health Detection**: Supports SMTP/IMAP/POP3 protocols
- 💻 **Beautiful CLI Interface**: Colorful table output based on Rich library
- ⚡ **Fast Response**: Millisecond-level connection detection

---

## ✨ Core Features

### 🔌 Protocol Health Detection
- **SMTP Detection**: Supports ports 25/587/465, auto-detects STARTTLS
- **IMAP Detection**: Supports ports 143/993, SSL/TLS auto-adaptation
- **POP3 Detection**: Supports ports 110/995, complete connection testing

### 🛡️ Security Configuration Audit
- **SPF Record Detection**: Verify Sender Policy Framework configuration
- **DKIM Record Detection**: Check DomainKeys Identified Mail signatures
- **DMARC Record Detection**: Confirm Domain-based Message Authentication, Reporting & Conformance

### 📊 Comprehensive Diagnostics
- **MX Record Analysis**: Parse mail exchange record priorities
- **Connectivity Testing**: Detect mail server port reachability
- **Smart Recommendations**: Automatically generate optimization suggestions

---

## 🚀 Quick Start

### Requirements

- **Python**: 3.8 or higher
- **OS**: Windows / macOS / Linux

### Installation

```bash
# Option 1: Install via pip (recommended)
pip install mailpulse-server

# Option 2: Install from source
git clone https://github.com/yourusername/mailpulse-server.git
cd mailpulse-server
pip install -r requirements.txt
pip install -e .
```

### Quick Start

```bash
# Show help
mailpulse --help

# Check SMTP server
mailpulse smtp mail.example.com --port 587 --tls

# Check IMAP server
mailpulse imap mail.example.com --port 993 --ssl

# Security audit
mailpulse security example.com --full

# Comprehensive diagnostics
mailpulse diagnose example.com
```

---

## 📖 Detailed Usage Guide

### SMTP Health Detection

```bash
# Basic check (port 25)
mailpulse smtp smtp.gmail.com

# Specify port and timeout
mailpulse smtp mail.example.com --port 587 --timeout 15

# Use TLS encryption
mailpulse smtp mail.example.com --port 465 --tls
```

### Security Configuration Audit

```bash
# Basic check (SPF + DMARC)
mailpulse security example.com

# Full check (SPF + DKIM + DMARC)
mailpulse security example.com --full
```

### Comprehensive Diagnostics

```bash
# One-click domain email configuration diagnosis
mailpulse diagnose example.com
```

### MX Record Analysis

```bash
# Analyze MX records
mailpulse mx example.com
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Simplicity First**: CLI tools should be easy to use, one command for one task
2. **Friendly Output**: Use Rich library for beautiful, readable output
3. **Zero Configuration**: Works out of the box, no complex config files needed
4. **Cross-Platform**: Pure Python implementation, supports all major operating systems

### Technology Choices

| Technology | Reason |
|------------|--------|
| Python 3.8+ | Wide compatibility, rich networking libraries |
| Click | Industry-standard CLI framework, clean decorator syntax |
| Rich | Beautiful terminal output, supports tables, progress bars |
| dnspython | Mature DNS query library, supports various record types |

### Roadmap

- [ ] 📧 Email sending test functionality
- [ ] 📈 Delivery rate statistics analysis
- [ ] 🔔 Blacklist detection
- [ ] 📊 Web Dashboard
- [ ] 🐳 Docker image support
- [ ] 📱 REST API interface

---

## 📦 Packaging & Deployment

### Package as Executable

```bash
# Install packaging tool
pip install pyinstaller

# Package as single file
pyinstaller --onefile --name mailpulse mailpulse/cli.py

# Output located in dist/ directory
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "mailpulse.cli"]
```

```bash
# Build image
docker build -t mailpulse-server .

# Run container
docker run --rm mailpulse-server security example.com
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Submitting PRs

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

### Issue Feedback

- 🐛 Bug reports: Please provide reproduction steps and environment info
- 💡 Feature suggestions: Please describe use cases and expected results
- 📖 Documentation improvements: Feel free to point out errors or deficiencies

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by SOLO Agent
</p>
