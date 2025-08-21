# 信息采集系统

**crawler-system-flask**  
版本号：v2.0.0
90%的代码保留了，删除了部分涉密信息，核心代码都在，大概率可以跑起来，后续有时间再完善

## 📌 项目简介

信息采集系统后端是基于 Flask 框架构建的服务，提供数据采集、邮件推送、用户管理功能。
本意是用于综合管理一些学校公告采集爬虫的平台，爬虫文件已移除，可以按需写在caiji/modules里

## 📦 使用说明

### 1. 克隆项目
```bash
git clone https://gitea.mgcsat.com/MgSziit/infosystem-flask.git
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```
> 由于requirements原因，部分情况下可能需要单独运行
```bash
pip install flask_sqlalchemy
```
> 推荐使用虚拟环境，确保 Python 版本 >= 3.9

### 3. 数据库初始化
```bash
# 导入数据库结构
psql -d jdbc -h localhost -p 5432 -U postgres -f crawler_system_db.sql
```

### 4. 配置文件设置
```bash
# 复制配置文件模板
cp config/config.ini.backup config/config.ini
# 编辑配置文件，填写数据库连接信息、邮件服务器等配置
```

### 5. 启动服务

#### Web API 服务
```bash
python runweb.py
```
默认访问地址：http://localhost:5000

#### 数据采集服务
```bash
python runcaiji.py
```

#### 邮件推送服务
```bash
python runmail.py
```

## 🗂 项目结构说明

```
crawler-system-flask/
├─ crawler_system_db.sql       # 数据库文件
├─ README.md                   # 项目说明文档
├─ requirements.txt            # Python 依赖列表
├─ runcaiji.py                # 数据采集服务启动入口
├─ runmail.py                 # 邮件推送服务启动入口
├─ runweb.py                  # Web API 服务启动入口
├─ www                        # 前端静态资源目录
├─ mailpush                   # 邮件推送模块
│  └─ mail                    # 邮件功能实现
│     ├─ content_builder.py   # 邮件内容构建器
│     ├─ email_count.py       # 邮件计数功能
│     ├─ email_heartbeat.py   # 邮件心跳监控
│     ├─ info_query.py        # 信息查询功能
│     ├─ smtp_client.py       # SMTP 客户端实现
│     └─ update_status.py     # 状态更新功能
├─ logs                       # 日志模块
│  ├─ logger_config.py        # 日志配置文件
│  └─ 2025_08                 # 2025年8月日志目录
├─ config                     # 配置文件目录
│  ├─ config.ini              # 主配置文件
│  ├─ config.ini.backup       # 配置文件备份
│  └─ db.py                   # 数据库连接配置
├─ caiji                      # 数据采集模块
│  ├─ utils                   # 采集工具类
│  │  ├─ common.py            # 通用工具函数
│  │  ├─ config_loader.py     # 配置加载器
│  │  ├─ DrissionPage.iml     # DrissionPage 配置文件
│  │  ├─ operate_base.py      # 基础操作类
│  │  ├─ pool_synchronization.py # 池同步工具
│  │  ├─ read_base.py         # 基础读取类
│  │  └─ send_heartbeat.py   # 心跳发送工具
│  ├─ modules                 # 采集模块实现
│  └─ main                    # 采集主程序
│     ├─ caiji_main.py        # 采集主逻辑
│     ├─ keyword_transmit.py  # 关键词传递功能
│     ├─ modules_logs.py      # 模块日志管理
│     └─ __pycache__          # Python 字节码缓存目录
└─ app                        # Flask 应用核心模块
   ├─ __init__.py             # Flask 应用初始化
   ├─ __pycache__             # Python 字节码缓存目录
   ├─ utils                   # 应用工具类
   │  ├─ recover_caiji.py     # 采集恢复工具
   │  ├─ recover_mail.py      # 邮件恢复工具
   │  └─ __pycache__          # Python 字节码缓存目录
   ├─ routes                  # API 路由模块
   │  ├─ auth.py              # 认证相关路由
   │  ├─ configuration_api.py # 配置管理接口
   │  ├─ crawler_api.py       # 爬虫控制接口
   │  ├─ heartbeat_api.py     # 心跳监控接口
   │  ├─ result_api.py        # 结果查询接口
   │  ├─ users_api.py         # 用户管理接口
   │  ├─ __init__.py          # 路由模块初始化
   │  └─ __pycache__          # Python 字节码缓存目录
   └─ models                  # 数据模型
      ├─ base_crawler.py      # 爬虫基类
      ├─ crawler_config.py    # 爬虫配置模型
      ├─ crawl_pool.py        # 爬虫池管理
      ├─ crawl_results.py     # 采集结果模型
      ├─ heartbeat_model.py   # 心跳监控模型
      ├─ users_model.py       # 用户模型
      ├─ __init__.py          # 模型模块初始化
      └─ __pycache__          # Python 字节码缓存目录
```

## 📡 API 接口说明

主要接口包括：
- `/api/config/*` - 配置管理相关接口
- `/api/crawler/*` - 爬虫控制相关接口
- `/api/heartbeat/*` - 心跳监控相关接口
- `/api/results/*` - 结果查询相关接口
- `/api/users/*` - 用户管理相关接口
- `/api/login/*` - 登录相关接口

## 📄 版本记录

- **v2.0.0**（当前版本）：架构优化，实现Linux移植
- **v1.0.0**（2025-05-08）：初始版本，基础采集功能实现