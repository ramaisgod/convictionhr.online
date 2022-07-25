from import_export import resources, fields
from apps.recruitment.models import Job, Candidate, Interview
from apps.employee.models import Employee
from apps.client.models import Client, ClientSPOC


class CandidateResource(resources.ModelResource):
    JOB_CODE = fields.Field()
    RECRUITER = fields.Field()

    class Meta:
        model = Candidate
        exclude = ['id', 'RESUME', 'RECRUITER_CODE']

    def dehydrate_JOB_CODE(self, Candidate):
        # return '%s by %s' % (Candidate.JOB_CODE, Candidate.JOB_CODE.JOB_CODE)
        if Candidate.JOB_CODE:
            return Candidate.JOB_CODE.JOB_CODE

    def dehydrate_RECRUITER(self, Candidate):
        if Candidate.RECRUITER:
            return Candidate.RECRUITER.EMPLOYEE_CODE


class InterviewResource(resources.ModelResource):
    CANDIDATE = fields.Field()
    INTERVIEWER_NAME = fields.Field()

    class Meta:
        model = Interview
        exclude = ['id']

    def dehydrate_CANDIDATE(self, Interview):
        if Interview.CANDIDATE:
            return Interview.CANDIDATE.CANDIDATE_ID

    def dehydrate_INTERVIEWER_NAME(self, Interview):
        if Interview.INTERVIEWER_NAME:
            return Interview.INTERVIEWER_NAME.PERSON_NAME


class JobResource(resources.ModelResource):
    CLIENT_CODE = fields.Field()

    class Meta:
        model = Job
        exclude = ['id']

    def dehydrate_CLIENT_CODE(self, Job):
        if Job.CLIENT_CODE:
            return Job.CLIENT_CODE.CUSTOMER_CODE


class EmployeeResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')

    class Meta:
        model = Employee


class ClientResource(resources.ModelResource):

    class Meta:
        model = Client
        exclude = ['id']
