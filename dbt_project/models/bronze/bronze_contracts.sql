{{ config(materialized='view') }}

SELECT
    id,
    display_title,
    docty                           AS document_type,
    docdt                           AS document_date,
    projectid                       AS project_id,
    loan_no                         AS loan_number,
    admreg                          AS region,
    owner,
    lang                            AS language,
    pdfurl                          AS pdf_url,
    last_modified_date,
    datestored                      AS date_stored,
    disclosure_date,
    no_of_pages
FROM read_parquet(
    '/home/newusermed/procurement-lakehouse/ingestion/data/raw/contracts/*.parquet',
    union_by_name=True
)
