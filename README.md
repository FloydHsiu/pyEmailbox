# Emailbox-Python

## 如何使用

1. 先到 /API/Config.py 內將下方兩個參數設定好

```python
#Gmail Account for Sending System Email
#You need to set up account id and password
GMAIL_ACCOUNT = None
GMAIL_PASSWORD = None
```

2. 到 /API/CreateDatabase.py 內的AddSystemData將自己的資料加入系統

```python
#Add Your Own Data
    cursor.execute("INSERT INTO CLIENTS VALUES(NULL, '1F', 'Wei-Ming', 'Chen', 'test@gmail.com')")
```

3. 安裝(Install it)

```shell
python setup.py install
```

4. 跑起來(Run it)

```
python -m Emailbox
```