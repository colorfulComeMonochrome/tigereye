# tigereye
### 一个模拟的电影院售票网站

##### 以flask框架搭建的API接口

##### 环境：

* Linux  ununtu16.04
* Python3.5.2  Flask 0.12.2  MySQL 5.7  

##### 项目实现功能：

1. 自己定制的json返回对象，每次请求返回相同格式的json对象：

   例：data: 主要的数据    msg:返回的信息(succ: 成功)    rc:  返回状态码(response code)

```json
{
  "data": {
    "address": "\u56db\u5ddd\u7701\u6960\u5e02\u5b5d\u5357\u6bcb\u8857P\u5ea7 308549", 
    "buy_limit": 0, 
    "cid": 1, 
    "halls": 0, 
    "handle_fee": 0, 
    "name": "\u5434\u8857\u5f71\u57ce", 
    "status": 1
  }, 
  "msg": "succ", 
  "rc": 0
}
```

2. 基于ipython的 测试shell：

    不需要手动导入需要的类。在shell启动时，自动创建含有需要包的app

3. 基于unittest 包的自动测试系统

    创建使用sqlite并生成测试数据的虚拟app环境，对方法进行测试

4. 使用nginx + gunicorn + wsgi 将项目部署到本地服务器上

   ​







