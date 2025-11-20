FROM nginx:alpine

# Copy nginx configuration
COPY default.conf /etc/nginx/conf.d/default.conf

# Create directories for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Create directories for frontend static files
RUN mkdir -p /var/www/frontend

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]