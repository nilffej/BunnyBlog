# BunnyBlog by Team BunnyTruffles
### Project Manager: Ahmed Sultan
### Roster: Jeff Lin, Leia Park and Ahmed Sultan

#### Our Project
BunnyBlog is a blog website designed by Team BunnyTruffles. Through BunnyBlog, visitors to the website will have access to a public Discover page of all blogs posted on BunnyBlog, as well as the individual blog pages of individual users. Registered users will be able to post their own blogs.

#### How to Run Our Project
0. Install Flask
    ```
    $ pip3 install flask
     ```
1. Clone our repo from GitHub.
    ```
    $ git clone git@github.com:nilffej/BunnyBlog.git
    ```
2. Initiate a Flask virtual environment.
    - to create virtual environment
    ```
    $ python3 -m venv hero
    ```
    - to activate virtual environment
    ```
    $ . ~/hero/bin/activate
    ```

3. Navigate to the BunnyBlog directory.
    - utilize `cd` to enter directory

4. Run: `$ python app.py`
5. Open a web browser and go to 127.0.0.1:5000

#### Using BunnyBlog
- The Discover Page is the landing page for all BunnyBlog visitors—regardless of whether or not they are logged in. From the Discover Page, one can 
    - Read all users' posts
    - Navigate to specific users' profiles through the side User panel
- BunnyBlog visitors may register or log in using the buttons located on the top right of the page.
- Logged-in users may access their own blog by clicking the 'My Profile' button in the top-right.
- On their profile, logged-in users may write a new post by typing in entries and clicking Submit.
- Logged-in users can log out of their sessions.
