# Viewpoint Diversity App

A quiz to help people learn and develop skills based around viewpoint diversity
Viewpoint Diversity is a psychology-based educational platform designed to bring people together in campuses, companies, organizations, and communities.

## Getting Started

<ul>
    <li>Pull down the repo</li>
    <li>Download python, this will include pip to allow you to download packages</li>
    <li>Open command prompt and navigate to the vda/vda folder</li>
    <li>Run python manage.py runserver, leave this running in the background</li>
    <li>Open an internet browser and navigate to http://localhost:8080/</li>
</ul>

## Prerequisites

<ul>
    <li>Download a python editor</li>
    <li>Download all required packages found in requirements.txt using pip</li>
</ul>


```
Python editor example: PyCharm

```

## Installing

### App Server

1. Download a python editor
```
Recommended editor: PyCharm
```
2. Pull the repo
```
https://gitlab.op-bit.nz/BIT/Project/Viewpoint-Diversity-App/vda.git
```
3. Open vda/vda/manage.py in PyCharm
4. Click 'Configure Python Interpreter' in the top right of the window
```
Will be in a yellow alert bar that will drop down
```
5. In the top right of the new window click the cog then 'Add Local...'
6. Check New environment and choose a location for the virtual environment
7. Change the base interpreter to be python 3.6 or higher
```
If using polytechnic computers select the option 'C:\Program Files(x86)\Python36-32\python.exe'
```
8. Check 'Inherit global site-packages' and press ok
9. You will now have a virtual environment named venv
10. Open command prompt and navigate to it
```
Any command shell will work like powershell
```
11. Inside venv run '.\Scripts\activate'
```
You should now be running in your environment you will have (venv) before your command prompt
```
12. Now navigate to the repo
13. Run the command `pip install -r requirements.txt` this will download all the packages needed
14. Now navigate into the vda folder, there should be a file called manage.py in here
15. Run the command python manage.py runserver
```
Keep this running in the background
```
16. Now open an internet browser and navigate to http://localhost:8080
```
Congrats you have opened the project
```

### SQL Server

1. To edit the data you can go to the django admin by navigating to http://localhost:8080/admin
```
Server must be currently running
```
2. To connect to the database you need to download the latest version of postgreSQL
3. Open pgAdmin 4
```
This will be installed when you install postgreSQL
```
4. In the browser on the left hand side right click Servers and choose create then Server
5. Enter a reasonable name then navigate to the connection tab
6. Set Hostname/address to 10.25.137.189
7. Make sure Port is set to 5432
8. Maintenance database needs to be set to vda
9. And Username is postgres then save
```
By selecting this server you will now be connected to the database
```

### Database Host Server

1. To connect to the linux server which hosts the database you will need to download PuTTY
2. In putty enter 10.25.137.189 as the Host Name and Port 22
3. Make sure connection type is set to SSH
4. In the left navigation bar under category, click into Connection -> SSH -> Auth
5. In the private key section at the bottom select Browse...
6. Navigate to the repo and select postgres.ppk
7. Connect and enter the username: user
```
You are now connected the server which holds the database
```

## Deployment

Whatever you push to the master branch will be updated on the live server
Live server is located at: https://vda.op-bit.nz/

## Built With

* [Python](https://docs.python.org/3/) - The language we used to code in
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Django](https://docs.djangoproject.com/en/2.1/) - The project was built in


## Versioning

- beautifulsoup4==4.6.3
- certifi==2018.8.24
- chardet==3.0.4
- cloudpickle==0.6.1
- dask==0.19.4
- decorator==4.3.0
- Django==2.0.2
- django-cors-headers==2.4.0
- django-rest-framework==0.1.0
- djangorestframework==3.8.2
- idna==2.7
- networkx==2.2
- Pillow==5.3.0
- pytz==2017.3
- PyWavelets==1.0.1
- requests==2.19.1
- six==1.11.0
- toolz==0.9.0
- urllib3==1.23

## Authors

* **Aidyn Jones** - *Initial work* 
* **Fawaz Khan Dinnunhan** - *Initial work* 


## Acknowledgments

* Project based off the Open Mind Platform (https://openmindplatform.org/)
* David Rozado, project manager
