"""
CareerCuse - Syracuse Career Services & Job Placement Tracker
IST659 Team Project | Spring 2026

"""

import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="CareerCuse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=careercuse.database.windows.net,1433;"
        "DATABASE=careercuse;"
        "UID=stuli01;"
        "PWD=Sar123thak@;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

def run_query(sql, params=None):
    conn = get_connection()
    try:
        if params:
            return pd.read_sql(sql, conn, params=params)
        return pd.read_sql(sql, conn)
    except Exception as e:
        st.error(f"Query error: {e}")
        return pd.DataFrame()

def run_exec(sql, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return True, "Success"
    except Exception as e:
        conn.rollback()
        return False, str(e)

# ── Sidebar nav ───────────────────────────────────────────────────────────────
try:
    st.sidebar.image("Logo.png", width=140)
except:
    pass

st.sidebar.markdown("## CareerCuse")
st.sidebar.markdown("Syracuse Career Services Tracker")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Students", "Jobs & Employers", "Applications", "Career Events"],
    index=0,
)

st.sidebar.divider()
st.sidebar.caption("IST659 Team Project · Spring 2026")


# PAGE 1DASHBOARD

if page == "Dashboard":
    st.title("📊 CareerCuse Analytics Dashboard")
    st.caption("Placement trends, pipeline health, and employer insights for Syracuse University")

    col1, col2, col3, col4 = st.columns(4)

    total_students  = run_query("SELECT COUNT(*) AS n FROM student").iloc[0]["n"]
    total_placed    = run_query("SELECT COUNT(*) AS n FROM placement").iloc[0]["n"]
    total_apps      = run_query("SELECT COUNT(*) AS n FROM application").iloc[0]["n"]
    total_employers = run_query("SELECT COUNT(*) AS n FROM employer").iloc[0]["n"]
    placement_rate  = round(total_placed / total_students * 100, 1) if total_students > 0 else 0

    col1.metric("Total Students",    f"{total_students:,}")
    col2.metric("Students Placed",   f"{total_placed:,}")
    col3.metric("Placement Rate",    f"{placement_rate}%")
    col4.metric("Partner Employers", f"{total_employers:,}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Placement Rate by School")
        df_school = run_query("""
            SELECT s.school_college AS School,
                   COUNT(DISTINCT s.student_id) AS Total,
                   COUNT(DISTINCT p.student_id) AS Placed,
                   CAST(COUNT(DISTINCT p.student_id) * 100.0 /
                        NULLIF(COUNT(DISTINCT s.student_id),0) AS DECIMAL(5,1)) AS Rate
            FROM student s
            LEFT JOIN placement p ON s.student_id = p.student_id
            GROUP BY s.school_college
            ORDER BY Rate DESC
        """)
        if not df_school.empty:
            fig = px.bar(df_school, x="Rate", y="School", orientation="h",
                         color="Rate", color_continuous_scale="Blues",
                         labels={"Rate": "Placement %"}, text="Rate")
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            fig.update_layout(showlegend=False, height=320, margin=dict(l=0,r=20,t=10,b=10),
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Application Pipeline Funnel")
        df_funnel = run_query("""
            SELECT status AS Stage, COUNT(*) AS Count
            FROM application
            GROUP BY status
            ORDER BY Count DESC
        """)
        if not df_funnel.empty:
            stage_order = ["Submitted","Under Review","Interview Scheduled",
                           "Offer Extended","Accepted","Rejected","Withdrawn"]
            df_funnel["order"] = df_funnel["Stage"].apply(
                lambda x: stage_order.index(x) if x in stage_order else 99)
            df_funnel = df_funnel.sort_values("order")
            fig2 = go.Figure(go.Funnel(
                y=df_funnel["Stage"], x=df_funnel["Count"],
                textinfo="value+percent initial",
                marker={"color": ["#005BBB","#1A73E8","#4A9FDE","#78C4F0","#A8DFF7","#D95F5F","#E8A0A0"]}
            ))
            fig2.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Salary Distribution (Placed Students)")
        df_sal = run_query("SELECT salary FROM placement WHERE salary IS NOT NULL")
        if not df_sal.empty:
            fig3 = px.histogram(df_sal, x="salary", nbins=15,
                                labels={"salary": "Annual Salary ($)"},
                                color_discrete_sequence=["#005BBB"])
            fig3.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=10), showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.subheader("Top Hiring Employers")
        df_emp = run_query("""
            SELECT e.company_name AS Employer, COUNT(p.placement_id) AS Placements
            FROM placement p
            JOIN employer e ON p.employer_id = e.employer_id
            GROUP BY e.company_name
            ORDER BY Placements DESC
        """)
        if not df_emp.empty:
            fig4 = px.bar(df_emp.head(8), x="Placements", y="Employer",
                          orientation="h", color_discrete_sequence=["#D44500"],
                          text="Placements")
            fig4.update_traces(textposition="outside")
            fig4.update_layout(height=280, margin=dict(l=0,r=20,t=10,b=10))
            st.plotly_chart(fig4, use_container_width=True)

    st.subheader("International vs Domestic — Placement Comparison")
    df_intl = run_query("""
        SELECT
            CASE WHEN s.is_international = 1 THEN 'International' ELSE 'Domestic' END AS Type,
            COUNT(DISTINCT s.student_id) AS Total,
            COUNT(DISTINCT p.student_id) AS Placed,
            CAST(COUNT(DISTINCT p.student_id)*100.0 /
                 NULLIF(COUNT(DISTINCT s.student_id),0) AS DECIMAL(5,1)) AS Rate
        FROM student s
        LEFT JOIN placement p ON s.student_id = p.student_id
        GROUP BY s.is_international
    """)
    if not df_intl.empty:
        c5, c6, c7 = st.columns(3)
        for _, row in df_intl.iterrows():
            col = c5 if row["Type"] == "Domestic" else c6
            col.metric(f"{row['Type']} — Placement Rate", f"{row['Rate']}%",
                       f"{row['Placed']} of {row['Total']} students")


