from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return self.title
    
class About(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    image1 = models.ImageField(upload_to='pictures', null=True)
    image2 = models.ImageField(upload_to='pictures', null=True)

    def __str__(self):
        return self.title


class FeatureCause(models.Model):
    title = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    goal = models.IntegerField(null=True)
    raised = models.IntegerField(null=True)
    image = models.ImageField(upload_to='pictures', null=True)



    def __str__(self):
        return self.title
    
    def percentage(self):
        perc = (self.raised/self.goal)*100
        return round(perc)


class WhatWeDo(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    icon = models.ImageField(upload_to='pictures', null=True)



    def __str__(self):
        return self.title

class Trustee(models.Model):
    name = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='pictures', null=True)


    def __str__(self):
        return self.name

class Testimonie(models.Model):
    name = models.CharField(max_length=200, null=True)
    profession = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='pictures', null=True)


    def __str__(self):
        return self.name


class Outlet(models.Model):
    name = models.CharField(max_length=200, null=True)
    service = models.CharField(max_length=200, null=True)
    overview = models.TextField(null=True)
    image = models.ImageField(upload_to='pictures', null=True)    


    def __str__(self):
        return self.name

class GeneralInformation(models.Model):
    address = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=200, null=True)
    aboutHead = models.CharField(max_length=200, null=True)
    causeHead = models.CharField(max_length=200, null=True)
    whatHead = models.CharField(max_length=200, null=True)
    donateHead = models.CharField(max_length=200, null=True)
    donateContent = models.TextField(null=True)
    teamHead = models.CharField(max_length=200, null=True)
    testimonieHead = models.CharField(max_length=200, null=True)
    contactHead = models.CharField(max_length=200, null=True)
    contactContent = models.TextField(null=True)
    pageHeaderImage = models.ImageField(upload_to='pictures', null=True)
    logo = models.ImageField(upload_to='pictures', null=True)
    logo2 = models.ImageField(upload_to='pictures', null=True)
    

    def __str__(self):
        return self.tel
    

class Gallery(models.Model):
    image = models.ImageField(upload_to='pictures', null=True)
    caption = models.CharField(max_length=200, null=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag


class Picture(models.Model):
    image = models.ImageField(upload_to='pictures', null=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag


class Paragraph(models.Model):
    content = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag


class GalleryVideo(models.Model):
    video = models.FileField(upload_to='videos', null=True)
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag