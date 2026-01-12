release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python create_default_superuser.py
web: gunicorn core.wsgi --log-file -

