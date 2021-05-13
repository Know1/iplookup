1. Install the GeoIP2 Python libraries
  >pip3 install geoip2

2. Install the Python flask framework
  >pip3 install flask

3. Install Gunicorn to run flask as a service
  >pip3 install gunicorn

4. Clone the Git to target directory
  >git clone https://github.com/Know1/iplookup.git /opt/geoip2

5. Run it Interactively as a test
  >cd /opt/geoip2\
  >gunicorn --pid /run/geoip2.pid -b localhost:5001 iplookup

You should now be able to connect to http://localhost:5001

Optional setup:
1. Set IPLookup to run as a service
  >cp /opt/geoip2/iplookup.service.sample /etc/systemd/system/geoip2.service\
  >systemctl daemon-reload\
  >systemctl enable iplookup.service\
  >systemctl start iplookup.service

2. Configure Apache2 as a reverse proxy to the service
  >cp /opt/geoip2/iplookup.conf.sample /etc/apache2/sites-available/iplookup.conf\
  >a2ensite iplookup\
  >systemctl reload apache2

3. Refresh the Maxmind GeoIP DBs regularly
  >apt install geoipupdate\
  >cp /opt/geoip2/GeoIP.conf.sample /etc/GeoIP.conf\
  >cp /opt/geoip2/geoipupdate.crond.sample /etc/cron.d/geoipupdate
