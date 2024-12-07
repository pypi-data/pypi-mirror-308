# Django DBackup

Django’nun kendi **dumpdata** komutu her ne kadar işlevsel olsa da, yedeklerinizi UTF-8 formatında almadığı için bazı durumlarda sıkıntılar yaşanabiliyor. İşte bu sorunu çözmek için bu modülü kullanabilirsiniz.

## 📦 Kurulum

1. **Modülü Yükleyin:**

   ```bash
   pip install dbackup

2. **settings.py dosyasında INSTALLED_APPS içine ekleyin**

    ```
    INSTALLED_APPS = [
        'dbackup',
    ]
    ```

## 🛠️ Kullanım

**Komut Satırı ile Yedekleme**
  Veritabanı yedeklerinizi UTF-8 formatında almak için aşağıdaki komutu kullanabilirsiniz:

  ```python manage.py dumpdatautf8```

  Bu komut, varsayılan olarak yedeği proje dizinine **dump_utf8.json** adıyla kaydeder.

**Komut Parametreleri**
  * -o veya --output: Çıktı dosyasının adını belirtir.
     
    ```python manage.py dumpdatautf8 --output=dump.json```
    
  * -i veya --indent: JSON formatında çıktı için girinti seviyesini belirtir.

      ```python manage.py dumpdatautf8 --indent=2```

  * -a veya --app: Belirli bir uygulamanın veritabanı verilerini yedeklemek için kullanılır.

      ```python manage.py dumpdatautf8 --app=auth```

  * -e veya --exclude: Belirli bir uygulamayı veya modeli yedeklemeye dahil etmemek için kullanılır. Birden fazla uygulama veya model için parametreyi tekrarlayın.

      ```python manage.py dumpdatautf8 --exclude=auth --exclude=contenttypes```

