from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os
import base64
import glob

from demo.models import DocterInfo, PatientInfo,RecordInfo
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
import time
from django.core import serializers





#登录
def login(request):
    if request.method == "GET":
        username = request.GET.get("username", default=0)
        pwd = request.GET.get("pwd", default=0)
    doctor = DocterInfo.objects.filter(doctor_account = username, doctor_pwd = pwd)
    if doctor.exists():
        data = {
            "code": "200",
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

#刷新病人信息
@csrf_exempt
def refresh(request):
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



#删除病人
def delete(request):
    jsonresponse = {"code":0}
    if request.method == "GET":
        patient_id = request.GET.get('patient_id', default=0)
    patient = PatientInfo.objects.get(patient_id=patient_id)
   # patient.delete()
    record = RecordInfo.objects.get(patient_id=patient_id)

    patient.delete()
    record.delete()
    jsonresponse["code"] = 200
    return JsonResponse(jsonresponse, safe=False)

#查看病历
def record(request):
    #header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE');
    p_data = []
    print("hhh")
    if request.method == "GET":
        patient_id = request.GET.get('patient_id', default=0)
        pat_info = RecordInfo.objects.filter \
            (patient_id=patient_id).values_list("r_p__patient_id",
                "r_p__patient_name", "r_p__patient_sex", "record_date"
                 , "r_p__p_d__doctor_name", "r_p__patient_age",
                    "r_p__patient_allergy","record_slicer_file"
                ,"record_condition", "record_opinion")


        for i in pat_info:
            str = i[7]
            if str:
                str = str.replace('F:\\大三下\\Lumbar\\','')

            data = {
                "patient_id": i[0],
                "patient_name": i[1],
                "patient_sex": i[2],
                "patient_date": i[3],
                "doctor_name": i[4],
                "patient_age": i[5],
                "patient_allergy": i[6],
                "record_slicer_file":str,
                "record_condition":i[8],
                "record_opinion":i[9]
            }
            print(str)
            p_data.append(data)

    return JsonResponse(p_data,safe=False)

#添加病人
@csrf_exempt
def add_patient(request):
    jsonresponse = {"code":0, "data":{}}
    #code = 0
    if request.method =="POST":
        request.ContentType = "application/x-www-form-urlencoded";
        received_main_data = json.loads(request.body)
        print(received_main_data)
        #添加信息表
        try:
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
            # patient = list(patient)
            print(patient[0]["patient_id"])
            patient_id = patient[0]["patient_id"]
            # 添加病历表
            RecordInfo.objects.create(
                patient_id=patient_id,
                record_date=time.strftime('%Y-%m-%d', time.localtime(time.time())),
                r_p_id=patient_id
            )
            jsonresponse["code"] = 200
            return JsonResponse(jsonresponse, safe=False)
        except :
            jsonresponse["code"] = 500

            return JsonResponse(jsonresponse, safe=False)


#传输文件
def postFile(request):
    jsonresponse = {"code":0,"data":''}
    if request.method == 'POST':
        receive_file = request.FILES.get('file', None)
        patient_id = request.POST.get('patient_id',None)
        print(patient_id)

        if  receive_file:
            dir = 'F:\\大三下\\Lumbar'
            print(os.path)
            destination = open(os.path.join(dir, patient_id + '- ' + receive_file.name ), 'wb+')
            #存储文件
            for chunk in receive_file.chunks():
                destination.write(chunk)
            destination.close()
            #存储文件路径
            record = RecordInfo.objects.get(patient_id=patient_id)
            record.record_slicer_file = 'F:\\大三下\\Lumbar\\'+ patient_id + '- ' + receive_file.name
            record.save()

            jsonresponse["code"] = 200
            jsonresponse['data'] = os.path.join(dir, patient_id + '- ' + receive_file.name )

        else:
            jsonresponse["code"] = 185


    return JsonResponse(jsonresponse,safe=False)

#提交病历
@csrf_exempt
def opinion(request):
    jsonresponse = {'code': 0}
    if request.method == "POST":
        try:
            request.ContentType = "application/x-www-form-urlencoded";
            received_record = json.loads(request.body)
            print(received_record['patient_id'])
            record = RecordInfo.objects.get(patient_id=received_record['patient_id'])

            record.record_slicer_file = received_record['record_slicer_file']
            record.record_opinion = received_record['record_opinion']
            record.record_condition = received_record['record_condition']
            record.save()
            print("sss")
            jsonresponse['code'] = 200

        except:
            jsonresponse['code'] = 175


    return JsonResponse(jsonresponse,safe=False)

#读取CT
@csrf_exempt
def read_img(request):
    try:
        img = []
        data = json.loads(request.body)
        data = data['filename']
        dir = "F:\\大三下\\Lumbar\\"
        imgpath = os.path.join(dir, format(data))
        print(imgpath)
        WSI_MASK_PATH = 'F:\\大三下\\Lumbar'  # 存放图片的文件夹路径
        paths = glob.glob(os.path.join('F:\\大三下\\Lumbar\\media\\images', '*.png'))
        paths.sort()
        for path in paths:
            with open(path,'rb') as f:
                img_data = f.read()
            img_data = base64.b64encode(img_data)
            img.append(img_data )
            img.append(',++')

        return HttpResponse(img, content_type="image/png")
    except Exception as e :
        print(e)
        return HttpResponse(str(e))


def post(request):
    jsonresponse = {"code": 0, "data": ''}
    if request.method == 'POST':
        receive_file = request.FILES.get('file', None)
        patient_id = 555
        print(patient_id)

        if receive_file:
            dir = 'F:\\大三下\\Lumbar'
            print(os.path)
            destination = open(os.path.join(dir, patient_id + '- ' + receive_file.name), 'wb+')
            # 存储文件
            for chunk in receive_file.chunks():
                destination.write(chunk)
            destination.close()
            # 存储文件路径
            record = RecordInfo.objects.get(patient_id=patient_id)
            record.record_slicer_file = 'F:\\大三下\\Lumbar\\' + patient_id + '- ' + receive_file.name
            record.save()

            jsonresponse["code"] = 200
            jsonresponse['data'] = os.path.join(dir, patient_id + '- ' + receive_file.name)

        else:
            jsonresponse["code"] = 185

    return JsonResponse(jsonresponse, safe=False)
