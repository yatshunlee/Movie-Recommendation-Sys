## About importing csv into the database: (DJANGO)

### Formatting wise:
1) refer to schemas of tables
2) remove columns of csv files after rearrange the columns in the order of the schemas
3) push it by sq

### Coding Wise (may need sqlite3 (since I am using anaconda and I have it with me already)):
1) python manage.py dbshell
2) .tables to check the tables
3) .mode csv
4) .import THECSVFILE TABLE
    e.g. .import movie.csv movie_movie


## About the poster images
check it on google drive and store in local:
SDSC5003\mysite\mysite\static\posters

dont push to github since the file is huge in size

download link:
https://drive.google.com/file/d/1QRXLC2zhaHBK5eYtZD1dyIpcZ5PGtvJU/view?usp=sharing
