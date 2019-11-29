# pytest-db

Pytest操作MySQL

---

### 如何使用

1. 安装 `pytest-db`

使用pip从github安装
```
pip install git+https://github.com/hanzhichao/pytest-db
```

2. 使用方法
在环境变量中添加
```
export DB_URI=mysql://root:password@localhost:3306/test
```
或在pytest.ini中配置
```
[pytest]
db_uri=mysql://root:password@localhost:3306/test
```
或命令行传入
```
$ pytest --db-uri=mysql://root:password@localhost:3306/test
```


3. 使用fixture函数: db
```
def test_a(db):
    print(db.query('select id from user limit 1;')
```
使用pytest -s 运行，查看结果
```
...
[{'id': 123321336}]
...
```
> 游标使用pymysql.cursors.DictCursor，结果使用fetchall,返回列表嵌套字典格式的结果

4. db对象支持的方法
- db.query(sql): 执行查询sql
- db.change_db(sql): 执行修改sql


---

- Email: <a href="mailto:superhin@126.com?Subject=Pytest%20Email" target="_blank">`superhin@126.com`</a> 
- Blog: <a href="https://www.cnblogs.com/superhin/" target="_blank">`博客园 韩志超`</a>
- 简书: <a href="https://www.jianshu.com/u/0115903ded22" target="_blank">`简书 韩志超`</a>

