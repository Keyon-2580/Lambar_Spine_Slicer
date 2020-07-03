from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os
import base64
import glob

from demo.models import DocterInfo, PatientInfo,RecordInfo,ModelInfo
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
import time
from django.shortcuts import render
import demo.test as test
import demo.segmentation as sg
from Original import STLGenerator
from test_002 import settings
from django.core import serializers

import demo.lasso as lasso



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
    record = RecordInfo.objects.get(patient_id=patient_id)

    patient.delete()
    record.delete()
    jsonresponse["code"] = 200
    return JsonResponse(jsonresponse, safe=False)

#查看病历
def record(request):
    p_data = []
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

        if  receive_file:
            dir = '/home/sxchongya/original_file'
            path = os.path.join(dir, patient_id + '/' )
            if not os.path.exists(path):
                os.mkdir(path)  # 新建文件夹
            destination = open(os.path.join(path, receive_file.name), 'wb+')
            #存储文件
            for chunk in receive_file.chunks():
                destination.write(chunk)
            destination.close()
            #存储文件路径
            record = RecordInfo.objects.get(patient_id=patient_id)
            record.record_slicer_file = '/home/sxchongya/original_file/'+ patient_id + '/' + receive_file.name
            record.save()

            jsonresponse["code"] = 200
            jsonresponse['data'] = os.path.join(dir, patient_id + '- ' + receive_file.name )
        else:
            jsonresponse["code"] = 185
    return JsonResponse(jsonresponse,safe=False)

#上传读取文件
def temporaryFile(request):
    jsonresponse = {"code": 0, "data": '', }
    if request.method == 'POST':
        receive_file = request.FILES.get('file', None)
        if receive_file:
            dir = '/home/sxchongya/original_file/temporary/'
            destination = open(os.path.join(dir, receive_file.name), 'wb+')
# 存储文件
            for chunk in receive_file.chunks():
                destination.write(chunk)
            destination.close()
# 转为png
            if format(os.path.splitext(receive_file.name)[1]) == '.gz':
                jsonresponse['data'] = receive_file.name.replace('.nii.gz', '')
                test.nii_to_image(receive_file.name,0,0)
            elif format(os.path.splitext(receive_file.name)[1]) == '.nrrd':
                jsonresponse['data'] = receive_file.name.replace('.seg.nrrd', '')
                test.nrrd_to_image(receive_file.name)
            elif format(os.path.splitext(receive_file.name)[1]) == '.zip':
                jsonresponse['data'] = receive_file.name.replace('.zip', '')
                test.dicomtoimg(receive_file.name)
            jsonresponse["code"] = 200
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
            jsonresponse['code'] = 200
        except:
            jsonresponse['code'] = 175
    return JsonResponse(jsonresponse,safe=False)

#读取CT
@csrf_exempt
def read_img(request):
    data = json.loads(request.body)
    patient_id = data['patient_id']
    code = data['code']
    file_name = data['file_name']

    try:
        img_num = {
            'x':0,
            'y':0,
            'z':0
        }
        if(code == 111):
            paths_x = glob.glob(os.path.join(settings.MEDIA_ROOT+'/temporary/'+file_name+'x/', '*.png'))
            paths_y = glob.glob(os.path.join(settings.MEDIA_ROOT+'/temporary/'+file_name+'y/', '*.png'))
            paths_z = glob.glob(os.path.join('/home/sxchongya/original_files/temporary/'+file_name+'z/', '*.png'))
            print('sss')
        elif(code == 222):
            paths_x = glob.glob(os.path.join(settings.MEDIA_ROOT+patient_id+'/sliced_file'+'x/', '*.png'))
            paths_y = glob.glob(os.path.join(settings.MEDIA_ROOT+patient_id+'/sliced_file'+'y/', '*.png'))
            paths_z = glob.glob(os.path.join(settings.MEDIA_ROOT+patient_id+'/sliced_file'+'z/', '*.png'))
        img_num['x'] = len(paths_x)
        img_num['y'] = len(paths_y)
        img_num['z'] = len(paths_z)

        return JsonResponse(img_num, safe = False)
    except Exception as e :
        print(e)
        return HttpResponse(str(e))


