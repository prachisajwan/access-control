from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AccessRequest(BaseModel):
    user: dict
    resource: dict

user = {"name": "Hope", "role": "admin", "department": "Engineering"}
resource = {"name": "salary_report", "owner": "Faith", "sensitivity": "high"}
rules = [
    {"condition": "role=='admin'"},
    {"condition": "role=='owner'"}
    ]

def checkAccess(user, rules, resource):
    
    if user['name'] == resource['owner']:
        return {"Decision": "Permit", "Reason": "User is the owner of the resource"}
    
    for i in range(len(rules)):    
        if user['role'] == rules[i]['condition'].split("==")[1].strip("'"):
            if user['role'] == 'owner':
                if user['name'] != resource['owner']:
                    return {"Decision": "Deny", "Reason": "User is not the owner of the resource"}
            return {"Decision": "Permit", "Reason": f"User role matches condition: {rules[i]['condition']}"}
    return {"Decision": "Deny", "Reason": "User role does not match any condition"}
test_res = checkAccess(user, rules, resource)
print(test_res)


@app.post("/check-access")
def check_access_endpoint(req: AccessRequest):
    return checkAccess(req.user, rules, req.resource) 