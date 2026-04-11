"""
Synthetic Data Generator

Generates SU and outputs INSERT statements
for 10 tables Run python generate_data.py > 02_insert_data_up.sql

"""

import random
from faker import Faker
from datetime import date, timedelta

fake = Faker()
random.seed(42)

SU_SCHOOLS = [
    ("School of Information Studies", ["Information Management", "Applied Data Science", "Library Science", "Cybersecurity"]),
    ("Whitman School of Management",  ["Finance", "Accounting", "Marketing", "Entrepreneurship", "Supply Chain Management"]),
    ("College of Engineering & Computer Science", ["Computer Science", "Electrical Engineering", "Computer Engineering", "Biomedical Engineering"]),
    ("S.I. Newhouse School of Public Communications", ["Journalism", "Public Relations", "Advertising", "Television, Radio & Film"]),
    ("Maxwell School of Citizenship", ["Public Administration", "International Relations", "Political Science", "Economics"]),
    ("College of Arts & Sciences",    ["Psychology", "Mathematics", "Biology", "Chemistry", "Sociology"]),
]

SU_EMPLOYERS = [
    ("Deloitte",                   "New York",     "NY", "Consulting"),
    ("JPMorgan Chase",             "New York",     "NY", "Finance"),
    ("PwC",                        "New York",     "NY", "Consulting"),
    ("EY",                         "New York",     "NY", "Consulting"),
    ("Amazon",                     "Seattle",      "WA", "Technology"),
    ("Micron Technology",          "Syracuse",     "NY", "Technology"),
    ("SRC Inc.",                   "Syracuse",     "NY", "Defense Technology"),
    ("Lockheed Martin",            "Syracuse",     "NY", "Aerospace & Defense"),
    ("JMA Wireless",               "Syracuse",     "NY", "Technology"),
    ("Barton & Loguidice",         "Syracuse",     "NY", "Engineering"),
    ("Excellus BlueCross BlueShield","Syracuse",   "NY", "Healthcare"),
    ("National Grid",              "Syracuse",     "NY", "Energy & Utilities"),
    ("Welch Allyn (Hill-Rom)",     "Skaneateles Falls","NY","Medical Devices"),
    ("Booz Allen Hamilton",        "McLean",       "VA", "Consulting"),
    ("Goldman Sachs",              "New York",     "NY", "Finance"),
    ("Microsoft",                  "Redmond",      "WA", "Technology"),
    ("Google",                     "Mountain View","CA", "Technology"),
    ("IBM",                        "Armonk",       "NY", "Technology"),
    ("KPMG",                       "New York",     "NY", "Consulting"),
    ("CrowdStrike",                "Austin",       "TX", "Cybersecurity"),
]

JOB_TITLES = {
    "Consulting":            ["Business Analyst", "Consultant", "Associate Consultant", "Management Consultant"],
    "Finance":               ["Financial Analyst", "Investment Banking Analyst", "Risk Analyst", "Quantitative Analyst"],
    "Technology":            ["Software Engineer", "Data Analyst", "Data Engineer", "Product Manager", "Cloud Engineer"],
    "Defense Technology":    ["Systems Engineer", "Software Developer", "Security Analyst"],
    "Aerospace & Defense":   ["Systems Engineer", "Electrical Engineer", "Software Engineer"],
    "Engineering":           ["Civil Engineer", "Structural Engineer", "Project Engineer"],
    "Healthcare":            ["Business Analyst", "IT Analyst", "Data Analyst"],
    "Energy & Utilities":    ["Operations Analyst", "Data Analyst", "Project Manager"],
    "Medical Devices":       ["Systems Engineer", "R&D Engineer", "Quality Engineer"],
    "Cybersecurity":         ["Security Analyst", "Threat Intelligence Analyst", "Penetration Tester"],
}

SU_VENUES = [
    "JMA Wireless Dome",
    "Whitman School of Management",
    "Hinds Hall (iSchool)",
    "Schine Student Center",
    "Link Hall (ECS)",
    "Maxwell Hall",
    "Newhouse Building",
    "Bird Library",
]

