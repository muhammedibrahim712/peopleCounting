import requests
import json
import time
from datetime import datetime

def updatevisitorinfo(data):
	url = "http://icameraapi.iconnectgroup.com/UpdateVisitorInfo"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	# print(json.dumps(data))
	r = requests.post(url, data=json.dumps(data), headers=headers)
	return r


def getvisitors(data):
	url = "http://icameraapi.iconnectgroup.com/GetVisitors"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	r = requests.post(url, data=json.dumps(data), headers=headers)	
	return r

def getemployeespics(data):
	url = "http://icameraapi.iconnectgroup.com/GetEmployeesPics"
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	# print(json.dumps(data))
	r = requests.post(url, data=json.dumps(data), headers=headers)	
	return r

def savecamerastatus(data):
	url = "http://icamera.iconnectgroup.com/SaveCameraStatus"

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	# print(json.dumps(data))
	r = requests.post(url, data=json.dumps(data), headers=headers)	
	return r



def savevisitorinfo(data):
	url = "http://icameraapi.iconnectgroup.com/SaveVisitorInfo"

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

	# print(json.dumps(data))
	r = requests.post(url, data=json.dumps(data), headers=headers)	
	return r


def uploadimage(files):
	url = "http://icameraapi.iconnectgroup.com/UploadImage?ClientCode=VisTest"	
	r = requests.post(url, files=files)
	return r

# updatevisitorinfo_data = {
# 	"ClientCode":"VisTest",
# 	"CompanyID":"2",
# 	"StoreID":"1",
# 	"Visitors":[
# 		{
# 			"ID":"19780",
# 			"VisitType":""
# 		},
# 		{
# 			"ID":"19781",
# 			"VisitType":"R"
# 		},
# 		{
# 			"ID":"19782",
# 			"VisitType":"R"
# 		}
# 	]
# }

# getvisitors_data = {
# 	"ClientCode":"VisTest",
# 	"CompanyID":"2",
# 	"StoreID":"1",
# 	"Date":"08/31/2019"
# }

# getemployeespics_data = {
# 	"ClientCode":"VisTest",
# 	"CompanyID":"2",
# 	"StoreID":"1",
# 	"Date":"05/31/2017"
# }

# savecamerastatus_data = {
# 	"ClientCode":"VisTest",
# 	"CompanyID":"2",
# 	"StoreID":"1",
# 	"StatusDateTime":"01/23/2017 07:57:37"	
# }

# savevisitorinfo_data = {
# 	"ClientCode":"VisTest",
# 	"CompanyID":"2",
# 	"StoreID":"1",
# 	"Visits":[
# 		{
# 			"NoOfPeople":"1",
# 			"UPS":"1",
# 			"VisitDateTime":"9/03/2016 15:24:21 PM",
# 			"Visitors":[
# 				{
# 					"MinAge":"14",
# 					"MaxAge":"25",
# 					"Gender":"F",
# 					"ActVisitorDateTime":"9/03/2016 15:24:21 PM",
# 					"Picture":"0_1.jpg",
# 					"Name":"test",
# 					"Accuracy":"99.0",
# 					"PicQuality":"G"
# 				}
# 			]
# 		}
# 	]
# }

# files = {'media': open('0_1.jpg', 'rb')}

# print("updatevisitorinfo")
# r = updatevisitorinfo(updatevisitorinfo_data)
# print(r)
# print(r.json())

# print("GetVisitors")
# r = getvisitors(getvisitors_data)
# print(r)
# print(r.json())

# print("getemployeespics")
# r = getemployeespics(getemployeespics_data)
# print(r)
# print(r.json())

# print("savecamerastatus")
# r = savecamerastatus(savecamerastatus_data)
# print(r)
# print(r.json())

# print("savevisitorinfo")
# r = savevisitorinfo(savevisitorinfo_data)
# print(r)
# print(r.json())

# print("uploadimage")
# r = uploadimage(files)
# print(r)
# print(r.json())


# a Python object (dict):

# CompanyID = 2
# StoreID = 1
# min_age = 24
# max_age = 36
# gender = "F"
# tmp_img_path = "face_0.jpg"
# visitor_name = "test"
# accuracy = 99.0
# pic_quality = "G"
# str_time = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")


# savevisitorinfo_data = {}
# savevisitorinfo_data["ClientCode"] = "VisTest"
# savevisitorinfo_data["CompanyID"] = str(CompanyID)
# savevisitorinfo_data["StoreID"] = str(StoreID)

# savevisitorinfo_data_visits = {}
# savevisitorinfo_data_visits["NoOfPeople"] = "1"
# savevisitorinfo_data_visits["UPS"] = "1"
# savevisitorinfo_data_visits["VisitDateTime"] = str_time

# visitors = []

# visits_visitors = {}
# visits_visitors["MinAge"] = str(min_age)
# visits_visitors["MaxAge"] = str(max_age)
# visits_visitors["Gender"] = gender
# visits_visitors["ActVisitorDateTime"] = str_time
# visits_visitors["Picture"] = tmp_img_path
# visits_visitors["Name"] = visitor_name
# visits_visitors["Accuracy"] = str(accuracy)
# visits_visitors["PicQuality"] = str(pic_quality)

# visitors.append(visits_visitors)

# savevisitorinfo_data_visits["Visitors"] = visitors

# visits = []
# visits.append(savevisitorinfo_data_visits)
# savevisitorinfo_data["Visits"] = visits

# # the result is a JSON string:
# print(savevisitorinfo_data)
# print("savevisitorinfo")
# r = savevisitorinfo(savevisitorinfo_data)
# print(r)
# print(r.json())


# ff = 0.3212345234
# asd = "{0:.2f}".format(ff)
# print(type(asd))
# print(asd)