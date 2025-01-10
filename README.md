PROOF OF CONCEPT:

This project was designed to be an incredibly simple example of how an HTTP botnet
may choose to operate. This specific bot uses "HTTP Polling" which is a low-bandwidth
option fon controlling a large overhead of bots (opposed to other methods such as
WebSockets or HTTP Streaming). Each infected device will make a request to the server
every 30 seconds to get an update as to what needs to be accomplished.

ATTACK METHODS:

   [+] UDP flood
   [+] TCP flood
   [+] HTTP flood
   [+] TLS exhaustion

NOTE:

Each job assigned by the bot master has an ID. This is done so if a bot receives the
same update from the server, the same job isnt carried out twice. This bot is multi-
threaded, so if an active attack is going on, another one or more can be launched
concurrently to engage more targets.

SETUP:

You are going to want to set permissions for your login panel and dashboard so
that no individual can bypass the authentication and access the DDOS panel.

      # Make dashboard readable only by the server and admin (not accessible to public)
      chmod 600 index.html

      # Make authentication script readable only by the server and admin (not accessible to public)
      chmod 600 auth.js
      
      # Make login publicly readable
      chmod 644 login.html

      # or use .htaccess (with Apache) to protect the dashboard

      <Files "index.html">
          Order Deny,Allow
          Deny from all
          Allow from 127.0.0.1
      </Files>

      # the 'client.py' payload will need to be modified as well. When you upload your
      # files, you need to change the variable 'gate_url' to point to your gate.php file
      #
      # example: gate_url = 'http://your-botnet.com/gate.php'

NOTE:
inside of the auth.js is a password for the login. this will need to be updated
to suit your needs.

