python manage.py makemigrations
python manage.py migrate
#dcir a django donde encontrar los archivos en el navegador.pegar en urls
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)