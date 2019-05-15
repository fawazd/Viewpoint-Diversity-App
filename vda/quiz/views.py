from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, get_user_model, logout,)
from django.views.generic import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import re
from bs4 import BeautifulSoup
import json
import datetime
from django.contrib import messages
import requests
import random


from .models import *

######### Homepage #########
class HomeView(View):
    def get(self, request):
        return render(request,'quiz/index.html')

    def post(self, request):
        current_username = request.POST.get('username')
        ## Checks if username input is empty and redirects to the index
        ## If it is empty, "is_invalid" is passed to the template to be included in the username input tag,
        ## which will outline the input area with red to alert the user of empty input
        if not current_username:
            invalid = "is-invalid"
            return render(request,'quiz/index.html', {'invalid': invalid})
        ## If username input is not empty and if the user exists, the user is then logged in
        else:
            ## Creates a Score object for the user with the default starting information and the username provided if they do not already exist
            if not Score.objects.filter(username=current_username):
                starting_page = Page.objects.get(page_id=1)
                starting_score = 0
                starting_step = 1
                new_user_score = Score.objects.create(username=current_username, current_step=starting_step, current_score=starting_score, page=starting_page, nextqp=0)
                new_user_score.save()
            if User.objects.filter(username=current_username):
                user = User.objects.get(username=current_username)
                login(request, user)
            ## If the user does not exist, creates new User object with the information provided and logs in the new user
            else:
                new_user = User.objects.create_user(current_username, current_username + '@email.com', 'password')
                login(request, new_user)

            ## Once verification and or user creation is complete, the user is logged in and redirected to the progress page
            return HttpResponseRedirect(reverse('quiz:progress'))

######### Quiz #########
class QuizView(View):
    def get(self, request, page_id):
        ## Initializing empty string variables that require conditions to be met in order to be assigned with appropriate values
        ## This is done so that we can pass on empty variables rather than have multiple returns for different conditions, to reduce code duplication
        question = answers = button = quote = nextstate = prevstate = question_type = ""

        page = Page.objects.get(page_id=page_id)
        ## Retrieving any existing quote(s) for the current page
        if Quote.objects.filter(page_id=page_id):
            quote = Quote.objects.get(page=page)
        ## Retrieves any existing question, and its answers based on question type for the current page
        if Question.objects.filter(page=page):
            question = Question.objects.get(page=page)
            question_type = question.type
            if question.type == "multichoice":
                answers = MultichoiceAnswer.objects.filter(question=question.question_id).order_by('?')
            else:
                answers = CheckboxAnswer.objects.filter(question=question.question_id)
        ## If no questions exist for the current page, a button action will, which is then used to retrieve the button
        if ButtonAction.objects.filter(page=page):
            button = Button.objects.get(button_id=(ButtonAction.objects.get(page=page)).button.button_id)


        ## Setting the next and previous page id values
        next = page.next_page
        prev = page.prev_page

        user = Score.objects.get(username=request.user.username)
        ## Computing if previous or next button should be clickable
        ## Next button is disabled if the user is on a page that is higher than their farther reached page stored in their Score instance
        if user.page.page_id < page.next_page:
            nextstate = "disabled"
        ## Previous button is disabled if they're on the first page of the quiz
        if page_id == 1:
            prevstate = "disabled"

        ## Any existing title and image for the current page is retrieved and passed on to the quiz template
        title = Title.objects.filter(page_id=page_id)
        image = Image.objects.filter(page_id=page_id)
        return render(request, 'quiz/quiz.html',
                      {'page': page, 'question': question, "question_type": question_type,"answers": answers, 'name': user,
                       'title': title, 'image':image, 'button': button, 'quote': quote, 'next': next, 'prev': prev, 'nextstate': nextstate, 'prevstate': prevstate})

    def post(self, request):
        ## Checks which submit button has been clicked and runs the designated code
        if 'next_page' in request.POST:
            current_user = Score.objects.get(username=request.user.username)
            next_page = int(request.POST.get('next_page'))
            ## Only updates user's score if they have not already attempted the question
            ## Checks their last answered question against the current page
            if current_user.nextqp < int(request.POST.get('current')):
                ## Updates their last answered to the latest answered question page id
                current_user.nextqp = current_user.page.page_id
                current_user.page = Page.objects.get(page_id=next_page)
                current_user.current_step = current_user.page.step
                ## Score computation for checbox answers
                if request.POST.getlist('answers[]'):
                    ## Sets total for 5 checkboxes where 2 answers will be incorrect
                    correct = len(request.POST.getlist('incorrect[]'))
                    total = len(request.POST.getlist('total[]'))
                    ## For every answer checked if true add 1 to correct and if false minus 1 off correct
                    for a in request.POST.getlist('answers[]'):
                        if a == "True":
                            correct += 1
                        else:
                            correct -= 1
                    ## Add to users score the page total divided by total and then multiplied by the amount
                    ## user got correct
                    current_user.current_score += ((current_user.page.page_score / total) * correct)
                ## If question was multichoice just add page's score
                else:
                    current_user.current_score += Page.objects.get(page_id=next_page).page_score
                ## Updates the current step for the user based on the what step the current page is assigned to
                current_user.save()
            ## Sets the page_id to appropriate next_page id retrieved from the template
            page_id = next_page
        elif 'previous' in request.POST:
            ## Sets the page_id to the previous page_id
            page_id = int(request.POST.get('previous'))
        else:
            ## Sets the page_id to the next page_id
            page_id = int(request.POST.get('next'))
        return HttpResponseRedirect(reverse('quiz:quiz', kwargs={'page_id':page_id}))

