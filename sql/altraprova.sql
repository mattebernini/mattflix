select * 
from recensione inner join film
        on recensione.imdb_id_film = film.imdb_id_film
where id_utente = 2