DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS question_tag;
DROP TABLE IF EXISTS tag_;

CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    submission_time integer NOT NULL,
    view_number integer,
    vote_number integer,
    title character varying(2550),
    message character varying(2550) NOT NULL,
    image character varying(2550)
);

CREATE TABLE answer (
    id SERIAL PRIMARY KEY,
    submission_time character varying(255) NOT NULL,
    vote_number integer,
    question_id integer,
    message character varying(255) NOT NULL,
    image character varying(255)
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    question_id integer,
    answer_id integer,
    message character varying(255) NOT NULL,
    submission_time character varying(255) NOT NULL,
    edited_number integer
);

INSERT INTO question VALUES
    (0, 1493368154, 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL),
    (1, 1493068124, 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(''.myBook'').booklet() I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine. BUT in my theme i also using jquery via webpack so the loading order is now following: jquery booklet app.js (bundled file with webpack, including jquery)', 'images/image1.png'),
    (2, 1493015432, 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format. This is the code I''m using to draw the image (that works on web/desktop but not cordova built ios app)', NULL);

INSERT INTO answer VALUES
    (0, 1493398154, 5, 0, 'You need to use brackets: my_list = []'),
    (1, 1493088154, 35, 0, 'Look it up in the Python docs');