EVENT_NAMES = [
    "Fall Career Fair 2025",
    "Spring Career Fair 2026",
    "iSchool Industry Networking Night",
    "Whitman Finance & Consulting Summit",
    "ECS Tech Day",
    "Newhouse Media Industry Panel",
    "SU Internship Expo",
    "Maxwell Public Policy Forum",
    "On-Campus Recruiting Day — Deloitte",
    "SU STEM Career Night",
]

ADVISORS = [
    ("Jennifer", "Pluta",    "j.pluta@syr.edu",   "School of Information Studies"),
    ("Lisette",  "Child",    "l.child@syr.edu",   "Whitman School of Management"),
    ("Nicholas", "Clarke",   "n.clarke@syr.edu",  "College of Engineering & Computer Science"),
    ("Maria",    "Santos",   "m.santos@syr.edu",  "S.I. Newhouse School"),
    ("David",    "Park",     "d.park@syr.edu",    "Maxwell School"),
]

REFERRAL_SOURCES = ["Career Fair", "Handshake", "LinkedIn", "Faculty Referral", "Alumni Network", "On-Campus Recruiting", "Company Website"]
APP_STATUSES     = ["Submitted", "Under Review", "Interview Scheduled", "Offer Extended", "Accepted", "Rejected", "Withdrawn"]
DEGREE_LEVELS    = ["Bachelors", "Masters", "PhD"]
INTERVIEW_TYPES  = ["Phone Screen", "Technical", "Behavioral", "Case Study", "Final Round"]
INTERVIEW_LOCS   = ["Zoom", "On-Campus", "Company Office", "Teams"]
NOTE_TYPES       = ["Initial Meeting", "Resume Review", "Mock Interview", "Career Guidance", "Offer Negotiation", "Follow-up"]


# helperss
def rand_date(start_year=2024, end_year=2026):
    start = date(start_year, 1, 1)
    end   = date(end_year, 3, 1)
    return start + timedelta(days=random.randint(0, (end - start).days))

def sql_str(v):
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"

def sql_date(d):
    return f"'{d}'" if d else "NULL"

def sql_int(v):
    return str(v) if v is not None else "NULL"

def sql_bit(v):
    return "1" if v else "0"


#generatee data
print("-- ============================================================")
print("-- CareerCuse: Synthetic Data (generated via Faker)")
print("-- IST659 Team Project | Spring 2026")
print("-- FILE: 02_insert_data_up.sql")
print("-- ============================================================")
print()
print("USE careercuse;")
print("GO")
print()

#students
print("-- - Students ──────────────────────────────────────────────────────")
print("INSERT INTO student (suid, first_name, last_name, email, phone, major, minor,")
print("    school_college, graduation_year, degree_level, is_international, career_interest, registration_date)")
print("VALUES")

student_rows = []
used_suids   = set()
used_emails  = set()

intl_names = [
    ("Arjun","Sharma"),("Priya","Patel"),("Wei","Zhang"),("Yuki","Tanaka"),
    ("Ananya","Kumar"),("Ravi","Gupta"),("Mei","Liu"),("Kenji","Watanabe"),
    ("Fatima","Al-Rashid"),("Omar","Hassan"),("Siddharth","Nair"),("Ayesha","Khan"),
    ("Hiroshi","Yamamoto"),("Divya","Menon"),("Zheng","Wang"),("Aarav","Singh"),
]
domestic_first = ["Emma","Liam","Olivia","Noah","Ava","Ethan","Sophia","Mason","Isabella","Logan",
                  "Mia","Lucas","Harper","Aiden","Ella","Jackson","Amelia","Carter","Scarlett","Sebastian"]
domestic_last  = ["Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Taylor","Anderson",
                  "Thomas","Moore","Martin","Lee","Thompson","White","Harris","Jackson","Lewis","Walker"]

