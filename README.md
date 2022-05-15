# Movie-Recommendation-Sys
It is a group project of SDSC5003 Storing and Retrieving Data. Our project is to build a web-based movie recommendation system.
You can search any movie, like and comment, and look for some recommendation on the website.
The dataset is from https://grouplens.org/datasets/movielens/ and poster images from IMDB website.

I built a recommendation system by KNN (collaborative filtering). Lately, I tried to use matrix completion technique to make a better prediction: iterative soft threshold SVD. To enhance the performance, I may try to use the Deep Latent Factor Model (Quite busy recently). 

Demo: https://www.youtube.com/watch?v=qJIU_dSHxOY&t=33s&ab_channel=YatshunLee

## Requirements and Installation
Language: Python (version 3.9.x)

To create a virtual environment for deployment
1. Install anaconda
2. conda create -n djangoenv
3. conda activate djangoenv

To install useful libraries
- conda install django=3.2.9
- pip install django-crispy-forms
- pip install -U scikit-learn==0.23.2
- pip install scipy==1.6.2
- pip install django_static_fontawesome== 5.14
- pip install pandas== 1.3.4

To store the poster images
- check it on google drive and store in local: SDSC5003\mysite\mysite\static\posters
- download link: https://drive.google.com/file/d/1QRXLC2zhaHBK5eYtZD1dyIpcZ5PGtvJU/view?usp=sharing

## Run
1. Open Anaconda command prompt. Compile conda activate djangoenv to activate the virtual environment.
2. Run python manage.py makemigrations to check if the database is valid and python manage.py migrate to deploy the database changes.
3. Deploy our website server by running python manage.py runserver. The following output will show in the terminal:
Starting development server at http://xxx.x.x.x:xxxx/. Then, you can open the website in your browser by the above link.
4. Log in our admin account to test functions of our website: manage users, movies, genres, reviews, and comments.
You may also register a new account to test recommend function, find a movie, create rating and review and leave some comments.
Testing account login credentials:

    |       | username | password |
    |-------|----------|----------|
    | admin |    admin |   123456 |

## Credit to My Groupmates
@ProgrammingAac
@hltung123
