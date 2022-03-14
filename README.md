<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">

![](static/img/logos/RentaStay-logo.svg)
<h1 align="center">RentaStay</h1>

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a>
            <ul>
                <li><a href="#getting-the-repository">Getting the repository</a></li>
                <li><a href="#setting-up-python">Setting up Python</a></li>
                <li><a href="#setting-up-oracle">Setting up Oracle</a></li>
                <li><a href="#setting-up-the-database">Setting up the Database</a></li>
            </ul>
        </li>
      </ul>
    </li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

RentaStay is an oracle powered bootstrapped Django website inspired by [Airbnb](https://www.airbnb.com/). Here a user can rent rooms that are available in the location they are going. At the same time, they can upload the information of their own house so that others can rent that. Based on this key idea many other features are added to ease access of the site for the users. We tried our best to add as many features as we could in this brief time. 

Watch the video describing detailed features of the website [here](https://youtu.be/EC00IQQwTzk).

The goal of the project was to learn database from the core. So, we were not allowed to use Django's built-in models features.  Instead, we had to use raw sql. Other than that, we had the privilege to use all the other features of Django that made the website easier to build. This was quite a challenging journey but a fun way to learn new things about website development.



### Built With 

#### Database
![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)

#### Backend
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

#### Fronend

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)

![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)

<p align="right"><a href="#top">back to top</a></p>

## Getting Started

Follow the step by step installation procedure to install and run this on your machine

### Prerequisites

Make sure you have python and oracle installed in your device.

**`Python`**: Install Python from [here](https://www.python.org/downloads/).

**`Oracle`**: Install Oracle from [here](http://www.oracle.com/index.html) and register for an account of your own.

### Installation

#### Getting the repository

1. Clone the repo:

    ```sh
    git clone https://github.com/fardinanam/RentaStay.git
    ```

2. If you don't have git installed in your device then download zip

#### Setting up Python

1. Go to the repository base folder and open terminal.

2. Install python packages

    ```sh
    pip install -r requirements.txt
    ```
    This will install all the required packages for this project

#### Setting up Oracle

0. The oracle `TNSListener` and `Services` are supposed to run by default but on windows sometimes these are required to start manually. In that case, in `Windows->Services` find `OracleOraDB19Home2TNSListener` (or just find the one that starts with oracle and ends with Listener) and `OracleServiceORCL`. Start these sequencially.

1. Open SQL Plus

2. Enter credentials

   ```sh
   username: sys as sysdba
   password: password
   ```

3.  Create a new user sa

    ```sql
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

<p align="right"><a href="#top">back to top</a></p>

<!-- CONTACT -->
## Contributors

- [Fardin Anam Aungon](https://github.com/fardinanam)

- [Shehabul Islam Sawraz](https://github.com/Shehabul-Islam-Sawraz)

## Supervisor

- Dr. Rifat Shahriyar

   **Professor**

    Department of Computer Science and Engineering
    Bangladesh University of Engineering and Technology
    Dhaka-1000, Bangladesh

    ▶   **Homepage:**

    [http://rifatshahriyar.github.io/](http://rifatshahriyar.github.io/)

<p align="right"><a href="#top">back to top</a></p>