for i in range(50):
    is_intl = i < 20
    if is_intl:
        fn, ln = intl_names[i % len(intl_names)]
    else:
        fn = random.choice(domestic_first)
        ln = random.choice(domestic_last)

    while True:
        suid = f"SU{random.randint(100000000, 999999999)}"
        if suid not in used_suids:
            used_suids.add(suid)
            break

    base_email = f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@syr.edu"
    while base_email in used_emails:
        base_email = f"{fn.lower()}.{ln.lower()}{random.randint(1,99)}@syr.edu"
    used_emails.add(base_email)

    school, majors = random.choice(SU_SCHOOLS)
    major   = random.choice(majors)
    minor   = random.choice(majors + [None, None])
    if minor == major:
        minor = None
    grad_yr = random.choice([2025, 2026, 2026, 2027])
    degree  = random.choice(["Bachelors","Bachelors","Masters","Masters","PhD"])
    phone   = fake.numerify("(###) ###-####")
    career  = random.choice(["Technology","Finance","Consulting","Data Analytics","Marketing",None])
    reg_dt  = rand_date(2024, 2026)

    row = (f"    ({sql_str(suid)}, {sql_str(fn)}, {sql_str(ln)}, {sql_str(base_email)}, "
           f"{sql_str(phone)}, {sql_str(major)}, {sql_str(minor)}, {sql_str(school)}, "
           f"{grad_yr}, {sql_str(degree)}, {sql_bit(is_intl)}, {sql_str(career)}, {sql_date(reg_dt)})")
    student_rows.append(row)

print(",\n".join(student_rows) + ";")
print("GO\n")

print("-- - Employers ─────────────────────────────────────────────────────")
print("INSERT INTO employer (company_name, industry, city, state, website, recruiter_name,")
print("    recruiter_email, visa_sponsorship, on_campus_recruiter)")
print("VALUES")

employer_rows = []
for name, city, state, industry in SU_EMPLOYERS:
    rec_fn = fake.first_name()
    rec_ln = fake.last_name()
    domain = name.lower().replace(" ", "").replace("&","").replace(".","")[:20] + ".com"
    rec_email = f"{rec_fn.lower()}.{rec_ln.lower()}@{domain}"
    website = f"https://www.{domain}"
    visa = sql_bit(industry in ["Technology","Consulting","Finance"])
    on_campus = sql_bit(random.random() > 0.3)
    row = (f"    ({sql_str(name)}, {sql_str(industry)}, {sql_str(city)}, {sql_str(state)}, "
           f"{sql_str(website)}, {sql_str(rec_fn+' '+rec_ln)}, {sql_str(rec_email)}, "
           f"{visa}, {on_campus})")
    employer_rows.append(row)

print(",\n".join(employer_rows) + ";")
print("GO\n")


print("-- - Job postings ──────────────────────────────────────────────────")
print("INSERT INTO job_posting (employer_id, title, job_type, location, salary_min,")
print("    salary_max, required_skills, visa_sponsorship, status, posted_date, deadline)")
print("VALUES")

posting_rows = []
for j in range(30):
    emp_id   = random.randint(1, 20)
    industry = SU_EMPLOYERS[emp_id - 1][3]
    titles   = JOB_TITLES.get(industry, ["Analyst", "Associate"])
    title    = random.choice(titles)
    job_type = random.choice(["Full-time","Full-time","Full-time","Internship","Co-op"])
    city, state = SU_EMPLOYERS[emp_id - 1][1], SU_EMPLOYERS[emp_id - 1][2]
    location = f"{city}, {state}"
    sal_min  = random.choice([55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000])
    sal_max  = sal_min + random.choice([10000, 15000, 20000, 25000])
    skills   = random.choice(["SQL, Python, Excel", "Python, R, Machine Learning",
                               "Java, AWS, Docker", "Communication, Leadership, Excel",
                               "Tableau, SQL, Data Visualization", "C++, Embedded Systems",
                               "Financial Modeling, Bloomberg, Excel"])
    visa     = sql_bit(industry in ["Technology","Consulting","Finance"])
    status   = random.choice(["Open","Open","Open","Closed","Filled"])
    posted   = rand_date(2024, 2025)
    deadline = posted + timedelta(days=random.randint(30, 90))
    row = (f"    ({emp_id}, {sql_str(title)}, {sql_str(job_type)}, {sql_str(location)}, "
           f"{sal_min}, {sal_max}, {sql_str(skills)}, {visa}, {sql_str(status)}, "
           f"{sql_date(posted)}, {sql_date(deadline)})")
    posting_rows.append(row)

