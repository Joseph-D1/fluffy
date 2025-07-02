# Fluffy Development Roadmap

This document outlines the planned features and development phases for the Fluffy site monitoring tool.

## Phase 1: Foundational Upgrade (Database & Users)

This phase focuses on evolving the application from a single-user tool with JSON files into a robust, multi-tenant service ready for new features.

### 1. Database Migration
The goal is to replace the current `sites.json` and `status.json` files with a persistent database.

- **Action:** Choose and set up a PostgreSQL database.
- **Backend:**
    -   Create database models/schema for `Users`, `Sites`, and `StatusChecks`.
        -   `Users`: (id, email, password_hash)
        -   `Sites`: (id, user_id, url, name)
        -   `StatusChecks`: (id, site_id, timestamp, status_code, response_time, status (`Up`/`Down`))
    -   Replace file I/O logic in `main.py` with database queries using an ORM like SQLAlchemy.
    -   The monitoring worker will now write check results to the `StatusChecks` table.
    -   The `/api/status` endpoint will query the database instead of reading a file.

### 2. User Accounts & Multi-Tenancy
The goal is to allow users to sign up, log in, and manage their own list of sites.

- **Backend:**
    -   Implement user registration and login endpoints.
    -   Use JWT (JSON Web Tokens) for securing API endpoints.
    -   Update all API endpoints (e.g., for adding/viewing sites) to be user-specific. They must validate the user's token and only return data owned by that user.
- **Frontend:**
    -   Create login and registration pages.
    -   Implement logic to store the JWT upon login and send it with every API request.
    -   Develop a "dashboard" view where logged-in users can add, view, and delete their own sites.

## Phase 2: Feature Enhancements

With the foundation in place, this phase focuses on adding high-value features for users.

### 1. Prettier Dash - Graphs and Dark Theme
The goal is to enhance the user dashboard with data visualizations and improved aesthetics.

- **Frontend:**
    -   Integrate a charting library (e.g., Chart.js or Recharts).
    -   Create new components to display graphs:
        -   **Response Time Graph:** A line chart showing the response time for a selected site over the last 24 hours.
        -   **Uptime Chart:** A bar chart or a series of colored blocks showing the uptime percentage and history for a site over the last 30 days.
    -   Implement a dark theme. This can be done with a simple toggle switch that adds/removes a `dark` class to the main app container, which will be used by Tailwind CSS (`dark:...` classes).
- **Backend:**
    -   Create new API endpoints to provide aggregated data for the graphs (e.g., `/api/sites/{site_id}/history`).

### 2. Notifications
The goal is to proactively notify users when a site's status changes.

- **Backend:**
    -   Integrate an email sending library (e.g., `fastapi-mail`).
    -   In the monitoring worker, add logic to detect a status change (e.g., from "Up" to "Down").
    -   When a change is detected, trigger an email to the site's owner.
    -   To prevent spamming, add a rule to only send a notification once per outage, until the site comes back up.
- **Future Expansion:** Design the notification system to be pluggable, allowing for other channels like Slack or Discord to be added later.

## Phase 3: Production & Deployment

This phase focuses on making the application a publicly available, hosted service.

### 1. Hosted Service (Infrastructure as Code)
The goal is to deploy the application to a cloud provider and manage the infrastructure using Terraform.

- **Infrastructure (Terraform):**
    -   Write Terraform configuration to provision all necessary cloud resources (e.g., on AWS, GCP, or Azure).
    -   This will include:
        -   A managed PostgreSQL database (e.g., AWS RDS).
        -   Virtual servers or containers (e.g., EC2 or ECS) to run the FastAPI backend.
        -   A static hosting service (e.g., S3/CloudFront) to serve the React frontend.
        -   Networking rules (VPC, security groups) to allow the services to communicate securely.
- **CI/CD:**
    -   Set up a CI/CD pipeline (e.g., using GitHub Actions) to automatically build, test, and deploy the backend and frontend when code is pushed to the main branch.

## Future Goals

### Selenium-Based User Journey Testing
The goal is to expand monitoring from simple uptime checks to complex user workflow validation.

- **Backend:**
    -   Add `selenium` to the Python dependencies.
    -   Update the `Sites` model to include a "check type" (`HTTP` or `Selenium`) and a field for the script content/path.
    -   The monitoring worker will need to be enhanced to run Selenium scripts in a headless browser.
- **Frontend:**
    -   Allow users to select the check type and provide a script when adding/editing a site.
    -   The dashboard will need to be updated to display the results of Selenium tests (e.g., "Flow Passed" or "Flow Failed").
