# Meimodu自动签到脚本

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-自动签到-blue?style=flat-square)](.github/workflows/auto-signin.yml)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen?style=flat-square)](LICENSE)

一个基于Python的Meimodu/Meimoai网站自动签到工具，支持GitHub Actions自动定时执行。

## 功能摘要

- 自动使用邮箱密码登录获取Token，随后执行签到任务
- 启用 GitHub Actions 后项目会自动在每天UTC时间00:00（北京时间08:00）执行签到

## 配置说明
### 本地运行

1. **克隆项目**

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
创建 `.env` 文件（可选，或直接在config.py中配置）：
```bash
# 必填配置
EMAIL=your-account-email@example.com
PASSWORD=your-password

# 可选配置
TARGET_URL=https://www.meimoaix.com/
```

4. **运行签到**
```bash
python main.py
```

### GitHub Actions使用

1. Fork本项目

2. 设置Secrets（项目Settings → Secrets and variables → Actions）

### 环境变量 / GitHub Secrets

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `EMAIL` | ✅ | 账号邮箱 |
| `PASSWORD` | ✅ | 账号密码 |
| `TARGET_URL` | ❌ | 目标网站地址（可使用备用地址如 `https://www.meimoai114514.com/`） |

> 请妥善保管你的账号密码，不要泄露给他人，不要在公共场合展示敏感信息，否则后果自负

### 日志查看

- **本地运行**: 查看控制台输出和 `logs/` 目录下的日志文件
- **GitHub Actions**: 在仓库的Actions页面查看执行日志

## 注意事项
   - 使用环境变量或GitHub Secrets存储账号密码
   - 请合理使用脚本，避免对服务器造成压力
   - 请遵守网站的使用条款
   - 仅用于个人学习和自动化工具研究

---

**免责声明**: 本项目仅供学习和研究使用，请遵守相关网站的使用条款，使用者需自行承担风险。