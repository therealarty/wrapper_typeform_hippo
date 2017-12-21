def mail_quest(quest,answ,question):

    id=[t[0] for t in quest if t[2]==question][0]

    dreemer=DreemerDreemeridentity.objects.filter()
    dreemer_info=list(dreemer.values(
    'dreemer','email'))
    dreemer_info_DF=pd.DataFrame(dreemer_info,columns=['dreemer','email'])

    no_email=[t for t in answ if '@' not in t[1]]
    token_no_mail=list(set([t[3] for t in no_email]))

    email=[t for t in answ if '@' in t[1]]

    for i in range(len(token_no_mail)):
        rep=[t for t in answ if t[3]==token_no_mail[i]]
        mail=[t[6] for t in rep if t[0]==id][0].lower()
        uuid=None
        if len(dreemer_info_DF[dreemer_info_DF['email']==mail])>0:
                uuid=dreemer_info_DF[dreemer_info_DF['email']==mail].iloc[0]['dreemer']
        email+=[[t[0],mail,uuid,t[3],t[4],t[5],t[6]] for t in rep]
        
    return(email)


    

def update_database_quest (quest_list,QuestionDjango):
    
    for i in range(len(quest_list)):
        if i % 100 == 0:
            print(i,'/',len(quest_list))
        quest=quest_list[i]
        QuestionDjango.objects.create(id=quest[1],question_text=quest[2],possible_answer=quest[3],type=quest[4])
        
    return("It's done !")



def update_database_answ (answ_list,AnswerDjango):
    
    
    token_already_uploaded=list(set([t['token'] for t in list(AnswerDjango.objects.all().values('usertoken'))]))
    to_update=[t for t in answ_list if t[3]  not in token_already_uploaded]
    len_tablesql=AnswerDjango.objects.count()
    
    for i in range(len(to_update)):
        if i % 100 == 0:
            print(i,'/',len(to_update))
        answer=to_update[i]
        AnswerDjango.objects.create(id=i+len_tablesql,userid=answer[2],email=answer[1],usertoken=answer[3],questionid=answer[0],date=answer[4],answer=answer[5],answer_text=answer[6])
        
    return("It's done !")



