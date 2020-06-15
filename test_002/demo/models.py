# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class DocterInfo(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_account = models.CharField(max_length=255, blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_sex = models.CharField(max_length=255, blank=True, null=True)
    doctor_pwd = models.CharField(max_length=255, blank=True, null=True)
    doctor_department = models.CharField(max_length=255, blank=True, null=True)
    doctor_job = models.CharField(max_length=255, blank=True, null=True)
    doctor_tel = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'docter_info'


class ModelInfo(models.Model):
    record_id = models.IntegerField()
    model_file = models.CharField(max_length=255, blank=True, null=True)
    model = models.OneToOneField(to="RecordInfo",on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'model_info'


class PatientInfo(models.Model):
    patient_id = models.AutoField(primary_key=True)
    doctor_id = models.CharField(max_length=255, blank=True, null=True)
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    patient_sex = models.CharField(max_length=255, blank=True, null=True)
    patient_age = models.CharField(max_length=255, blank=True, null=True)
    patient_born = models.CharField(max_length=255, blank=True, null=True)
    patient_nation = models.CharField(max_length=255, blank=True, null=True)
    patient_address = models.CharField(max_length=255, blank=True, null=True)
    patient_job = models.CharField(max_length=255, blank=True, null=True)
    patient_allergy = models.CharField(max_length=255, blank=True, null=True)
    p_d = models.ForeignKey(to="DocterInfo", to_field="doctor_id",on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'patient_info'


class RecordInfo(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient_id = models.CharField(max_length=255, blank=True, null=True)
    record_date = models.DateField(blank=True, null=True)
    record_slicer_file = models.CharField(max_length=255, blank=True, null=True)
    record_condition = models.CharField(max_length=255, blank=True, null=True)
    record_opinion = models.CharField(max_length=255, blank=True, null=True)
    r_p = models.OneToOneField(to="PatientInfo",on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'record_info'