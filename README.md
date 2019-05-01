## 启动步骤
1. 先启动Django
2. 再启动Celery Worker 
```celery multi start w1 -A mysite -l info
```
3. 还要启动Redis
```/opt/redis-5.0.0/src# ./redis-server ../redis60025.conf```
