FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

# Secret Key
ENV SECRET_KEY=192^r7&oruq+%y3a9izntp&n6kug2@-!oj%!b4wz3&erv0=qa@

# Debug
ENV DEBUG=True

# Allowed Hosts
ENV ALLOWED_HOSTS=localhost,127.0.0.1

# Email settings
ENV EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
ENV EMAIL_HOST=smtp.example.com
ENV EMAIL_PORT=587
ENV EMAIL_USE_TLS=True
ENV EMAIL_HOST_USER=your_email@example.com
ENV EMAIL_HOST_PASSWORD=your_email_password

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
