from pathlib import Path

# 🔹 Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent


# 🔹 Security
SECRET_KEY = 'django-insecure-j2c3922frnembu3=j)pgd!g6u&$_0dwx=oog-r_(@^&nta)35h'
DEBUG = True
ALLOWED_HOSTS = []


# 🔹 Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'hotel',
]


# 🔹 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 🔹 URLs
ROOT_URLCONF = 'bingebiryani.urls'


# 🔹 Templates (FIXED duplicate DIRS ❌)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ only one DIRS
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# 🔹 WSGI
WSGI_APPLICATION = 'bingebiryani.wsgi.application'


# 🔹 Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔹 Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 🔹 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# 🔹 Static Files
STATIC_URL = 'static/'


# 🔹 Auth Redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = 'login'


# 🔹 Email Configuration (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bingebiriyani@gmail.com'
EMAIL_HOST_PASSWORD = 'oaxe mqmj eyfu ojja'

RAZORPAY_KEY = "rzp_test_SPYWvGotl2ezQR"
RAZORPAY_SECRET = "WlGCwHfVSB6DYDppop6yZ0iy"
