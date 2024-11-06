# CS50W Projects

### Installation
1. Clone the repository.
    ```bash
    $ git clone https://github.com/whyk47/CS50W.git
    ```
2. Install dependencies.
    ```bash
    $ python.exe -m pip install --upgrade pip
    $ pip install -r requirements.txt
    ```
3. Navigate to the desired project folder.
    ```bash
    $ cd commerce
    ```
4. Start the development Server.
    ```bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver
    ```
5. You should get the following output.
    ```bash
    $ python manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    November 06, 2024 - 20:03:07
    Django version 5.0.4, using settings 'hakoot.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```
    Follow the link to the development server to access the application.

### Project Overview
1. Search: Front-end clone of Google Search, Google Image Search, and Google Advanced Search. [Video Demo](https://youtu.be/0OjAZcYxP5A)
2. Wiki: Wikipedia-like online encyclopedia. [Video Demo](https://youtu.be/Bz9MZXSzDwA)
3. Commerce: eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.” [Video Demo](https://youtu.be/nS1kOXhf24Y)
4. Mail: Front-end for an email client that makes API calls to send and receive emails. [Video Demo](https://youtu.be/31GerWzAL2s)
5. Social Network: Twitter-like social network website for making posts and following users. [Video Demo](https://youtu.be/mDw8EKzzxLM)
6. Hakoot (Capstone Project): Full stack quiz site inspired by Kahoot. [Video Demo](https://youtu.be/61no9QvlWX8)