SELECT id, name, modified
FROM content.genre
WHERE modified > '%s'
ORDER BY modified;