from selenium import webdriver
from budget.models import Project,Category
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
import pytest
from mixer.backend.django import mixer
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pdb
from fixtures import create_project,delete_objects
import random
    



@pytest.mark.django_db
def test_projects_are_empty(setup,live_server):

    delete_objects()
    setup.get(live_server.url)
    time.sleep(1)
    
    alert = setup.find_element_by_class_name('noproject-wrapper')
    assert(
        alert.find_element_by_tag_name('h3').text == 'Sorry, you don\'t have any projects, yet.'
    )

    time.sleep(2)
        
    

    setup.find_element_by_tag_name('a').click()

    time.sleep(2)
        
    assert(setup.current_url == live_server.url + reverse('add'))

    time.sleep(2)
     
    setup.find_element_by_id('id_name').send_keys('ashique')
    setup.find_element_by_id('id_budget').send_keys(5000)
    setup.find_element_by_id('categoryInput').send_keys('sales', Keys.ENTER)

    time.sleep(2)

    #detail_url = setup.current_url + reverse('detail',args=['/ashique/'])
    setup.find_element_by_tag_name('button').click()

    time.sleep(2)
    assert(setup.current_url == live_server.url + reverse('detail',args=['ashique']))
    #time.sleep(2)

    setup.find_element_by_tag_name('button').click()

    setup.find_element_by_id('title').send_keys('first_transaction')
    setup.find_element_by_id('amount').send_keys(100)
    dropdown= Select(setup.find_element_by_name('category'))
    dropdown.select_by_visible_text('sales')
    
    time.sleep(2)

    setup.find_element_by_id('addbtn').click()

    time.sleep(2)
        
    

@pytest.mark.django_db
def test_project_not_empty(setup,live_server):
    delete_objects()
    
    project1 = create_project('varun ',500,'skills')
    category_name_list = []
    project_name_list = []
    for _ in range(5):
        project_object = mixer.blend('budget.Project')
        project_name_list.append(project_object.name)
        category_object = mixer.blend('budget.Category',project=project_object)
        category_name_list.append(category_object.name)
   
    setup.get(live_server.url)
    # pdb.set_trace()
    time.sleep(2)

    #detail_page = reverse('detail',args=[project1.slug])[1:]
    
    #detail_url =  setup.current_url + reverse('detail',args=[project1.slug])[1:]
    setup.find_element_by_tag_name('a').click()

    time.sleep(2)

        
    assert(setup.current_url == live_server.url + reverse('detail',args=[project1.slug]))
    time.sleep(2)

    value = category_name_list[0]
    for _ in range(4):
        setup.find_element_by_tag_name('button').click()

        setup.find_element_by_id('title').send_keys('first_transaction')
        setup.find_element_by_id('amount').send_keys(random.randrange(20, 50))
        dropdown= Select(setup.find_element_by_name('category'))
        dropdown.select_by_visible_text(category_object.name)

        setup.find_element_by_id('addbtn').click()

    
    time.sleep(2)

    
    time.sleep(2)