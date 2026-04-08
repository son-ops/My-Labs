FROM php:8.4-apache

RUN apt-get update \
    && apt-get install -y \
        libzip-dev \
        zip \
        unzip \
    && docker-php-ext-install zip \
    && a2enmod headers \
    && rm -rf /var/lib/apt/lists/*

COPY ./configs/apache2.conf /etc/apache2/apache2.conf
COPY ./configs/000-default.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /var/www/html

COPY ./src/ /var/www/html/

RUN mkdir -p /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html/uploads \
    && chmod -R 775 /var/www/html/uploads \
    && chown root:www-data /var/www/html

RUN name=$(tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 8) && echo 'SSS{test_flag}' > /${name}_flag.txt

EXPOSE 80