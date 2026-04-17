{{ config(materialized='table') }}

SELECT
    project_id,
    COUNT(*) AS total_documents,
    COUNT(DISTINCT document_type) AS doc_type_diversity,
    MIN(document_date) AS first_document_date,
    MAX(document_date) AS last_document_date,
    MAX(region) AS region,
    MAX(owner) AS owner,
    SUM(TRY_CAST(no_of_pages AS INTEGER)) AS total_pages
FROM {{ ref('silver_contracts') }}
WHERE project_id IS NOT NULL
GROUP BY project_id
ORDER BY total_documents DESC
