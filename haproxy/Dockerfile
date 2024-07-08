# Usa l'immagine ufficiale di HAProxy
FROM haproxy:2.4-alpine

# Imposta una directory di lavoro temporanea
WORKDIR /tmp

# Copia il file di configurazione di HAProxy
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

# Crea la directory per il certificato SSL temporaneamente
RUN mkdir -p ssl

# Copia il certificato SSL nella directory temporanea
COPY fullchain.pem ssl/cert.pem

# Sposta la directory ssl nella destinazione finale con i privilegi appropriati
USER root
RUN mv ssl /usr/local/etc/haproxy/ssl

# Imposta l'utente predefinito per HAProxy
USER haproxy
