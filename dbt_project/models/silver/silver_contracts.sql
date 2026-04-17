{{ config(materialized='table') }}

SELECT
    id,
    TRIM(REPLACE(display_title, '\n', ' '))     AS title,
    document_type,
    TRY_CAST(document_date AS TIMESTAMP)        AS document_date,
    YEAR(TRY_CAST(document_date AS TIMESTAMP))  AS document_year,
    project_id,
    loan_number,
    TRIM(region)                                AS region,
    TRIM(owner)                                 AS owner,
    language,
    pdf_url,
    TRY_CAST(disclosure_date AS TIMESTAMP)      AS disclosure_date,
    no_of_pages,
    last_modified_date

FROM {{ ref('bronze_contracts') }}

WHERE id IS NOT NULL
  AND display_title IS NOT NULL
