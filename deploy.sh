#!/bin/bash

# ================================================
# Deploy automático para Django en Plesk + Passenger
# Proyecto: devilearn
# Dominio: academia.patchamama.com
# ================================================

# Salir si hay error
set -e

# Ruta al proyecto
PROJECT_DIR="/var/www/vhosts/patchamama.com/academia.patchamama.com/devilearn"

# Activar entorno virtual
echo "Activando entorno virtual..."
source "$PROJECT_DIR/../venv/bin/activate"



# (Opcional) Actualizar código desde Git
# echo "Actualizando repositorio..."
# git pull origin main

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ir a la carpeta del proyecto
cd "$PROJECT_DIR"

# Migraciones de base de datos

echo "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Reiniciar Passenger
echo "Reiniciando Passenger..."
mkdir -p tmp
touch tmp/restart.txt

echo "✅ Deploy completado con éxito"
