

```py

# Database configuration - V1
DATABASE_URL = config(
    'DATABASE_URL',
    default=f'sqlite:///{BASE_DIR}/db.sqlite3'
)
print(DATABASE_URL)
DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}
print(DATABASES)


# Database configuration - V2
# Vérifier si on est en développement
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASE_URL = config('DATABASE_URL')
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True
        )
    }
#print(DATABASE_URL)



# Database configuration - V3
# Configuration de la base de données
if DEBUG:
    # Base de données de développement
    DATABASE_URL = config(
        'DEV_DATABASE_URL',
        default='postgresql://pamoja_db_owner:guoE3jILT4pF@ep-icy-brook-a21a9iky.eu-central-1.aws.neon.tech/pamoja_db_dev?sslmode=require'
    )
else:
    # Base de données de production
    DATABASE_URL = config(
        'PROD_DATABASE_URL',
        default='postgresql://pamoja_db_owner:guoE3jILT4pF@ep-icy-brook-a21a9iky.eu-central-1.aws.neon.tech/pamoja_db?sslmode=require'
    )

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}