######### Progress #########
class ProgressView(View):
    def get(self, request):
        user = Score.objects.get(username=request.user.username)
        page = Page.objects.get(page_id=user.page.page_id)
        ## Creates a temporary dictionary with 0 values to represent each of the five steps
        progress = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}
        total_scores = 0
        overall_score = 0
        ## Using the farthest reached page by the user, retrieves the farthest step
        for i in range(1, page.step+1):
            ## Filters all the pages for each of the steps and retrieves the count of pages
            pages = Page.objects.filter(step=i).order_by("pk")
            page_count = len(pages)

            ## Checks every page in the step and saves the users current page
            for p in range(page_count):
                if pages[p].page_id == user.page.page_id:
                    current_page = p
            ## Checks if the current step being calculated is less than the farthest reached step
            ## If so, automatically assigns 100 percent completion for that step
            ## Does the same if the users current page is the same as the total count pages in the step, meaning they have reached the end of that step
            if i < page.step or current_page == page_count:
                progress[i] = 100
                ## Score calculation in this instance is simple as the user has completed the step:
                ## Add up all the points available in all the pages in the current step, use that in the final calculation below to calculate overall score
                for p in pages:
                    total_scores += p.page_score
            ## If the user is currently on a step that they have not completed,
            ## Uses page count of the step and the index of the current page in relation to the page count of the step to calculate the percentage completed
            else:
                progress[i] = int((100 / page_count) * current_page)
                ## Calculating score for incomplete step:
                ## Only get all available points from every page up to the page the user is currently on, use that in the final calculation below to calculate overall score
                for p in pages:
                    if p.page_id <= user.page.page_id:
                        total_scores += p.page_score
        ## With all the available scores that we added up previously, for both complete and incomplete steps
        ## Calculate the overall percentage by using that and the user's score that we keep track of in the Score object
        if total_scores != 0:
            overall_score = int((100/total_scores) * user.current_score)
        ## Directs the user to the progress page, along with all the information we want the user to see
        return render(request, 'quiz/progress.html', {'progress': progress, 'username': request.user.username, 'user': user, 'user_score': overall_score})

    def post(self, request):
        ## When the form is submitted, get the user's current page and redirects them to the quiz, passing along the page id
        user = Score.objects.get(username=request.user.username)
        page = Page.objects.get(page_id=user.page.page_id, step=user.current_step)
        return HttpResponseRedirect(reverse('quiz:quiz', kwargs={'page_id':page.page_id}))