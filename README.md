# TelegramBot
提供Telegram主题和背景合并合并，背景提取，随机获取主题 和群组管理的Telegram机器人

配置文件 setup.cfg (采用yaml格式配置)
  机器人api 
          
        telegrambotid: 您的机器人api

  数据库配置（您无须配置数据库中的表 机器人会自动配置）
    
    1.只需在您的mysql中创建
        create database telegramdata;
    2.数据库帐号密码 在setup.cfg里 配置
    3.如果需要在服务器上运行
         请配置mysql超时设置(若未设置 mysql将会默认8小时断开连接，
         而机器人的运行又极度依赖于数据库，所以务必配置数据库超时设置)
    
  违禁词配置
    
    在banconfig/banword配置 每行一个


依赖安装
  
    pip install -r requirement.txt （由于python3.10 的问题 您可能需要手动安装 如果能正常安装就当我没说）

运行
  
    python3 setup.py

