# TelegramBot
提供Telegram主题合并，背景提取，群组管理的Telegram机器人

配置
  机器人api
       
       在main2.py的全局变量myapi后添加

  数据库配置（您无须配置数据库中的表 机器人会自动配置）
    
    1.只需在您的mysql中创建
        create database telegramdata;
    2.数据库帐号密码 在mysqlop.py 设置
    
  违禁词配置
    
    在banconfig/banword配置 每行一个


依赖安装
  
    pip install -r requirement.txt （由于python3.10 的问题 您可能需要手动安装 如果能正常安装就当我没说）

运行
  
    python3 main3.py

