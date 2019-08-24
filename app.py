import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from flask import jsonify, Flask, request, render_template
import json
import os
from pyrebase import pyrebase
import datetime
# import secret

app = Flask(__name__)

SECRET_KEY = os.getenv("FIREBASE_API_KEY")
datetime_ref = datetime.datetime

# Auth -  getting user idToken
config = {
    "apiKey": SECRET_KEY,
    "authDomain": "flask-auth-84403.firebaseapp.com",
    "databaseURL": "https://flask-auth-84403.firebaseio.com/",
    "storageBucket": "flask-auth-84403.appspot.com",
    "projectId": "flask-auth-84403",
}

firebase = pyrebase.initialize_app(config)

pyreAuth = firebase.auth()


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
        return jsonify({"message": "please post a user tot his endpoint"})


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


# @app.route('/user/profile', methods=['GET', 'POST'])
# def userprofile():
#     email = "manloengchung@googlemail.com"
#     user = auth.get_user_by_email(email)
#     # print('Successfully fetched user data: {0}'.format(user.uid))
#     return render_template('loggedIn.html')


# @app.route('/business/profile', methods=['GET', 'POST'])
# def businessprofile():
#     email = "manloengchung@googlemail.com"
#     user = auth.get_user_by_email(email)
#     # print('Successfully fetched user data: {0}'.format(user.uid))
#     return render_template('loggedIn.html')


# # # Admin SDK - setting up for admin privileges
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "firebase-private-key.json"

default_app = firebase_admin.initialize_app()
db = firestore.client()

# # # adds user
@app.route('/api/user/signup', methods=['GET', 'POST'])
def usersignup():
    # need to use dynamic information from the frontend submission
    if request.method == 'POST':
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        display_name = data['display_name']
        print(email)
        print(password)
        # could add name from req form
        try:
            # creates a new user in firebase (under the hood)
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
            )
    #             # then logs in
            checkauth = pyreAuth.sign_in_with_email_and_password(
                email, password)
            print(checkauth, "<-----")
            localId = checkauth['localId']
    # #             # adds data into our data when user signs up and set up its own user obj
    # #             # needs to be more accept a range of data
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
        return jsonify({"message": "please post a user tot his endpoint"})


# # # adding business
@app.route('/api/business/signup', methods=['GET', 'POST'])
def businesssignup():
    #     # need to use dynamic information from the frontend submission
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
        # adds data into our data when user signs up and set up its own user obj
        # needs to be more accept a range of data
            doc_ref = db.collection(u'business').document(localId)
            doc_ref.set({u'email': email,
                         u'display_name': display_name})
        except:
            # should print firebase error
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
        if data['title'] and data['vacancies'] and data['created_by'] and data['location'] and data['pay'] and data['start_time'] and data['duration'] and data['description'] and len(data.keys()) == 8:
            created_at = datetime_ref.now()
            data["created_at"] = created_at
            applicants = []
            data["applicants"] = applicants

            db.collection(u'jobs').add(data)
            # return jsonify(data)
            docs = db.collection(u'jobs').where(u'created_at', u'==', created_at).where(
                u'created_by', u'==', data['created_by']).stream()
            jobDic = {}
            for doc in docs:
                doc_content = doc.to_dict()
                jobDic["job"] = doc_content
                doc_content["job_id"] = doc.id
            return jsonify(jobDic)

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

# getting(for a specific job) and posting applications from a business' perspective
@app.route('/api/applications/', methods=['GET', 'POST'])
def handleApplications():
    if request.method == 'POST':
        data = request.get_json()
        if data['b_uid'] and data['u_uid'] and data['job_id'] and len(data.keys()) == 3:
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
            appDic['applications'] = appList
            return jsonify(appDic)
        return jsonify({"message": "please provide a valid query"})


if __name__ == '__main__':
    app.run(debug=True)
