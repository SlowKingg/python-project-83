-- Schema for the Page Analyzer database
-- This file defines the `urls` table
-- PostgreSQL-compatible
DROP TABLE IF EXISTS urls;

CREATE TABLE IF NOT EXISTS urls (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