print(",\n".join(posting_rows) + ";")
print("GO\n")

print("-- - Applications ──────────────────────────────────────────────────")
print("INSERT INTO application (student_id, posting_id, status, applied_date,")
print("    last_updated, referral_source, notes)")
print("VALUES")

app_rows  = []
used_apps = set()
for _ in range(60):
    while True:
        sid = random.randint(1, 50)
        pid = random.randint(1, 30)
        if (sid, pid) not in used_apps:
            used_apps.add((sid, pid))
            break
    status     = random.choice(APP_STATUSES)
    applied_dt = rand_date(2024, 2026)
    updated_dt = applied_dt + timedelta(days=random.randint(1, 60))
    referral   = random.choice(REFERRAL_SOURCES)
    notes      = random.choice([None, None, "Strong candidate", "Referred by alumni", "Applied online"])
    row = (f"    ({sid}, {pid}, {sql_str(status)}, {sql_date(applied_dt)}, "
           f"{sql_date(updated_dt)}, {sql_str(referral)}, {sql_str(notes)})")
    app_rows.append(row)

print(",\n".join(app_rows) + ";")
print("GO\n")

print("-- - Interviews ────────────────────────────────────────────────────")
print("INSERT INTO interview (application_id, interview_date, interview_type,")
print("    location, interviewer_name, outcome, feedback)")
print("VALUES")

int_rows = []
app_ids  = random.sample(range(1, 61), 35)
for app_id in app_ids:
    int_date    = rand_date(2024, 2026)
    int_type    = random.choice(INTERVIEW_TYPES)
    location    = random.choice(INTERVIEW_LOCS)
    interviewer = fake.name()
    outcome     = random.choice(["Passed","Passed","Passed","Failed","Pending","Pending"])
    feedback    = random.choice([None, None, "Strong technical skills", "Good cultural fit",
                                  "Needs improvement in communication", "Excellent problem-solving"])
    row = (f"    ({app_id}, {sql_date(int_date)}, {sql_str(int_type)}, {sql_str(location)}, "
           f"{sql_str(interviewer)}, {sql_str(outcome)}, {sql_str(feedback)})")
    int_rows.append(row)

print(",\n".join(int_rows) + ";")
print("GO\n")

print("-- - Career events ─────────────────────────────────────────────────")
print("INSERT INTO career_event (event_name, event_date, location, event_type,")
print("    description, expected_attendees, budget)")
print("VALUES")

event_rows = []
for idx, ename in enumerate(EVENT_NAMES):
    ev_date  = rand_date(2024, 2026)
    venue    = SU_VENUES[idx % len(SU_VENUES)]
    etype    = random.choice(["Career Fair","Networking","Info Session","Workshop","Panel"])
    desc     = f"Annual {etype.lower()} connecting SU students with top recruiters."
    expected = random.choice([50, 100, 150, 200, 300, 500])
    budget   = random.choice([1000, 2500, 5000, 7500, 10000, 15000])
    row = (f"    ({sql_str(ename)}, {sql_date(ev_date)}, {sql_str(venue)}, {sql_str(etype)}, "
           f"{sql_str(desc)}, {expected}, {budget})")
    event_rows.append(row)

print(",\n".join(event_rows) + ";")
print("GO\n")


