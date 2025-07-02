# Fluffy - a Simple Site Monitor

> Fluffy - Hagrid's 3-headed guard dog


Fluffy is a tool to help monitor sites, and to give me peace of mind that my clients sites are still alive and kicking, and my Cloud Infrastructure skills* are validated.

## How to use

To configure the sites that should be monitored, edit `backend/sites.json` 

Fluffy had a FastAPI backend and a React frontend. To get started, you need to get both services up and running:

### Backend

1. Navigate to the backend directory:

`cd fluffy/backend`

2. Install the dependencies:

`pip install -r requirements.txt`

3. Run the FastAPI server:

`uvicorn main:app --reload`


### Frontend

1. Navigate to the frontend directory:

`cd fluffy/frontend`

2. Install the dependencies:

`npm install`

3. Start the react development server:

`npm start`


## Ideas/Goals
- Selenium to run through common user journey for site
- Notifications when status changes
- Make a hosted service
- user accounts
- database instead of JSON
- prettier dash - graphs and things
