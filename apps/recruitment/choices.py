CHOICE_JOB_TYPE = [
    ('', '---------'),
    ('FULL TIME', 'FULL TIME'),
    ('PART TIME', 'PART TIME'),
    ('PERMANENT', 'PERMANENT'),
    ('TEMPORARY', 'TEMPORARY'),
    ('CONTRACT', 'CONTRACT'),
    ('FREELANCE', 'FREELANCE'),
    ('TRAINING', 'TRAINING')
]

CHOICE_PRIORITY = [
    ('', '---------'),
    ('HIGH', 'HIGH'),
    ('LOW', 'LOW'),
    ('MEDIUM', 'MEDIUM')
]

# CHOICE_SKILL = [
#     ('', '---------'),
#     ('VOICE', 'VOICE'),
#     ('BLENDED', 'BLENDED'),
#     ('DATA', 'DATA'),
#     ('ACCOUNTS', 'ACCOUNTS'),
#     ('IT', 'IT'),
#     ('HR', 'HR'),
#     ('ADMIN', 'ADMIN')
# ]

CHOICE_JOB_STATUS = [
    ('', '---------'),
    ('IN-PROGRESS', 'IN-PROGRESS'),
    ('ON-HOLD', 'ON-HOLD'),
    ('FILLED', 'FILLED'),
    ('CANCELLED', 'CANCELLED'),
    ('INACTIVE', 'INACTIVE')
]

CHOICE_LINE_OF_BUSINESS = [
    ('', '---------'),
    ('INTERNATIONAL', 'INTERNATIONAL'),
    ('DOMESTIC', 'DOMESTIC')
]

CHOICE_INTERVIEW_TYPE = [
    ('', '---------'),
    ('IN PERSON', 'IN PERSON'),
    ('PHONE', 'PHONE'),
    ('VIDEO CONFERENCE', 'VIDEO CONFERENCE')
]

CHOICE_INTERVIEW_ROUND = [
    ('', '---------'),
    ('HR', 'HR'),
    ('TR', 'TR'),
    ('MR/OPERATIONS', 'MR/OPERATIONS'),
    ('V&A', 'V&A'),
    ('APTITUDE-TEST', 'APTITUDE-TEST'),
    ('TEAM LEADER', 'TEAM LEADER'),
    ('AMCAT', 'AMCAT'),
    ('CHAT', 'CHAT'),
    ('CD CHAT', 'CD CHAT'),
    ('CD VOICE', 'CD VOICE'),
    ('VERSANT TEST', 'VERSANT TEST'),
]

CHOICE_INTERVIEW_STATUS = [
    ('', '---------'),
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
    ('ON-HOLD', 'ON-HOLD')
]

CHOICE_SEARCH_BY_CANDIDATE = [
    ('', '--- Search By ---'),
    ('CANDIDATE_ID', 'CANDIDATE_ID'),
    ('CANDIDATE_NAME', 'CANDIDATE_NAME'),
    ('RECRUITER_ID', 'RECRUITER_ID'),
    ('RECRUITER_NAME', 'RECRUITER_NAME'),
    ('CUSTOMER_CODE', 'CUSTOMER_CODE'),
    ('CUSTOMER_NAME', 'CUSTOMER_NAME'),
    ('JOB_CODE', 'JOB_CODE'),
    ('JOB_TITLE', 'JOB_TITLE'),
    ('PAN_NUMBER', 'PAN_NUMBER'),
    ('MOBILE_NUMBER', 'MOBILE_NUMBER'),
    ('EMAIL', 'EMAIL'),
    ('SOURCE', 'SOURCE')
]


CHOICE_SEARCH_BY_INTERVIEW = [
    ('', '--- Search By ---'),
    ('INTERVIEW_ID', 'INTERVIEW_ID'),
    ('CANDIDATE_ID', 'CANDIDATE_ID'),
    ('CANDIDATE_NAME', 'CANDIDATE_NAME'),
    ('RECRUITER_ID', 'RECRUITER_ID'),
    ('RECRUITER_NAME', 'RECRUITER_NAME'),
    ('CUSTOMER_CODE', 'CUSTOMER_CODE'),
    ('CUSTOMER_NAME', 'CUSTOMER_NAME'),
    ('JOB_CODE', 'JOB_CODE'),
    ('JOB_TITLE', 'JOB_TITLE'),
    ('PAN_NUMBER', 'PAN_NUMBER'),
    ('MOBILE_NUMBER', 'MOBILE_NUMBER'),
    ('EMAIL', 'EMAIL')
]

CHOICE_SEARCH_BY_JOB = [
    ('', '--- Search By ---'),
    ('JOB_CODE', 'JOB_CODE'),
    ('JOB_TITLE', 'JOB_TITLE'),
    ('RECRUITER_ID', 'RECRUITER_ID'),
    ('RECRUITER_NAME', 'RECRUITER_NAME'),
    ('CLIENT_CODE', 'CLIENT_CODE'),
    ('CLIENT_NAME', 'CLIENT_NAME'),
    ('JOB_DESCRIPTION', 'JOB_DESCRIPTION'),
    ('REQUIRED_SKILLS', 'REQUIRED_SKILLS'),
    ('CREATED_BY', 'CREATED_BY')
]


CHOICE_SEARCH_BY_ASSIGNED_JOB = [
    ('', '--- Search By ---'),
    ('JOB_CODE', 'JOB_CODE'),
    ('JOB_TITLE', 'JOB_TITLE'),
    ('CLIENT_CODE', 'CLIENT_CODE'),
    ('CLIENT_NAME', 'CLIENT_NAME'),
    ('JOB_DESCRIPTION', 'JOB_DESCRIPTION'),
    ('REQUIRED_SKILLS', 'REQUIRED_SKILLS'),
    ('ASSIGNED_BY', 'ASSIGNED_BY')
]

# Dropdown for experience field
j = [('', '---------')]
for i in range(41):
    j.append((i, i))

CHOICE_EXP = j
