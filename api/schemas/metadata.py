import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required
from graphene import ObjectType
from api.models import *
from api.schemas.validation import Validation
from django.db.models import Q
import datetime
from graphql import GraphQLError
            

class HobbyCategoryType(DjangoObjectType):
    class Meta:
        model = HobbyCategory

class HobbyType(DjangoObjectType):
    class Meta:
        model = Hobby

class RaasiType(DjangoObjectType):
    class Meta:
        model = Raasi

class EducationCategoryType(DjangoObjectType):
    class Meta:
        model = EducationCategory

class OccupationCategoryType(DjangoObjectType):
    class Meta:
        model = OccupationCategory

class StarType(DjangoObjectType):
    class Meta:
        model = Star

class MotherTongueType(DjangoObjectType):
    class Meta:
        model = MotherTongue

class ReligionType(DjangoObjectType):
    class Meta:
        model = Religion

class CasteType(DjangoObjectType):
    class Meta:
        model = Caste
                        
class SubCasteType(DjangoObjectType):
    class Meta:
        model = SubCaste

class MembershipType(DjangoObjectType):
    class Meta:
        model = Membership
        fields = ("features", "membership", "offer_percent", "membership_price")

class MetaQuery(graphene.ObjectType):

    hobby_category = graphene.List(HobbyCategoryType)
    def resolve_hobby_category(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = HobbyCategory.objects.all()
        return qs  

    hobby = graphene.List(HobbyType)
    def resolve_hobby(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Hobby.objects.all()
        return qs  

    raasi = graphene.List(RaasiType)
    def resolve_raasi(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Raasi.objects.all()
        return qs          
        
    occupation_category = graphene.List(OccupationCategoryType)
    def resolve_occupation_category(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = OccupationCategory.objects.all()
        return qs          
        
    education_category = graphene.List(EducationCategoryType)
    def resolve_education_category(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = EducationCategory.objects.all()
        return qs          
        
    star = graphene.List(StarType)
    def resolve_star(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Star.objects.all()
        return qs          
        
    mother_tongue = graphene.List(MotherTongueType)
    def resolve_mother_tongue(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = MotherTongue.objects.all()
        return qs          

    religion = graphene.List(ReligionType)
    def resolve_religion(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Religion.objects.all()
        return qs          

    caste = graphene.List(CasteType)
    def resolve_caste(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Caste.objects.all()
        return qs          

    sub_caste = graphene.List(SubCasteType)
    def resolve_sub_caste(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = SubCaste.objects.all()
        return qs          

    membership = graphene.List(MembershipType)
    def resolve_membership(self, info, **kwargs):
        Validation.check_staff_role(info.context.user)
        qs = Membership.objects.all()
        return qs     
