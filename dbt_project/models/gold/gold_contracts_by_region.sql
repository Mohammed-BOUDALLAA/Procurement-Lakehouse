{{ config(materialized='table') }}

SELECT
    region,
    document_type,
    document_year,
    COUNT(*) AS total_documents,
    COUNT(DISTINCT project_id) AS unique_projects,
    AVG(TRY_CAST(no_of_pages AS INTEGER)) AS avg_pages,
    MIN(document_date) AS earliest_doc,
    MAX(document_date) AS latest_doc
FROM {{ ref('silver_contracts') }}
WHERE region IS NOT NULL
  AND document_year IS NOT NULL
GROUP BY region, document_type, document_year
ORDER BY document_year DESC, total_documents DESC
