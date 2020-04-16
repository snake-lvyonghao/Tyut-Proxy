from django.db import models


# Create your models here.
class Student(models.Model):
    Sid = models.IntegerField(unique=True)
    Spassword = models.IntegerField()

    def __toString__(self):
        result = {"id": self.Sid, "password": self.Spassword}
        return result

    @classmethod
    def createStudent(cls, Sid, Spassword):
        stu = cls(
            Sid=Sid,
            Spassword=Spassword,
        )
        return stu

class PersonalInformation(models.Model):
    ClassId = models.ForeignKey("Student", to_field="Sid", on_delete=models.CASCADE) # 学号
    Class = models.CharField(max_length=15)  # 班级
    Coct = models.CharField(max_length=15)  # 已修课程学分
    Gpa = models.CharField(max_length=15)    # GPA
    GpaSort = models.CharField(max_length=15) # GPA专业排名
    WeightSort = models.CharField(max_length=15) # 加权班级排名
    AverageCredit = models.CharField(max_length=15) # 平均成绩
    AverageCreditSort = models.CharField(max_length=15) # 平均成绩专业排名
    FailingCredits = models.CharField(max_length=15) # 尚不及格学分
    Name = models.CharField(max_length=15) # 姓名
    TotalCreditsRequired = models.CharField(max_length=15) # 要求总学分
    ComInPraCre = models.CharField(max_length=15)    # 已修自主实践学分
    GpaSortClass = models.CharField(max_length=15) # GPA班级排名
    WeightCredit = models.CharField(max_length=15) # 加权学分成绩
    WeightCreditSort = models.CharField(max_length=15) # 加权专业排名
    AverageSortClass = models.CharField(max_length=15) # 平均成绩班级排名
    FailedCredits = models.CharField(max_length=15) # 曾不及格学分

    def __toString__(self):
        result = {'ClassId': self.ClassId.Sid,'Class':self.Class,'Coct':self.Coct,
                  'Gpa':self.Gpa,'GpaSort':self.GpaSort,'WeightSort':self.WeightSort,'AverageCredit':self.AverageCredit,
                  'AverageCreditSort':self.AverageCreditSort,'FailingCredits':self.FailingCredits,'Name':self.Name,'TotalCreditsRequired':self.TotalCreditsRequired,'ComInPraCre':self.ComInPraCre,
                  'GpaSortClass':self.GpaSortClass,'WeightCredit':self.WeightCredit,'WeightCreditSort':self.WeightCreditSort,
                  'AverageSortClass':self.AverageSortClass,'FailedCredits':self.FailedCredits}
        return result

class Kccj(models.Model):
    Kid = models.ForeignKey("Student", to_field="Sid", on_delete=models.CASCADE) # 学号
    ClassId = models.CharField(max_length=15)
    ClassName = models.CharField(max_length=50)
    GPA = models.CharField(max_length=15)
    ClassAttribute = models.CharField(max_length=15)
    TestTime = models.CharField(max_length=15)
    Credit = models.CharField(max_length=15)

    def __toString__(self):
        result = {'Kid':self.Kid.Sid,'ClassId':self.ClassId,'ClassName':self.ClassName,'GPA':self.GPA,
                  'ClassAttribute':self.ClassAttribute,'TestTime':self.TestTime,'Credit':self.Credit}
        return result

class Kcb(models.Model):
    Kid = models.ForeignKey("Student", to_field="Sid", on_delete=models.CASCADE) # 学号
    KcbMessage = models.TextField()

    def __toString__(self):
        result = {'Kid':self.Kid.Sid,'KcbMessage':self.KcbMessage}
        return result