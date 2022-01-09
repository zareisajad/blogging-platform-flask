# Flask Blogging Platform
![Screenshot 2021-12-20 at 10-33-14 explore](https://user-images.githubusercontent.com/71011395/146785396-41bae187-b7c2-4659-8b32-e6aa164b0a5d.png)

Flask-Blogging Platform is Where you can publish content in the form of blog posts and get feedback from your people and friends.
You can follow your favorite authors and see their posts in your personal feed. Also, the latest published content can be seen in the Explorer section.
of course there is more cool features.

- password reset using email
- create post with html editor(summernote)
- like/unlike ajax
- follow/unfollow
- personal feed
- explore
- search users
- 


## Used In This App:
- python3.8
- flask framework
- Bootstrap5
- SQLite database
- [summernote](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjf6MSTsKT1AhUQ-6QKHS3_AU8QFnoECBkQAQ&url=https%3A%2F%2Fsummernote.org%2F&usg=AOvVaw0bOj5o1D9z1cfWlhrAXezd) the html editor.

## How To Run it:
1. install ```python3```, ```pip3```, ```python3-venv``` in your machine.
2. clone or download the project
3. cd to the app directory then create a virtualenv named ```venv``` using ```python3 -m venv venv```
4. connect to virtualenv using ```source venv/bin/activate``` (it's different on windows os).
5. then install packages using ```pip install -r requirements.txt```
6. next run this command: ```flask db upgrade```
7. now you can run the sever using: ```flask run```
8. finally enter this url in your browser: http://127.0.0.1:5000
