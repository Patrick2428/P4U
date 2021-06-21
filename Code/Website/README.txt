1. Install node js : install node js and npm 
i)  https://www.instructables.com/Install-Nodejs-and-Npm-on-Raspberry-Pi/
ii) https://gist.github.com/davps/6c6e0ba59d023a9e3963cea4ad0fb516

2. Install apache2 on rpi

3. Proxy-pass backened server (localhost:3000) to apache2 
 - open and edite /etc/apache2/sites-available/000-default.conf
	sudo nano 000-default.conf 
	enter the line : 'ProxyPass / http://localhost:3000/'
 - enable proxy in apache2
	go to /etc/apache2/sites-enabled/
	run: sudo a2enmod (with this you enable apache modules)
	The two modules to enable are 1.proxy and 2.proxy_http

3. Included dependencies
npm i express
npm i --save-dev nodemon
npm i bcrypt