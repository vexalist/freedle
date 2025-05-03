## Purpose

Enable users to quickly create and share a link for a group to indicate availability across a set of dates — no login, no complexity. Ideal for casual group scheduling.

## Target Audience

- Small groups (friends, clubs, teams) organizing events
- Users who want to avoid account creation or app installs

## Core Features (MVP)

- Create a poll with title and up to 10 date options
- Shareable link with a short slug for others to access the poll
- Participants can enter a name and select any subset of dates
- All responses are visible in a table format
- Names must be unique within a poll
- Poll data is immutable — no edits or deletes

## Non-Goals

- No authentication or user accounts
- No notifications or email integration
- No time zone support or time-of-day granularity
- No poll editing or admin controls

## Success Criteria

- A user can create and share a poll link within 2 minutes
- Participants can clearly view all responses and submit their own
- Duplicate names are gracefully blocked with a helpful error