### Hexlet tests and linter status:
[![Actions Status](https://github.com/AIGelios/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AIGelios/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/b186e999be61aa5b3bf8/maintainability)](https://codeclimate.com/github/AIGelios/python-project-83/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b186e999be61aa5b3bf8/test_coverage)](https://codeclimate.com/github/AIGelios/python-project-83/test_coverage)

### APP on Render.com:
https://page-analyzer-nvps.onrender.com

### About:
Page Analyzer - a web service that analyzes the specified pages for SEO suitability

### Setup and usage:
How to install:
```
git clone git@github.com:AIGelios/python-project-83.git
cd python-project-83
make install
```

How to confugure database:
```
nano .env
```
create 2 environment variables inside the .env file:
```
DATABASE_URL=postgresql://(your database link)
SECRET_KEY=(your secret key for flask app)
```
### Launch the app:
```
make start
``` 