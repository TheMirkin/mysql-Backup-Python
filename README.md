# MySQL-Backup-Python


MySQL yedekleme için Database Ayarlarını json dosyasından kendinize göre düzenleyin : 
```json
{
  "db": {
    "host": "localhost",
    "user": "root",
    "pass": "password",
    "dbname": "dbname",
    "file": "dosya.sql"
  }
}
```

Kullanımı : 
```
python Backup.py
```
### Başka birşey yapmanıza gerek yok bulunduğu dizine dosyanızı kaydedicektir.

