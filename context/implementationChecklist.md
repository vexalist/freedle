# �� Project Setup

- [x]  Set up Git repository and initial project structure
- [x]  Choose stack (e.g., Python Flask + Jinja, Node.js + Express + EJS, or similar)
- [x]  Create Heroku app and connect to Git repo
- [x]  Configure environment variables and settings
- [x]  Set up basic routing and template rendering

## 🧩 Database Setup

- [x]  Design schema using Postgres (or SQLite for local dev)
- [x]  Define models/tables: Polls, PollDates, Responses, ResponseSelections
- [x]  Add uniqueness constraint on (poll_id, name) in Responses
- [x]  Add unique `slug` field to Polls and logic to generate it
- [x]  Apply migrations or initialize schema

## 🎨 UI Implementation

### Poll Creation Page

- [x]  Form with poll title (max 80 chars)
- [x]  Select up to 10 future dates using calendar input
- [x]  Submit button creates poll and redirects to link

### Poll View Page

- [x]  Show poll title and list of date options as table headers
- [x]  Show list of participant names and selected dates
- [x]  Show tally for each date (number of selections)
- [x]  Form for name input (max 40 chars)
- [x]  Checkbox inputs for available dates
- [x]  Submit response and refresh view

### UI Feedback

- [x]  Show error if name is duplicate within poll
- [x]  Show success message on submission

## 🔁 Backend Logic

- [x]  Handle poll creation: store poll, dates, generate slug
- [x]  Fetch poll by slug
- [x]  Validate response name is unique within poll
- [x]  Store response and selected dates
- [x]  Query data for table view (participants × dates)

## 🚀 Deployment

- [x]  Push to Heroku
- [ ]  Set up automated deploy from main branch
- [ ]  Verify app works end-to-end

## 🧪 Manual Testing

- [x]  Create a poll and share link
- [x]  Submit participant response
- [x]  Submit duplicate name and test validation
- [x]  Refresh page and verify data persists correctly

## 🧼 Post-MVP Cleanup

- [ ]  Add basic CSS styling for table and forms
- [ ]  Ensure mobile responsiveness
- [ ]  Add favicon and meta tags
- [ ]  Improve homepage
- [ ]  Improve fonts
- [ ]  Make disabled buttons look disabled
- [ ]  Improve spacing
- [ ]  Align checkbox symbol to the middle of square
- [ ]  Remove share link from response page
- [ ]  Tally needs more distance from date

## 🆕 New Features

- [ ]  Add time slots support