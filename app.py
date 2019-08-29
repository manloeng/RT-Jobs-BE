import requests
from requests.packages import urllib3
print(urllib3.__file__)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from flask import jsonify, Flask, request, render_template, abort
import json
import os
from pyrebase import pyrebase
import datetime


app = Flask(__name__)

if 'TEST' in os.environ:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "test-private-key.json"
else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "firebase-private-key.json"

# SET KEYS FROM LOCAL ENVIRONMENT
SECRET_KEY = os.getenv("FIREBASE_API_KEY")
    


# os.environ["FIREBASE_API_KEY"]
# SECRET_KEY = os.getenv("FIREBASE_API_KEY")

# if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
#     print('GOOGLE_APPLICATION_CREDENTIALS in local environment')
# else:
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "firebase-private-key.json"


# AUTH - GETTING USER IDTOKEN

config = {
    "apiKey": SECRET_KEY,
    "authDomain": "flask-auth-84403.firebaseapp.com",
    "databaseURL": "https://flask-auth-84403.firebaseio.com/",
    "storageBucket": "flask-auth-84403.appspot.com",
    "projectId": "flask-auth-84403",
}
configTest = {
    "apiKey": SECRET_KEY,
    "authDomain": "experiment-8e12e.firebaseapp.com",
    "databaseURL": "https://experiment-8e12e.firebaseio.com/",
    "storageBucket": "experiment-8e12e.appspot.com",
    "projectId": "experiment-8e12e",
}
activeConfig = configTest if 'TEST' in os.environ else config


firebase = pyrebase.initialize_app(activeConfig)
pyreAuth = firebase.auth()

datetime_ref = datetime.datetime

@app.route('/api/')
def index():
    with open("endpoints.json", "r") as endpoints_file:
        return json.load(endpoints_file)

@app.route('/api/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
        print(checkauth)
        id_token = checkauth['idToken']
        localId = checkauth['localId']
        display_name = checkauth['displayName']
        verify(id_token)
        if verify(id_token) == "user":
            details = {}
            details["email"] = email
            details["display_name"] = display_name
            details["localId"] = localId
            user = {}
            user["user"] = details
            return jsonify(user)
        return jsonify({"message": "not valid"})
    if request.method == 'GET':
        return jsonify({"message": "please post a user to this endpoint"})


@app.route('/api/business/login', methods=['GET', 'POST'])
def businesslogin():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        checkauth = pyreAuth.sign_in_with_email_and_password(email, password)
        id_token = checkauth['idToken']
        id_token = checkauth['idToken']
        localId = checkauth['localId']
        display_name = checkauth['displayName']
        verify(id_token)
        if verify(id_token) == "business":
            details = {}
            details["email"] = email
            details["display_name"] = display_name
            details["localId"] = localId
            business = {}
            business["business"] = details
            return jsonify(business)
        return jsonify({"message": "not valid"})
    if request.method == 'GET':
        return jsonify({"message": "please post a user tot his endpoint"})


def verify(id_token):
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    print(uid)
    # check if user/ business
    users_ref = db.collection(u'users')
    userData = users_ref.stream()
    for user in userData:
        if uid in user.id:
            print('user logged in')
            return "user"

    business_ref = db.collection(u'business')
    businessData = business_ref.stream()
    for business in businessData:
        if uid in business.id:
            print('business logged in')
            return "business"

# ADMIN SDK - SETTING UP FOR ADMIN PRIVILEGES

default_app = firebase_admin.initialize_app()
db = firestore.client()

@app.route('/api/user/signup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        display_name = data['display_name']
        try:
            # creates a new user in firebase (under the hood)
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
            )
                # then logs in
            checkauth = pyreAuth.sign_in_with_email_and_password(
                email, password)
            print(checkauth, "<-----")
            localId = checkauth['localId']
                # adds user to our database
            doc_ref = db.collection(u'users').document(localId)
            doc_ref.set({u'email': email, u'name': display_name})
        except Exception as e:
            print(e)
            return jsonify("an error has occured")
        details = {}
        details["email"] = email
        details["display_name"] = display_name
        details["localId"] = localId
        user = {}
        user["user"] = details
        return jsonify(user)
    if request.method == 'GET':
        return jsonify({"message": "please post a user to this endpoint"})


@app.route('/api/business/signup', methods=['GET', 'POST'])
def businesssignup():
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        display_name = data['display_name']
        print(email)
        print(password)
        try:
            # creates a new user in firebase (under the hood)
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
            )
            # then logs in
            checkauth = pyreAuth.sign_in_with_email_and_password(
                email, password)
            print(checkauth, "<-----")
            localId = checkauth['localId']
        # adds business to our database
            doc_ref = db.collection(u'business').document(localId)
            doc_ref.set({u'email': email,
                         u'display_name': display_name})
        except:
            return jsonify({'messsage': "error"})
        details = {}
        details["email"] = email
        details["display_name"] = display_name
        details["localId"] = localId
        business = {}
        business["business"] = details
        return jsonify(business)
    if request.method == 'GET':
        return jsonify({"message": "please post a user tot his endpoint"})