#分割
def segmentation(request):
    jsonresponse = {'code':0}
    print(request.body)
    data = json.loads(request.body)

    patient_id = data['patient_id']
    nii_path = RecordInfo.objects.filter(patient_id=patient_id).values_list('record_slicer_file')
    if(nii_path == ''):
        jsonresponse['code'] = 300
        return JsonResponse(jsonresponse,safe=False)
    print((nii_path[0][0]))
    path = nii_path[0][0]
    try:
        sliced_path = settings.MEDIA_ROOT + patient_id+'/'
        if not os.path.exists(sliced_path):
                os.mkdir(sliced_path)
        sg.segmentation(path,sliced_path)

        sliced_path = sliced_path + 'sliced_file.nii.gz'
        test.nii_to_image('sliced_file.nii.gz',1,patient_id)#保存png
        print('-------------------------------------------------------')
        #存储分割后得路径
        record = RecordInfo.objects.get(patient_id=patient_id)
        record.record_sliced_files = sliced_path
        record.save()
        print(sliced_path)

        jsonresponse['code'] = 200
    except Exception as e:
        jsonresponse['code'] = 200
        print(e)
    return JsonResponse(jsonresponse,safe=False)

    return
#显示模型
def models(request):
    patient_id = request.GET.get('patient_id')
    model_file = ModelInfo.objects.filter(model__patient_id=patient_id).values_list('model_file')
    sliced_file = RecordInfo.objects.filter(patient_id=patient_id).values_list('record_sliced_files')
    path = sliced_file[0][0]
    print(path)
    path_0 = settings.MEDIA_ROOT
    #模型文件
    #STLGenerator.GenSTL(path,path_0 + patient_id + '/')
    STLGenerator.GenSTL('/home/sxchongya/original_file/temporary/spine1_0.nii.gz', path_0 + patient_id + '/')
    print('`````````````````````````')
    data = {
        'patient_id':patient_id,
        'aaa': '/original_files/' + patient_id + '/'+ 'SJG.stl',
        'bbb': '/original_files/' + patient_id + '/'+ 'ZJP.stl',
        'ccc': '/original_files/' + patient_id + '/'+ 'YMN.stl',
        'ddd': '/original_files/temporary/2 0.625MM.nrrd'
    }
    return render(request,"../templates/test.html",{"aaa":json.dumps(data['aaa']),
                                                   "bbb":json.dumps(data['bbb']),
                                                   "ccc":json.dumps(data['ccc']),
                                                   "ddd": json.dumps(data['ddd']),
                                                   "patient_id":json.dumps(data['patient_id'])})

@csrf_exempt
def taosuo(request):
    patient_id = request.GET.get('patient_id')
    number = request.GET.get('number')
    print(patient_id)
    path = '/original_files/'+patient_id+'/sliced_filez/'+number+'.png'

    return render(request,"../templates/456.html",{'aaa':json.dumps(path),
                                                   'bbb':json.dumps(patient_id),
                                                   'ccc':json.dumps(number)})

@csrf_exempt
def dealed(request):
    data = request.body
    data = json.loads(data)
    text = data['text']
    patient_id = data['patient_id']
    number = data['number']
    path = "/home/sxchongya/original_files/temporary/foo.svg"
    fo = open(path, "w")
    fo.write(text)
    fo.close()
    record = RecordInfo.objects.filter(patient_id=patient_id).values_list('record_sliced_files')
    niipath = record[0][0]
    lasso.lasso(path,niipath , number, niipath)
    return JsonResponse('1',safe=False)


def regist(request):
    jsonresponse = {'code':0}
    data = request.body
    data = json.loads(data)
    print(data)
    try:
        DocterInfo.objects.create(
            doctor_account=data['account'],
            doctor_name = data['name'],
            doctor_sex = data['sex'],
            doctor_pwd = data['pwd'],
            doctor_department = data['department'],
            doctor_job = data['job'],
            doctor_tel = data['tel'],
        )
        jsonresponse['code'] = 200
        print('--------------------------------')
    except Exception as e:
        print(e)
    return JsonResponse(jsonresponse,safe=False)