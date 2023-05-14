select username, email, 
    count(distinct recensione.imdb_id_film) as films,
    count(distinct seguaci.segue) as seguiti
from utente inner join recensione 
    on utente.id = recensione.id_utente
    inner join seguaci on utente.id = seguaci.id_utente
group by utente.username, email