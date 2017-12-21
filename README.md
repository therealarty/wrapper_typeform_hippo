# wrapper_typeform_hippo

TypeForm API wrapper for questions and answers written in python. You'll get datas in two lists (format of lists is explained at the end of this doc) <br />
There are also functions to update a SQL database with the questions list and answers list (For Rythm only).

## Installing
```
pip install git+git://github.com/hippo26/wrapper_typeform_hippo.git
```

## Requirements

-requests <br />
-time <br />
-pandas <br />
-uuid <br />


## Usage
### Authorized Access
```
import requests
import pandas as pd
import time
import uuid as uuid2

import wrapper_typeform.rythm_database as db

from wrapper_typeform.typeform_wrapper import Client


client = Client('{YOUR_TOKEN}')

To get the {YOUR_TOKEN} follow the documentation
 
https://developer.typeform.com/get-started/scopes/
```

Get questions and answers from your form {form_id} to lists quest and answ:
```
quest, answ=client.typeform_to_DF('{form_id}')
```

### For Rythm only

#### Email and UUID

Get the email and the uuid (if it exists) when it is asks in a specific question (question text: {question_text_email} ):
```
dreemer=DreemerDreemeridentity.objects.filter(email__iexact=list(set([t[1] for t in answ if t[1]!=None)))
    dreemer_info=list(dreemer.values(
    'dreemer','email'))
    dreemer_info_DF=pd.DataFrame(dreemer_info,columns=['dreemer','email'])

answ=db.mail_quest(dreemer_info_DF,quest,answ,'{question_text_email}')
```

#### Update the database

Be careful, to use the following functions, tables {QuestionDjango} and {AnswerDjango} must be already created (see below how to create them). <br />

Add the questions list to the table {QuestionDjango}  <br />

NB: you need to run this fonction just 1 time for each form
```
db.update_database_quest(quest,{QuestionDjango})
```

Add the answers list to the table {AnswerDjango} <br />
NB: run this function everytime you want to update the datas of the form
```
db.update_database_answ(answ,{AnswerDjango})
```

Create the tables {QuestionDjango} and {AnswerDjango} <br />
<br />
I. Create tables {_question_sql} and {_answer_sql} on postgreSQL <br />
<br />
  1) Open a terminal <br />
  2) Copy and paste: 
  ```
  env PGPASSWORD='{password_database}' psql -h analytics-db.rythm.co -U dreem
  ```
  3) Copy and paste: 
  ```
  create table {_question_sql} (id varchar(30) PRIMARY KEY,question_text text, possible_answer text, type text);
  ```
  4) Copy and paste: 
  ```
  create table {_answer_sql} (id integer PRIMARY KEY, email varchar(100),userid UUID, usertoken varchar(100),date integer,questionid varchar(30) references {_question_sql} ,answer integer, answer_text text);

  ```

II. Create tables {QuestionDjango} and {AnswerDjango} on Django <br />
<br />
1) Open models.py <br />
2) Copy and paste at the end of the doc: 
```
#Questions 
class {QuestionDjango}(models.Model):
    id=models.TextField(primary_key=True)
    #question we ask in the form
    question_text=models.TextField(blank=True, null=True)
    possible_answer=models.TextField(blank=True, null=True)
    type=models.TextField(blank=True, null=True)

    class Meta:
        managed=False
        db_table='{_question_sql}'

#Answers 
class {AnswerDjango}(models.Model):
    id=models.BigIntegerField(primary_key=True)
    userid=models.UUIDField(blank=True, null=True)
    email=models.CharField(max_length=254, blank=True, null=True)
    usertoken=models.CharField(max_length=100, blank=True, null=True)
    questionid=models.TextField(primary_key=True)
    date=models.BigIntegerField(blank=True, null=True)
    answer=models.IntegerField(blank=True, null=True)
    answer_text=models.TextField(blank=True, null=True)

    class Meta:
        managed=False
        db_table='{_answer_sql}'
```


## Format of lists you'll get from Typeform API
### Questions list {quest}

It's a list of list and each element of {quest} looks like:

```
[id_global_question, id_sub_question, question_text, possible_answer, type_of_question]
```

Let's take an exemple. <br />
<br />
Imagine that in your form, one is asked 'What is your favourite football player?' (this question's token is 'XvwSeCsz3GZZ' on Typeform API) and the multiple choices are: <br />
<br />
-Zinedine Zidane <br />
-Cristiano Ronaldo <br />
-Lionel Messi <br />
-Diego Mardonna <br />
-Pelé <br />
-Other <br />
<br />
In the list {quest} you'll get the following sublists: 

```
['XvwSeCsz3GZZ','XvwSeCsz3GZZ_0','What is your favourite football player?','Zinedine Zidane','multiple_choice_1_choice']

['XvwSeCsz3GZZ','XvwSeCsz3GZZ_1','What is your favourite football player?','Cristiano Ronaldo','multiple_choice_1_choice']

['XvwSeCsz3GZZ','XvwSeCsz3GZZ_2','What is your favourite football player?','Lionel Messi','multiple_choice_1_choice']

['XvwSeCsz3GZZ','XvwSeCsz3GZZ_3','What is your favourite football player?','Diego Mardonna','multiple_choice_1_choice']

['XvwSeCsz3GZZ','XvwSeCsz3GZZ_4','What is your favourite football player?','Pelé','multiple_choice_1_choice']

['XvwSeCsz3GZZ','XvwSeCsz3GZZ','What is your favourite football player?','autre_text','multiple_choice_1_choice']
 ```

Question types: <br />
'legal','date','yes_no','rating','number','opinion_scale','website','long_text','email','short_text','dropdown','multiple_choice_1_choice','multiple_choice_choices'] <br />
<br />
Rem: for types in ['website','long_text','email','short_text'], possible_answer=None <br />
<br />
Let's take an other exemple. You are asked 'How old are you?' (and your answer must be included in [18,120] and question token is 'XvwSeCsz3GZZ'), then you'll find in the list {quest}: <br />
```
['XvwSeCsz3GZZ','XvwSeCsz3GZZ','How old are you?','[18,120]','number']
```

### Answers list {answ}
It's a list of list and each element of {answ} looks like:
```
[id_sub_question, email, uuid, usertoken, date, answer, answer_text]
```
Rem: <br />
  -date in utc timestamp <br />
  <br />
  -if you did not answer to this id_global_question: <br />
      answer=None <br />
      answer_text=None <br />
          <br />
    <br />
  -for question_type in ['legal','yes_no','dropdown','multiple_choice_1_choice','multiple_choice_choices'] except autre_text: <br />
    - answer=1 if you chose this possible_answer else 0 <br />
    - answer_text=None <br />
    <br />
  -for question_type in ['rating','number','opinion_scale']: <br />
    - answer=your_answer <br />
    - answer_text=None  <br />
   <br />
  -for question_type in ['date','website','long_text','email','short_text'] or if autre_text : <br />
    - answer=1 <br />
    - answer_text=your_answer



