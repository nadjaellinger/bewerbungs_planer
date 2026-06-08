from enum import Enum

class ApplicationStatus(Enum):
    APPLIED =               "Applied"
    INVITED_FIRST =         "Invited to first interview"
    INTERVIEWED_FIRST =     "Waiting for feedback after first interview"
    INVITED_SECOND =        "Invited to second interview"
    INTERVIEWED_SECOND =    "Waiting for feedback after second interview"
    INVITED_THIRD =         "Invited to third interview"
    INTERVIEWED_THIRD =     "Waiting for feedback after third interview"
    OFFERED =               "Offered"
    REJECTED =              "Rejected"
    ACCEPTED =              "Accepted"
    WITHDRAWN =             "Withdrawn"