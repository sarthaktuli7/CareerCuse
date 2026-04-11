# CareerCuse
### Syracuse Career Services & Job Placement Tracker
**IST659 Team Project — Spring 2026**

---

## Team
| Name | Role |
|------|------|
| Sarthak | Database design, SQL scripts, data logic |
| Madeline | Streamlit app, front-end screens |
| Lulu   | Data generation, insert scripts |
| Kamdi   | Analytics queries, presentation, team log |

---

## Project Overview
CareerCuse tracks the full student career journey at Syracuse University
from registering with Career Services, applying to jobs, going through
interviews, and landing a placement. It also tracks employers, career fair
events, and salary outcomes, with a built-in analytics dashboard.

---

## Tech Stack
| Layer | Tool |
|-------|------|
| Database | SQL Server (via Docker) |
| App | Python + Streamlit |
| DB connector | pyodbc |
| Charts | Plotly |
| Data generation | Python Faker |
| IDE | VS Code |
| Version control | GitHub |

---

## Quick Start

### 1. Start SQL Server via Docker
```bash
docker run -e "ACCEPT_EULA=Y" \
           -e "SA_PASSWORD=CareerCuse2026!" \
           -p 1433:1433 \
           --name careercuse-sql \
           -d mcr.microsoft.com/mssql/server:2022-latest
```

### 2. Run SQL scripts in order (Azure Data Studio or VS Code SQL extension)
```
01_create_tables_up.sql    -- creates all 10 tables
02_insert_data_up.sql      -- loads sample data
03_data_logic_up.sql       -- views, stored procedures, function, trigger
04_analytics_queries.sql   -- run to verify analytics
```

### 3. (Optional) Regenerate data with Faker
```bash
pip install faker
python generate_data.py > sql/02_insert_data_up.sql
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## Database Schema (10 Tables)
```
student          -- SU student profiles
employer         -- Companies recruiting at SU
job_posting      -- Open roles from employers
application      -- Student job applications
interview        -- Interview records per application
career_event     -- Career fairs and networking events
event_attendance -- Which students attended each event
event_employer   -- Which employers participated in events
placement        -- Final job placements
advisor_note     -- Career advisor meeting notes
```

## Data Logic
| Object | Type | Purpose |
|--------|------|---------|
| v_application_pipeline | View | Full application status view |
| v_placement_analytics | View | Placement stats by school/major |
| p_submit_application | Stored Procedure | Validates and submits an application |
| p_advance_application | Stored Procedure | Updates application status with validation |
| f_student_placement_rate | Function | Returns placement % for a given school |
| trg_auto_fill_posting | Trigger | Auto-marks a posting as Filled on placement |

---

## IST659 Artifacts Checklist
| # | Artifact | Status |
|---|----------|--------|
| 1 | Team name, members, project description | Done |
| 2 | Data analysis Excel (entities, attributes, relationships) | Done |
| 3 | Conceptual ER Diagram | Done |
| 4 | Logical Data Model | Done |
| 5 | External data model & data logic | Done (03_data_logic_up.sql) |
| 6 | Basic screen layout | Done (app.py — 5 screens) |
| 7 | Detailed screen diagrams | In progress |
| 8 | SQL UP/DOWN — internal model + data | Done |
| 9 | SQL UP/DOWN — data migration | N/A (synthetic data) |
| 10 | SQL UP/DOWN — data logic | Done |
| 11 | Application implementation | Done (app.py) |
| 12 | Team log | In progress |
| 13 | Slide deck | In progress |
| 14 | Video — presentation + demo | Pending |
| 15 | Video — reflection | Pending |