@app.route('/api/jobs/', methods=['GET', 'POST'])
def handleJobs():
    if request.method == 'POST':
        data = request.get_json()
        if set(('title', 'vacancies', 'created_by','location','pay','start_time','duration','description')) == set(data):
        #if data['title'] and data['vacancies'] and data['created_by'] and data['location'] and data['pay'] and data['start_time'] and data['duration'] and data['description'] and len(data.keys()) == 8:
            created_at = datetime_ref.now()
            data["created_at"] = created_at
            applicants = []
            data["applicants"] = applicants

            db.collection(u'jobs').add(data)
            docs = db.collection(u'jobs').where(u'created_at', u'==', created_at).where(
                u'created_by', u'==', data['created_by']).stream()
            jobDic = {}
            for doc in docs:
                doc_content = doc.to_dict()
                jobDic["job"] = doc_content
                doc_content["job_id"] = doc.id
            return jsonify(jobDic)
        else:
            abort(400, "Invalid/Missing JSON body keys")
    else:
        docs = db.collection(u'jobs').stream()
        jobsDic = {}
        jobsList = []
        for doc in docs:
            doc_content = doc.to_dict()
            doc_content["job_id"] = doc.id
            jobsList.append(doc_content)
        jobsDic['jobs'] = jobsList
    return jsonify(jobsDic)


@app.route('/api/job/<job_id>', methods=['GET', 'DELETE'])
def handleJob(job_id):
    if request.method == 'GET':
        job = db.collection(u'jobs').document(job_id)
        doc = job.get()
        job_return = {}
        job_dict = doc.to_dict()
        job_return['job'] = job_dict
        if job_dict == None:
            abort(404, "job not found")
        return jsonify(job_return)
    if request.method == 'DELETE':
        job = db.collection(u'jobs').document(job_id)
        if job.get().to_dict() == None:
            abort(404, "job not found")
        job.delete()
        return jsonify({'message': 'deleted'}), 204

@app.route('/api/applications/', methods=['GET', 'POST'])
def handleApplications():
    if request.method == 'POST':
        data = request.get_json()
        if set(('b_uid', 'u_uid', 'job_id')) == set(data):
        # if bool(data['b_uid']) and data['u_uid'] and data['job_id'] and len(data.keys()) == 3:
            created_at = datetime_ref.now()
            confirmation = "null"
            data["created_at"] = created_at
            data["confirmation"] = confirmation

            db.collection(u'applications').add(data)
            job_ref = db.collection(u'jobs').document(data["job_id"])
            job_ref.update(
                {u'applicants': firestore.ArrayUnion([data["u_uid"]])})
            docs = db.collection(u'applications').where(
                u'created_at', u'==', created_at).stream()
            appDic = {}
            for doc in docs:
                doc_content = doc.to_dict()
                appDic["application"] = doc_content
                doc_content["app_id"] = doc.id
            return jsonify(appDic)
        else:
             abort(400, "Invalid/Missing JSON body keys")

    else:
        if request.args.get("user_id"):
            user_id = request.args.get("user_id")
            docs = db.collection(u'applications').where(
                u'u_uid', '==', user_id).stream()
            appDic = {}
            appList = []
            for doc in docs:
                doc_content = doc.to_dict()
                doc_content["applications"] = doc.id
                appList.append(doc_content)
            if len(appList) == 0:
                abort(404,"user not found by id")
            appDic['applications'] = appList
            return jsonify(appDic)

        if request.args.get("job_id"):
            job_id = request.args.get("job_id")
            docs = db.collection(u'applications').where(
                u'job_id', '==', job_id).stream()
            appDic = {}
            appList = []
            for doc in docs:
                doc_content = doc.to_dict()
                doc_content["applications"] = doc.id
                appList.append(doc_content)
            if len(appList) == 0:
                abort(404, "job not found by id")
            appDic['applications'] = appList
            return jsonify(appDic)
        return jsonify({"message": "please provide a valid query"})


@app.route('/api/applications/<app_id>', methods=['PATCH'])
def handleApplication(app_id):
    data = request.get_json()
    app = db.collection(u'applications').document(app_id)
    doc = app.get()
    if doc.to_dict() == None:
        abort(404,"application not found")
    if 'confirmation' in data:
        app_rej = data['confirmation']
        app.update({
            u'confirmation': app_rej,
        })
        app_return = {}
        app_dict = app.get().to_dict()
        app_return['application'] = app_dict
        return jsonify(app_return)
    else: abort(400, "missing confirmation")


if __name__ == '__main__':
    app.run(debug=True)
