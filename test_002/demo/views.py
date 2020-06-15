from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from demo.models import DocterInfo, PatientInfo,RecordInfo
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
import time
from django.core import serializers


def getuser(request):
    u = DocterInfo.objects.all()

    context = {
        "doctor":u
    }
    return render(request, "home.html",context = context)


def test(request):
    cursor = connection.cursor()
    cursor.execute("select * from docter_info")
    row = cursor.fetchone()
    cursor.close()

    return JsonResponse(row,safe=False)




def login(request):
    if request.method == "GET":
        username = request.GET.get("username", default=0)
        pwd = request.GET.get("pwd", default=0)
    doctor = DocterInfo.objects.filter(doctor_account = username, doctor_pwd = pwd)
    if doctor.exists():
        data = {
            "code": "0000",
            "doctor_name": doctor[0].doctor_name,
            "doctor_sex": doctor[0].doctor_sex,
            "doctor_tel": doctor[0].doctor_tel,
            "doctor_department": doctor[0].doctor_department,
            "doctor_job": doctor[0].doctor_job,
            "doctor_id": doctor[0].doctor_id
        }
        print(data)
    else:
        data = {
        }
    return JsonResponse(data)

@csrf_exempt
def showdata(request):
    p_data = []
    if request.method == "GET":

        doctor_id = request.GET.get("doctor_id", default=0)
        #print(doctor_name)
        pat_info = RecordInfo.objects.filter\
            (r_p__p_d__doctor_id = doctor_id).values_list("r_p__patient_id",
            "r_p__patient_name", "r_p__patient_sex","record_date"
            ,"r_p__p_d__doctor_name","r_p__patient_age","r_p__patient_allergy")

        for i in pat_info:
            data = {
                "patient_id":i[0],
                "patient_name": i[1],
                "patient_sex": i[2],
                "patient_date": i[3],
                "doctor_name": i[4],
                "patient_age":i[5],
                "patient_allergy":i[6]
            }
            p_data.append(data)
        return JsonResponse(p_data, safe=False)
    #新建病人
    if request.method =="POST":
        request.ContentType = "application/x-www-form-urlencoded";
        received_main_data = json.loads(request.body)
        print(received_main_data)
        #添加信息表
        PatientInfo.objects.create(
        doctor_id=received_main_data["doc_id"],
        patient_name=received_main_data["name"],
        patient_sex=received_main_data["sex"],
        patient_age=received_main_data["age"],
        patient_born=received_main_data["born"],
        patient_nation=received_main_data["nation"],
        patient_address=received_main_data["address"],
        patient_job=received_main_data["job"],
        patient_allergy=received_main_data["allergy"],
        p_d_id=received_main_data["doc_id"])
        patient = PatientInfo.objects.filter(patient_name=received_main_data["name"]) \
            .values("patient_id")
        #patient = list(patient)
        print(patient[0]["patient_id"])
        patient_id = patient[0]["patient_id"]
        #添加病历表
        RecordInfo.objects.create(
            patient_id=patient_id,
            record_date=time.strftime('%Y-%m-%d',time.localtime(time.time())),
            r_p_id=patient_id
            )

        pat_info = RecordInfo.objects.filter \
            (r_p__p_d__doctor_id=received_main_data["doc_id"]).\
            values_list("r_p__patient_id",
            "r_p__patient_name", "r_p__patient_sex","record_date"
            ,"r_p__p_d__doctor_name","r_p__patient_age","r_p__patient_allergy")

        # print(pat_info[0][0])
        for i in pat_info:
            data = {
                "patient_id": i[0],
                "patient_name": i[1],
                "patient_sex": i[2],
                "patient_date": i[3],
                "doctor_name": i[4],
                "patient_age": i[5],
                "patient_allergy": i[6]
            }
            p_data.append(data)
        #print(received_main_data)

        return JsonResponse(p_data, safe=False)


def delete(request):
    if request.method == "GET":
        patient_id = request.GET.get('patient_id', default=0)
    patient = PatientInfo.objects.get(patient_id=patient_id)
   # patient.delete()
    record = RecordInfo.objects.get(patient_id=patient_id)
    # model = ModelINfo.objects.get(record.record_id)
    # model.delete()
    patient.delete()
    record.delete()
    return JsonResponse('deletedOK', safe=False)


def record(request):
    p_data = []
    if request.method == "GET":
        patient_id = request.GET.get('patient_id', default=0)
        pat_info = RecordInfo.objects.filter \
            (patient_id=patient_id).values_list("r_p__patient_id",
                "r_p__patient_name", "r_p__patient_sex", "record_date"
                 , "r_p__p_d__doctor_name", "r_p__patient_age",
                    "r_p__patient_allergy")

        for i in pat_info:
            data = {
                "patient_id": i[0],
                "patient_name": i[1],
                "patient_sex": i[2],
                "patient_date": i[3],
                "doctor_name": i[4],
                "patient_age": i[5],
                "patient_allergy": i[6]
            }
            p_data.append(data)


    return JsonResponse(p_data,safe=False)
