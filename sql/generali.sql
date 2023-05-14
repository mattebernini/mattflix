select *
from (
    select count(*) as numero_utenti
    from utente
) as t1
natural join
(
    select count(*) as numero_recensioni
    from recensione
) as t2
natural join
(
    select count(*) as numero_film
    from film
) as t3
natural join
(
	select count(*) as interazioni
	from seguaci
) as t4
