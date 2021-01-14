# FlaskJWT



根據 requirements.txt 列表安裝模組：

```console
$ pip install -r requirements.txt
```

使用前記得要調整SERCET KEY(私𫓂)

```python
app.config['JWT_SECRET_KEY'] = '使用前請務必調整此欄'
```

必要套件
- Flask==1.1.2
- Flask-JWT-Extended==3.25.0
- Flask-Script==2.0.6