print("-- - Event attendance ──────────────────────────────────────────────")
print("INSERT INTO event_attendance (event_id, student_id, registered, attended, notes)")
print("VALUES")

att_rows   = []
used_atts  = set()
for _ in range(40):
    while True:
        eid = random.randint(1, 10)
        sid = random.randint(1, 50)
        if (eid, sid) not in used_atts:
            used_atts.add((eid, sid))
            break
    registered = 1
    attended   = sql_bit(random.random() > 0.2)
    notes      = random.choice([None, None, "Met with Deloitte recruiter", "Submitted resume", "Followed up via email"])
    row = f"    ({eid}, {sid}, {registered}, {attended}, {sql_str(notes)})"
    att_rows.append(row)

print(",\n".join(att_rows) + ";")
print("GO\n")


print("-- - Event employers ───────────────────────────────────────────────")
print("INSERT INTO event_employer (event_id, employer_id, booth_number, positions_available)")
print("VALUES")

ee_rows  = []
used_ee  = set()
for _ in range(20):
    while True:
        eid = random.randint(1, 10)
        emp = random.randint(1, 20)
        if (eid, emp) not in used_ee:
            used_ee.add((eid, emp))
            break
    booth    = f"Booth {random.randint(1, 50)}"
    openings = random.randint(1, 10)
    row = f"    ({eid}, {emp}, {sql_str(booth)}, {openings})"
    ee_rows.append(row)

print(",\n".join(ee_rows) + ";")
print("GO\n")

print("-- - Placements ────────────────────────────────────────────────────")
print("INSERT INTO placement (student_id, employer_id, posting_id, job_title,")
print("    start_date, salary, placement_type, notes)")
print("VALUES")

pl_rows   = []
used_sids = set()
for _ in range(20):
    while True:
        sid = random.randint(1, 50)
        if sid not in used_sids:
            used_sids.add(sid)
            break
    emp_id  = random.randint(1, 20)
    pid     = random.randint(1, 30)
    industry= SU_EMPLOYERS[emp_id - 1][3]
    title   = random.choice(JOB_TITLES.get(industry, ["Analyst"]))
    start   = rand_date(2025, 2026)
    salary  = random.choice([60000,65000,70000,75000,80000,85000,90000,95000,100000,110000,120000])
    ptype   = random.choice(["Full-time","Full-time","Full-time","Internship"])
    notes   = random.choice([None, None, "Placed via career fair", "Referred by advisor", "On-campus recruiting"])
    row = (f"    ({sid}, {emp_id}, {pid}, {sql_str(title)}, {sql_date(start)}, "
           f"{salary}, {sql_str(ptype)}, {sql_str(notes)})")
    pl_rows.append(row)

print(",\n".join(pl_rows) + ";")
print("GO\n")

print("-- - Advisor notes ─────────────────────────────────────────────────")
print("INSERT INTO advisor_note (student_id, advisor_name, advisor_email,")
print("    meeting_date, note_type, notes)")
print("VALUES")

note_rows = []
for _ in range(30):
    sid    = random.randint(1, 50)
    adv    = random.choice(ADVISORS)
    mdate  = rand_date(2024, 2026)
    ntype  = random.choice(NOTE_TYPES)
    note   = random.choice([
        "Reviewed resume and suggested industry-specific keywords.",
        "Discussed internship search strategy and target companies.",
        "Conducted mock interview — strong performance overall.",
        "Student secured offer, negotiation guidance provided.",
        "Explored graduate school vs. industry career paths.",
        "Identified skill gaps, recommended Python and SQL courses.",
    ])
    row = (f"    ({sid}, {sql_str(adv[0]+' '+adv[1])}, {sql_str(adv[2])}, "
           f"{sql_date(mdate)}, {sql_str(ntype)}, {sql_str(note)})")
    note_rows.append(row)

print(",\n".join(note_rows) + ";")
print("GO\n")
print("PRINT '>> All synthetic data inserted successfully.';")
print("GO")
