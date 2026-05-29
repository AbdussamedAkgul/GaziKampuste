#!/bin/bash
set -e

echo "Veritabanı migration'ları uygulanıyor..."
flask db upgrade

echo "Gunicorn sunucusu başlatılıyor..."
exec gunicorn --bind 0.0.0.0:5000 run:app
