# CareerCuse
### Syracuse University Career Services & Job Placement Tracker
**IST659 — Data Administration Concepts & Database Management | Spring 2026 | Section M002 | Prof. Kelvin King**

---

## The Team

| Name | Role |
|------|------|
| Sarthak Tuli | Database design, Azure SQL setup, SQL scripts, data logic |
| Madeline | Streamlit app, front-end screens |
| Lulu | Data generation, insert scripts |
| Kamdi | Analytics queries, presentation, team log |

---

## What We Built

CareerCuse is a career services tracking system built for Syracuse University Career Services staff. It tracks students from the moment they register all the way through to placement — applications, interviews, employer relationships, career fair attendance, salary outcomes, and advisor notes all in one place.

We built it because there is no single system at SU that connects all of this. Advisors currently work across spreadsheets and disconnected tools. CareerCuse gives them a live dashboard and a real database behind it.

One angle we felt strongly about was visa sponsorship tracking. As international students ourselves, we know how much it matters to filter employers and job postings by whether they sponsor H1B or OPT. That is a feature we built in from the start.

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Database | Azure SQL — careercuse.database.windows.net |
| App | Python + Streamlit |
| DB Connector | pymssql |
| Charts | Plotly Express + Plotly Graph Objects |
| Data | Python Faker (synthetic) |
| IDE | VS Code |
| Version Control | GitHub |

---

## Quick Start

**1. Install Python dependencies**
```bash
pip install streamlit pymssql pandas plotly
```

**2. Run the app**
```bash
streamlit run app.py
```

Opens in your browser at `http://localhost:8501`. Connects to Azure SQL automatically — no local database setup needed.

---

## Database Schema — 10 Tables

```
student            SU student profiles
employer           Companies recruiting at SU
job_posting        Open roles from employers
application        Student job applications
interview          Interview records per application
career_event       Career fairs and networking events
event_attendance   Which students attended each event
event_employer     Which employers participated in events
placement          Final job placements
advisor_note       Career advisor meeting notes
```

---

## Data Logic Objects

| Object | Type | Purpose |
|--------|------|---------|
| v_application_pipeline | View | Full pipeline with student, employer and job details |
| v_placement_analytics | View | Placement stats by school and major |
| p_submit_application | Stored Procedure | Validates and submits a new application |
| p_advance_application | Stored Procedure | Updates application status with validation |
| f_student_placement_rate | Function | Returns placement % for a given school |
| trg_auto_fill_posting | Trigger | Auto-marks a posting as Filled when a student is placed |

---

## SQL Scripts

Run in this order in VS Code against Azure SQL:

```
sql/01_create_tables_up.sql     creates all 10 tables
sql/02_insert_data_up.sql       loads sample data
sql/03_data_logic_up.sql        deploys views, stored procedures, function, trigger
sql/04_analytics_queries.sql    16 analytical queries for verification
```

Each script has a matching DOWN script to reset everything if needed.

---

## App Screens

- **Dashboard** — live KPIs, placement rate by school, application funnel, salary distribution, top employers, international vs domestic comparison
- **Students** — filterable directory with school, degree and type filters, add new student form
- **Jobs & Employers** — open postings with visa sponsorship filter, full employer directory
- **Applications** — pipeline tracker, advance status via stored procedure, submit new application via stored procedure
- **Career Events** — event attendance records, ROI analysis connecting event spend to placement outcomes

---

## Azure Setup Notes

- Subscription: Azure for Students
- Server: careercuse.database.windows.net
- Region: West US 2
- Tier: General Purpose Serverless Gen5 1 vCore
- Database auto-pauses after inactivity — first connection takes 20-30 seconds to wake up
- Each teammate's IP must be added to the Azure firewall under Server → Networking

---

## IST659 Artifacts

| # | Artifact | Status |
|---|----------|--------|
| 1 | Team name, members, project description | Done |
| 2 | Data analysis Excel — entities, attributes, relationships | Done |
| 3 | Conceptual ER Diagram | Done |
| 4 | Logical Data Model | Done |
| 5 | External data model and data logic | Done — 03_data_logic_up.sql |
| 6 | Basic screen layouts | Done — app.py 5 screens |
| 7 | Detailed screen diagrams | Done — App Walkthrough doc |
| 8 | SQL UP/DOWN — internal model and data | Done |
| 9 | SQL UP/DOWN — data migration | Done — generate_data.py |
| 10 | SQL UP/DOWN — data logic | Done |
| 11 | Application implementation | Done — running on Azure SQL |
| 12 | Team log | Done |
| 13 | Slide deck | Done |
| 14 | Video — presentation and demo | Pending |
| 15 | Video — individual reflection | Pending |
