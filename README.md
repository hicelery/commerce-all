# commerce-all

A Django e-commerce platform for product browsing, cart management, checkout, user accounts, reviews, discounts, and admin operations.

Live site: https://commerce-all-7e9e664f7d53.herokuapp.com/

## Overview

The app provides a complete shopping flow with catalog browsing, product filtering, checkout, order history, and a staff dashboard for content and moderation.

## Tech Stack

- Django 4.2
- PostgreSQL
- Cloudinary for image storage
- django-allauth for authentication and Google sign-in
- Crispy Forms, Django Summernote, WhiteNoise, and Gunicorn

## Run Locally

### Prerequisites

- Python 3.12
- PostgreSQL
- Cloudinary account
- Optional: Google OAuth credentials and SMTP email settings

### Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure the required environment variables.
5. Run migrations and start the server.

```bash
git clone <repository-url>
cd IFA_FINAL
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The project expects `DATABASE_URL` to point to PostgreSQL. Set environment variables in your shell or in a local `env.py` file before starting the app.

Required environment variables:

- `SECRET_KEY`
- `DATABASE_URL`
- `CLOUDINARY_URL`

Optional environment variables:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`

To create an admin account:

```bash
python manage.py createsuperuser
```

Then open `/admin` after logging in.

### Hosted Online

Use the live site link above to access the deployed version. The app is hosted on Heroku with Gunicorn, and media assets are served through Cloudinary.

## Features

- Product catalogue with filtering, sorting, and search
- Product detail pages with image galleries and reviews
- Cart, shipping, discount code, and checkout flow
- User accounts with order history
- Admin tools for products, categories, discounts, reviews, and contact or order queries
- Google account sign-in
- Responsive navigation and breadcrumb support

## UX Design

The design uses a simple, playful visual style aimed at a younger shopping audience. The layout is built around a modular data model so product, cart, checkout, and account flows stay consistent across desktop and mobile layouts. Wireframes and database planning were used to keep the site easy to navigate and scalable.

## Agile

Development was split into three sprints and managed through a kanban board with MoSCoW prioritisation. User stories were broken into smaller delivery tasks, with testing and grooming states used to keep iteration focused. After the MVP, the workflow moved toward a gitflow-style release process.

## Testing

Automated Django tests cover the main models, forms, and views. The suite currently contains 316 tests with a 100% pass rate and 95% overall coverage. Manual UX checks, Lighthouse audits, and accessibility validation were also used. Full results and detailed coverage notes are in [TESTING_EXIT_REPORT.md](TESTING_EXIT_REPORT.md).

## AI Retrospective

Main use case of AI in this project:

Project planning and organisation tooling
Code creation (for simple, easy to define use cases)
Debugging
Test pack creation

AI was most useful for planning, boilerplate generation, debugging support, and expanding the test suite. A custom Copilot agent helped standardise work into clear tasks and checkpoints. The main lesson was that AI output was strongest when given full workspace context and a narrow task, with manual review still needed for redundant or invalid code.

## References

- Design inspiration: https://www.ssense.com/en-gb/, https://london.doverstreetmarket.com/
- Beast Mode reference: https://gist.github.com/burkeholland/1366d67f8d59247e098b6df3c6a6e38
