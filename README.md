# Meimodu自动签到脚本

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-自动签到-blue?style=flat-square)](.github/workflows/auto-signin.yml)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
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
# 必填配置（二选一）
# 方式一：使用邮箱密码登录
EMAIL=your-account-email@example.com
PASSWORD=your-password

# 方式二：使用Cookie免登录（与邮箱密码二选一）
COOKIE=your-cookie-value

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
| **认证方式一：邮箱密码登录** |
| `EMAIL` | ✅ | 账号邮箱地址（与PASSWORD配合使用） |
| `PASSWORD` | ✅ | 账号登录密码（与EMAIL配合使用） |
| **认证方式二：Cookie免登录** |
| `COOKIE` | ✅ | 网站登录凭证Cookie，可以通过浏览器开发者工具获取已登录Cookie值（与邮箱密码二选一即可） |
| **通用配置** |
| `TARGET_URL` | ❌ | 目标网站地址（可使用备用地址如 `https://www.meimoai114514.com/`） |

> **⚠重要提示**：请妥善保管你的账号信息，并注意以下事项：
> 1. 认证方式只需选择一种（邮箱密码或Cookie），但如果选择了Cookie也可以填写邮箱密码，在Cookie失效时会尝试使用邮箱密码登录
> 2. 不要泄露账号密码给他人
> 3. 不要在公共场合展示敏感信息
> 4. 如果使用了 `Cookie` 则不要随意登录 `TARGET_URL` 之外的Meimodu网址，这似乎会造成原来的登录信息失效（类似于抢号？），并且 `Cookie` 很可能会有时效性，所以如果想一劳永逸的话还是推荐填写账号密码

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
