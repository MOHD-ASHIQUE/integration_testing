import pytest
from mixer.backend.django import mixer
from budget.models import Project,Category

@pytest.mark.django_db
def delete_objects():
    Project.objects.all().delete()
    
    
@pytest.mark.django_db
def create_project(user_name,user_budget,category_name):
    project1 = mixer.blend('budget.Project',name=user_name,budget=user_budget)
    category1 = mixer.blend('budget.Category',project=project1,name=category_name)
    return project1