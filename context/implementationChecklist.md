# 📁 Project Setup

- [ ]  Set up Git repository and initial project structure
- [ ]  Choose stack (e.g., Python Flask + Jinja, Node.js + Express + EJS, or similar)
- [ ]  Create Heroku app and connect to Git repo
- [ ]  Configure environment variables and settings
- [ ]  Set up basic routing and template rendering

## 🧩 Database Setup

- [ ]  Design schema using Postgres (or SQLite for local dev)
- [ ]  Define models/tables: Polls, PollDates, Responses, ResponseSelections
- [ ]  Add uniqueness constraint on (poll_id, name) in Responses
- [ ]  Add unique `slug` field to Polls and logic to generate it
- [ ]  Apply migrations or initialize schema

## 🎨 UI Implementation

### Poll Creation Page

- [ ]  Form with poll title (max 80 chars)
- [ ]  Select up to 10 future dates using calendar input
- [ ]  Submit button creates poll and redirects to link

### Poll View Page

- [ ]  Show poll title and list of date options as table headers
- [ ]  Show list of participant names and selected dates
- [ ]  Show tally for each date (number of selections)
- [ ]  Form for name input (max 40 chars)
- [ ]  Checkbox inputs for available dates
- [ ]  Submit response and refresh view

### UI Feedback

- [ ]  Show error if name is duplicate within poll
- [ ]  Show success message on submission

## 🔁 Backend Logic

- [ ]  Handle poll creation: store poll, dates, generate slug
- [ ]  Fetch poll by slug
- [ ]  Validate response name is unique within poll
- [ ]  Store response and selected dates
- [ ]  Query data for table view (participants × dates)

## 🚀 Deployment

- [ ]  Push to Heroku
- [ ]  Set up automated deploy from main branch
- [ ]  Seed test data (optional)
- [ ]  Verify app works end-to-end

## 🧪 Manual Testing

- [ ]  Create a poll and share link
- [ ]  Submit participant response
- [ ]  Submit duplicate name and test validation
- [ ]  Refresh page and verify data persists correctly

## 🧼 Post-MVP Cleanup

- [ ]  Add basic CSS styling for table and forms
- [ ]  Ensure mobile responsiveness
- [ ]  Add favicon and meta tags