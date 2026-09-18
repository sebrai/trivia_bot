# trivia app

## general info

- **creator:** *sebrai*

- **title:** *trivia bot*

## tech

- **backend:** *python/flask*
- **frontend:** *html,css, jinja2*
- **questions:** *open_trivia api*
[link to site](https://opentdb.com/api_config.php, "open trivia api")
- **database:** *mariadb*

## security

- *password hashes + salt*
- *.env file for password and username*

## db structure

- *users*

``` sql

    +------------+--------------+------+-----+---------------------+-------+
    | Field      | Type         | Null | Key | Default             | Extra |
    +------------+--------------+------+-----+---------------------+-------+
    | id         | varchar(255) | NO   | PRI | uuid()              |       |
    | username   | varchar(31)  | NO   |     | NULL                |       |
    | password   | varchar(255) | NO   |     | NULL                |       |
    | created_at | timestamp    | NO   |     | current_timestamp() |       |
    | score      | int(11)      | NO   |     | 0                   |       |
    +------------+--------------+------+-----+---------------------+-------+


```

- *questions*

``` sql

    +---------+--------------+------+-----+---------+-------+
    | Field   | Type         | Null | Key | Default | Extra |
    +---------+--------------+------+-----+---------+-------+
    | id      | varchar(255) | NO   | PRI | uuid()  |       |
    | text    | varchar(255) | NO   |     | NULL    |       |
    | awnser  | varchar(7)   | YES  |     | NULL    |       |
    | user_id | varchar(255) | NO   | MUL | NULL    |       |
    | user_a  | varchar(7)   | NO   |     | NULL    |       |
    +---------+--------------+------+-----+---------+-------+


```

## idea

- *you can take random trivia with multiple difficulties, the questions are supplied by open trivia api, your account and quiz scores are saved in a db*
