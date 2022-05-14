# Movie-Recommendation-Sys
Using dataset from https://grouplens.org/datasets/movielens/ to build a recommendation system by KNN.
Besides, for future update, we can also use matrix completion technique to make a better prediction: like iterative soft threshold SVD or even deep latent factor model.

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