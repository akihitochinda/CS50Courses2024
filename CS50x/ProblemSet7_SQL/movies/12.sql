-- List the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred
SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name = "Bradley Cooper"
INTERSECT
SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name = "Jennifer Lawrence"
