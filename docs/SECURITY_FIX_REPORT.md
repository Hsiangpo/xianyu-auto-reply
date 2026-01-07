# 闲鱼自动回复系统安全清理报告

## 已修复的安全问题

### 1. ✅ 外部数据外发（已移除）

| 风险点       | 文件                      | 修复方式                                               |
| ------------ | ------------------------- | ------------------------------------------------------ |
| 版本检查 API | `reply_server.py:414-433` | 改为返回本地版本信息，不再调用 `xianyu.zhinianblog.cn` |
| 邮件外发 API | `db_manager.py:2872-2903` | 禁用外部 API `dy.zhinianboke.com`，改用本地 SMTP       |
| 商品详情 API | `global_config.yml:24`    | 禁用 `selfapi.zhinianboke.com` 外部 API                |

### 2. ✅ 硬编码凭证（已更新）

| 风险点                            | 文件                   | 修复方式                                             |
| --------------------------------- | ---------------------- | ---------------------------------------------------- |
| 默认密码                          | `reply_server.py:44`   | 改为环境变量 `ADMIN_PASSWORD`（未设置则跳过默认检测） |
| 默认密码                          | `db_manager.py:645`    | 未设置 `ADMIN_PASSWORD` 则拒绝初始化管理员           |
| API 密钥 `xianyu_api_secret_2024` | `reply_server.py:1120` | 改为环境变量 `API_SECRET_KEY` 或随机生成             |
| 硬编码 AI Key/URL                 | `verify_ai.py`         | 改为环境变量 `AI_API_KEY/AI_BASE_URL`                |

### 3. ✅ 测试后门（已移除）

| 风险点                      | 文件                   | 修复方式                           |
| --------------------------- | ---------------------- | ---------------------------------- |
| `zhinina_test_key` 测试密钥 | `reply_server.py:1180` | 完全删除，所有请求必须使用正确密钥 |

### 4. ✅ 前端安全（已更新）

| 风险点           | 文件                                            | 修复方式                     |
| ---------------- | ----------------------------------------------- | ---------------------------- |
| 默认密码自动填充 | `frontend/src/pages/auth/Login.tsx:197`         | 改为显示警告提示             |
| 默认密码显示     | `frontend/src/pages/auth/Login.tsx:255`         | 隐藏具体密码值               |
| 默认密码警告     | `frontend/src/pages/accounts/Accounts.tsx:1332` | 隐藏具体密码值               |
| 编译后静态文件   | `static/assets/*.js`                            | 已重新编译，移除所有敏感信息 |

### 5. ✅ 密码与日志安全（新增）

| 风险点             | 文件                 | 修复方式                                                                 |
| ------------------ | -------------------- | ------------------------------------------------------------------------ |
| 登录密码明文存储   | `db_manager.py`      | 使用 Fernet 加密存储，密钥来自 `PASSWORD_ENCRYPTION_KEY` 或 `JWT_SECRET_KEY` |
| API 密钥日志泄露   | `reply_server.py`    | 验证失败不再记录原始密钥值                                               |
| 默认密码日志泄露   | `reply_server.py`    | 默认密码检查日志不再输出明文                                            |

---

## 部署建议

### 环境变量配置

在部署时，请设置以下环境变量：

```bash
# 管理员密码（必须设置）
export ADMIN_PASSWORD="your_secure_password_here"

# JWT密钥（必须设置）
export JWT_SECRET_KEY="your_jwt_secret_here"

# 登录密码加密密钥（可选，推荐设置）
export PASSWORD_ENCRYPTION_KEY="your_fernet_key_here"

# API密钥（建议设置）
export API_SECRET_KEY="your_api_secret_key_here"

# SMTP配置（邮件功能需要）
export SMTP_SERVER="smtp.example.com"
export SMTP_PORT="587"
export SMTP_USER="your_email@example.com"
export SMTP_PASSWORD="your_email_password"
```

### 数据库重置

如果您之前使用过默认密码或弱口令，建议：

1. 登录后立即修改管理员密码
2. 或删除 `data/xianyu_data.db` 重新初始化

### 前端重新构建

修改前端代码后，需要重新构建：

```bash
cd frontend
npm install
npm run build
```

---

## 仍需注意的事项

1. **定期更新密码**：建议每 3 个月更换管理员密码
2. **监控日志**：检查是否有异常登录尝试
3. **备份数据**：定期备份数据库文件
4. **网络隔离**：建议在内网或 VPN 环境下部署

---

## 修改时间

- 修复日期：2026-01-07
- 修复版本：安全加固版
