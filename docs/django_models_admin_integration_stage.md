# Django Models & Admin Integration Stage

## Goal
Connect luxury templates with Django database and management panel.

## Core Models

### Page
- title
- slug
- content
- seo_title
- seo_description
- keywords
- schema_type
- status
- timestamps

### EncyclopediaItem
- category
- title
- content
- related_topics
- sources
- seo_metadata

### ContentArticle
- title
- body
- content_type
- author_signature
- publish_status

## Admin Features

- Page management
- Encyclopedia management
- Article review
- SEO metadata control
- Publishing workflow

## Flow

Database
 -> Django Admin
 -> Content Agent
 -> SEO Engine
 -> Publication

## Author Signature Rule

پژوهشگر
مدیر عامل شرکت کشت و صنعت زمرد ملل
مجتبی روزگار