# PAGE 2 STUDENTS

elif page == "Students":
    st.title("🎓 Student Management")

    tab1, tab2 = st.tabs(["View Students", "Add Student"])

    with tab1:
        st.subheader("All Students")
        col1, col2, col3 = st.columns(3)
        school_filter = col1.selectbox("Filter by School", ["All"] + [
            "School of Information Studies",
            "Martin J. Whitman School of Management",
            "College of Engineering and Computer Science",
            "S.I. Newhouse School of Public Communications",
            "Maxwell School of Citizenship and Public Affairs",
            "College of Arts and Sciences",
        ])
        degree_filter = col2.selectbox("Degree Level", ["All", "Bachelors", "Masters", "PhD"])
        intl_filter   = col3.selectbox("Student Type", ["All", "International", "Domestic"])

        where = ["1=1"]
        if school_filter != "All":
            where.append(f"school_college = '{school_filter}'")
        if degree_filter != "All":
            where.append(f"degree_level = '{degree_filter}'")
        if intl_filter == "International":
            where.append("is_international = 1")
        elif intl_filter == "Domestic":
            where.append("is_international = 0")

        df_students = run_query(f"""
            SELECT student_id AS ID, suid AS SUID,
                   first_name + ' ' + last_name AS Name,
                   email AS Email, major AS Major,
                   school_college AS School,
                   CAST(graduation_year AS VARCHAR(4)) AS GradYear,
                   degree_level AS Degree,
                   CASE WHEN is_international=1 THEN 'Yes' ELSE 'No' END AS International
            FROM student
            WHERE {' AND '.join(where)}
            ORDER BY last_name, first_name
        """)
        st.dataframe(df_students, use_container_width=True, height=420)
        st.caption(f"{len(df_students)} students found")

    with tab2:
        st.subheader("Register New Student")
        with st.form("add_student_form"):
            c1, c2 = st.columns(2)
            suid       = c1.text_input("SUID (e.g. SU100000026)")
            fname      = c1.text_input("First Name")
            lname      = c1.text_input("Last Name")
            email      = c1.text_input("SU Email")
            phone      = c2.text_input("Phone (optional)")
            major      = c2.text_input("Major")
            minor      = c2.text_input("Minor (optional)")
            school     = c2.selectbox("School / College", [
                "School of Information Studies",
                "Martin J. Whitman School of Management",
                "College of Engineering and Computer Science",
                "S.I. Newhouse School of Public Communications",
                "Maxwell School of Citizenship and Public Affairs",
                "College of Arts and Sciences",
            ])
            c3, c4     = st.columns(2)
            grad_yr    = c3.number_input("Graduation Year", 2025, 2030, 2026)
            degree     = c3.selectbox("Degree Level", ["Bachelors", "Masters", "PhD"])
            is_intl    = c4.checkbox("International Student (F1/J1)")
            career_int = c4.text_input("Career Interest (optional)")
            submitted  = st.form_submit_button("Register Student", type="primary")

        if submitted:
            if not all([suid, fname, lname, email, major, school]):
                st.error("Please fill in all required fields.")
            else:
                ok, msg = run_exec("""
                    INSERT INTO student (suid, first_name, last_name, email, phone, major, minor,
                        school_college, graduation_year, degree_level, is_international,
                        career_interest, registration_date)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (suid, fname, lname, email, phone or None, major, minor or None,
                      school, grad_yr, degree, 1 if is_intl else 0,
                      career_int or None, date.today()))
                if ok:
                    st.success(f"Student {fname} {lname} registered successfully!")
                    st.cache_resource.clear()
                else:
                    st.error(f"Error: {msg}")



# PAGE 3 JOBS & EMPLOYERS

elif page == "Jobs & Employers":
    st.title("🏢 Jobs & Employers")

    tab1, tab2 = st.tabs(["Job Postings", "Employers"])

    with tab1:
        st.subheader("Open Job Postings")
        col1, col2 = st.columns(2)
        job_type_f = col1.selectbox("Job Type", ["All","Full-time","Internship","Co-op"])
        visa_f     = col2.checkbox("Visa Sponsorship Only")

        where = ["jp.status = 'Open'"]
        if job_type_f != "All":
            where.append(f"jp.job_type = '{job_type_f}'")
        if visa_f:
            where.append("jp.visa_sponsorship = 1")

        df_jobs = run_query(f"""
            SELECT jp.posting_id AS ID,
                   e.company_name AS Company,
                   jp.title AS Title,
                   jp.job_type AS Type,
                   jp.location AS Location,
                   CONCAT('$', FORMAT(jp.salary_min,'N0'), ' - $', FORMAT(jp.salary_max,'N0')) AS Salary,
                   jp.required_skills AS Skills,
                   CASE WHEN jp.visa_sponsorship=1 THEN 'Yes' ELSE 'No' END AS VisaSponsorship,
                   jp.deadline AS Deadline
            FROM job_posting jp
            JOIN employer e ON jp.employer_id = e.employer_id
            WHERE {' AND '.join(where)}
            ORDER BY jp.posted_date DESC
        """)
        st.dataframe(df_jobs, use_container_width=True, height=420)
        st.caption(f"{len(df_jobs)} open postings")

    with tab2:
        st.subheader("Employer Directory")
        df_emp = run_query("""
            SELECT e.employer_id AS ID,
                   e.company_name AS Company,
                   e.industry AS Industry,
                   e.city + ', ' + e.state AS Location,
                   e.recruiter_name AS Recruiter,
                   e.recruiter_email AS RecruiterEmail,
                   CASE WHEN e.visa_sponsorship=1 THEN 'Yes' ELSE 'No' END AS VisaSponsorship,
                   CASE WHEN e.on_campus_recruiter=1 THEN 'Yes' ELSE 'No' END AS OnCampus,
                   COUNT(jp.posting_id) AS OpenPostings
            FROM employer e
            LEFT JOIN job_posting jp ON e.employer_id = jp.employer_id AND jp.status='Open'
            GROUP BY e.employer_id, e.company_name, e.industry, e.city, e.state,
                     e.recruiter_name, e.recruiter_email, e.visa_sponsorship, e.on_campus_recruiter
            ORDER BY e.company_name
        """)
        st.dataframe(df_emp, use_container_width=True, height=420)


# PAGE 4  APPLICATIONS

elif page == "Applications":
    st.title("📋 Application Pipeline")

    tab1, tab2 = st.tabs(["View Pipeline", "Submit Application"])

    with tab1:
        st.subheader("Application Pipeline")
        df_pipe = run_query("""
            SELECT a.application_id AS AppID,
                   s.first_name + ' ' + s.last_name AS Student,
                   s.school_college AS School,
                   e.company_name AS Employer,
                   jp.title AS Position,
                   a.status AS Status,
                   a.applied_date AS Applied,
                   a.referral_source AS Source,
                   CASE WHEN i.interview_id IS NOT NULL THEN 'Yes' ELSE 'No' END AS Interviewed
            FROM application a
            JOIN student s ON a.student_id = s.student_id
            JOIN job_posting jp ON a.posting_id = jp.posting_id
            JOIN employer e ON jp.employer_id = e.employer_id
            LEFT JOIN interview i ON a.application_id = i.application_id
            ORDER BY a.applied_date DESC
        """)

        status_filter = st.multiselect(
            "Filter by Status",
            ["Submitted","Under Review","Interview Scheduled","Offer Extended","Accepted","Rejected","Withdrawn"],
            default=[]
        )
        if status_filter:
            df_pipe = df_pipe[df_pipe["Status"].isin(status_filter)]

        st.dataframe(df_pipe, use_container_width=True, height=420)
        st.caption(f"{len(df_pipe)} applications")

        st.divider()
        st.subheader("Advance Application Status")
        st.caption("Uses stored procedure p_advance_application")
        col1, col2 = st.columns(2)
        app_id_input = col1.number_input("Application ID", min_value=1, step=1)
        new_status   = col2.selectbox("New Status", [
            "Under Review","Interview Scheduled","Offer Extended","Accepted","Rejected","Withdrawn"])
        if st.button("Update Status", type="primary"):
            ok, msg = run_exec("EXEC p_advance_application ?, ?", (int(app_id_input), new_status))
            if ok:
                st.success(f"Application {app_id_input} updated to '{new_status}'")
            else:
                st.error(f"Error: {msg}")

    with tab2:
        st.subheader("Submit New Application")
        st.caption("Uses stored procedure p_submit_application")
        with st.form("submit_app_form"):
            c1, c2 = st.columns(2)

            df_s = run_query("SELECT student_id, first_name + ' ' + last_name AS name FROM student ORDER BY last_name")
            df_p = run_query("""
                SELECT jp.posting_id,
                       e.company_name + ' - ' + jp.title AS label
                FROM job_posting jp
                JOIN employer e ON jp.employer_id = e.employer_id
                WHERE jp.status = 'Open'
                ORDER BY e.company_name
            """)

            student_opts = {row["name"]: row["student_id"] for _, row in df_s.iterrows()}
            posting_opts = {row["label"]: row["posting_id"] for _, row in df_p.iterrows()}

            sel_student = c1.selectbox("Student", list(student_opts.keys()))
            sel_posting = c1.selectbox("Job Posting", list(posting_opts.keys()))
            referral    = c2.selectbox("Referral Source", [
                "Career Fair","Handshake","LinkedIn","Faculty Referral",
                "Alumni Network","On-Campus Recruiting","Company Website"])
            notes       = c2.text_area("Notes (optional)")
            submitted   = st.form_submit_button("Submit Application", type="primary")

        if submitted:
            sid = student_opts[sel_student]
            pid = posting_opts[sel_posting]
            ok, msg = run_exec("EXEC p_submit_application ?, ?, ?, ?",
                               (sid, pid, referral, notes or None))
            if ok:
                st.success(f"Application submitted for {sel_student}!")
            else:
                st.error(f"Error: {msg}")



# PAGE 5 CAREER EVENTS

elif page == "Career Events":
    st.title("📅 Career Events")

    tab1, tab2 = st.tabs(["Events & Attendance", "Event ROI"])

    with tab1:
        st.subheader("Upcoming & Past Events")
        df_events = run_query("""
            SELECT ce.event_id AS ID,
                   ce.event_name AS Event,
                   ce.event_date AS Date,
                   ce.location AS Venue,
                   ce.event_type AS Type,
                   ce.expected_attendees AS Expected,
                   COUNT(DISTINCT ea.student_id) AS Registered,
                   SUM(CASE WHEN ea.attended=1 THEN 1 ELSE 0 END) AS Attended,
                   COUNT(DISTINCT ee.employer_id) AS Employers,
                   '$' + FORMAT(ce.budget,'N0') AS Budget
            FROM career_event ce
            LEFT JOIN event_attendance ea ON ce.event_id = ea.event_id
            LEFT JOIN event_employer ee ON ce.event_id = ee.event_id
            GROUP BY ce.event_id, ce.event_name, ce.event_date, ce.location,
                     ce.event_type, ce.expected_attendees, ce.budget
            ORDER BY ce.event_date DESC
        """)
        st.dataframe(df_events, use_container_width=True, height=360)

        st.divider()
        st.subheader("Student Attendance by Event")
        df_att = run_query("""
            SELECT ce.event_name AS Event,
                   s.first_name + ' ' + s.last_name AS Student,
                   s.major AS Major,
                   CASE WHEN ea.attended=1 THEN 'Attended' ELSE 'No-show' END AS Status,
                   ea.notes AS Notes
            FROM event_attendance ea
            JOIN career_event ce ON ea.event_id = ce.event_id
            JOIN student s ON ea.student_id = s.student_id
            ORDER BY ce.event_date DESC
        """)
        st.dataframe(df_att, use_container_width=True, height=300)

    with tab2:
        st.subheader("Career Event ROI Analysis")
        st.caption("Connecting event spending to actual placements")
        df_roi = run_query("""
            SELECT ce.event_name AS Event,
                   ce.budget AS Budget,
                   COUNT(DISTINCT ea.student_id) AS StudentsAttended,
                   COUNT(DISTINCT p.placement_id) AS Placements,
                   CASE
                       WHEN COUNT(DISTINCT p.placement_id) > 0
                       THEN CAST(ce.budget * 1.0 / COUNT(DISTINCT p.placement_id) AS DECIMAL(10,2))
                       ELSE NULL
                   END AS CostPerPlacement
            FROM career_event ce
            LEFT JOIN event_attendance ea ON ce.event_id = ea.event_id AND ea.attended = 1
            LEFT JOIN student s ON ea.student_id = s.student_id
            LEFT JOIN placement p ON s.student_id = p.student_id
            GROUP BY ce.event_id, ce.event_name, ce.budget
            ORDER BY Placements DESC
        """)
        if not df_roi.empty:
            c1, c2 = st.columns(2)
            with c1:
                fig = px.scatter(df_roi, x="Budget", y="Placements",
                                 text="Event", size="StudentsAttended",
                                 color="Placements", color_continuous_scale="Blues",
                                 labels={"Budget": "Event Budget ($)", "Placements": "Placements Generated"})
                fig.update_traces(textposition="top center")
                fig.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.dataframe(df_roi, use_container_width=True, height=350)