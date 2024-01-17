-- | url id | url name | last check date | last check status code |

SELECT
    urls.id, urls.name,
    url_checks.status_code,
    url_checks.created_at
    FROM urls LEFT JOIN url_checks
    ON urls.id = url_checks.url_id
    AND url_checks.created_at = (SELECT
    MAX(created_at) FROM url_checks
    WHERE url_id = urls.id)
    ORDER BY urls.id;