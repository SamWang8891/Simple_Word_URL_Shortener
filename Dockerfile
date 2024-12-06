FROM library/debian

RUN apt update && \
    apt install -y apt-transport-https lsb-release ca-certificates wget && \
    wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg && \
    echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list && \
    apt update && \
    apt install -y php8.2 php8.2-fpm nginx python3 python3-dotenv python3-pip && \
    pip3 install segno

EXPOSE 80

CMD service php8.2-fpm start && nginx -g "daemon off;" 