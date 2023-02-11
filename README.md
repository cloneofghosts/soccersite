# LastEver - Python

A "port" of the LastEver project but using Django and Python. Front end will be mostly the same but the admin side will be done using the default layout that Django provides.

## Added Modules
The module list can be found in the provided requirements.txt.

To install the apps to your local machine:

1. Navigate to your development folder in Command Prompt/PowerShell
2. Run the command pip install -r requirements.txt
3. Once all the apps make sure everything is migrated to the database using python manage.py migrate.
4. Once everything is migrated you can run the server using python manage.py runserver