SELECT
p.id,
p.full_name,
array_agg(distinct pfw.role)::text[] as roles,
array_agg(distinct pfw.film_work_id)::text[] as film_ids,
p.modified
FROM content.person as p
LEFT JOIN content.person_film_work as pfw on pfw.person_id = p.id
WHERE p.modified > '%s'
group by p.id
ORDER BY modified;