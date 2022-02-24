## Getting Started

Follow the step by step installation procedure to install and run this on your machine

### Prerequisites

Make sure you have python and oracle installed in your device.

**`Python`**: Install Python from [here](https://www.python.org/downloads/)

**`Oracle`**: Install Oracle from [here](http://www.oracle.com/index.html) and register for an account of your own

### Installation

#### Getting the repository

1. Clone the repo:

    ```sh
    git clone https://github.com/fardinanam/RENTASTAY.git
    ```

2. If you don't have git installed in your device then download zip

#### Setting up python

1. Go to the repository base folder and open terminal.

2. Install python packages

    ```sh
    pip install -r requirements.txt
    ```
    This will install all the required packages for this project

#### Setting up Oracle

1. Open SQL Plus

2. Enter credentials

   ```sh
   username: sys as sysdba
   password: password
   ```

3.  Create a new user sa

    ```sh
    create user sa identified by sa;
    grant all privileges to sa;
    ```

#### Setting up the Database

1. Connect to oracle as sa in SQL Plus

2. Copy and paste the codes from sql/schemas.sql and run.

3. Copy and paste the codes from sql/PLSQL.sql and run it. 

    ***Almost there...***

4. copy and paste all the codes from sql/insert_locations.sql and run. (Only the cities of Bangladesh are added here. You can add more if you want.)

5. If no errors are shown we are good to go!

#### One last step

1. Now that everything is set, open terminal in the base directory of the repo.

2. Run the code
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

#### You are all set. Wohoo! 
- Run the server

    ```sh
    python manage.py runserver
    ```