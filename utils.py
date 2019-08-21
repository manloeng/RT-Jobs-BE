# import json
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore


# cred = credentials.Certificate("firebase-private-key.json")
# default_app = firebase_admin.initialize_app(cred)
# # print(default_app)
# db = firestore.client()


# def delete_collection(coll_ref, batch_size):
#     docs = coll_ref.limit(batch_size).get()
#     deleted = 0

#     for doc in docs:
#         doc.reference.delete()
#         deleted = deleted + 1

#     if deleted >= batch_size:
#         return delete_collection(coll_ref, batch_size)


# delete_collection(db.collection(u'users'), 100)
# delete_collection(db.collection(u'business'), 100)
# delete_collection(db.collection(u'jobDescription'), 100)


# with open('db/testData/users.json') as users:
#     usersArrData = json.load(users)
#     for usersData in usersArrData:
#         # print(usersData)
#         doc_ref = db.collection(u'users').document()
#         doc_ref.set(usersData)


# with open('db/testData/business.json') as business:
#     businessArrData = json.load(business)
#     for businessData in businessArrData:
#         # print(businessData)
#         doc_ref = db.collection(u'business').document()
#         doc_ref.set(businessData)


# with open('db/testData/jobDescription.json') as jobDescription:
#     jobDescriptionArr = json.load(jobDescription)
#     for jobDescription in jobDescriptionArr:
#         # print(jobDescription)
#         doc_ref = db.collection(u'jobDescription').document()
#         doc_ref.set(jobDescription)
