import pandas as pd

def mail_quest(dreemer_info_DF,quest,answ,question):

    id=[t[0] for t in quest if t[2]==question]
    
    if len(id)==0:
        return('This question is not in the form')
    else:
        id=id[0]
    
    no_email=[t for t in answ if '@' not in str(t[1])]
    token_no_mail=list(set([t[3] for t in no_email]))

    email=[t for t in answ if '@' in str(t[1])]

    for i in range(len(token_no_mail)):
        rep=[t for t in answ if t[3]==token_no_mail[i]]
        mail=[t[6] for t in rep if t[0]==id][0]
        if mail != None:
            mail=mail.lower()
        uuid=None
        if len(dreemer_info_DF[dreemer_info_DF['email']==mail])>0:
                uuid=dreemer_info_DF[dreemer_info_DF['email']==mail].iloc[0]['dreemer']
        email+=[[t[0],mail,uuid,t[3],t[4],t[5],t[6]] for t in rep]
    
    
    return(email)

def uuid(answ, dreemer_info_DF):
    
    email_base=dreemer_info_DF.email.unique()
    email_liste=list(set([t[1] for t in answ if (pd.isnull(t[2]) & pd.notnull(t[1]))]))
    email_liste=[t for t in email_liste if t in email_base]
    answ_with_uuid=[t for t in answ if t[1] not in email_liste]
    
    for i in range(len(email_liste)):
        uuid=dreemer_info_DF[dreemer_info_DF['email']==email_liste[i]].iloc[0]['dreemer']
        answ_with_uuid+=[[t[0],t[1],uuid,t[3],t[4],t[5],t[6]] for t in answ if t[1]==email_liste[i]]
    
    return(answ_with_uuid)
    

def update_database_quest (quest_list,QuestionDjango):
    
    for i in range(len(quest_list)):
        if i % 100 == 0:
            print(i,'/',len(quest_list))
        quest=quest_list[i]
        QuestionDjango.objects.create(id=quest[1],question_text=quest[2],possible_answer=quest[3],type=quest[4])
    
    print(len(quest_list),'/',len(quest_list))
    return("It's done !")



def update_database_answ (answ_list,AnswerDjango):
    
    
    token_already_uploaded=list(set([t['usertoken'] for t in list(AnswerDjango.objects.all().values('usertoken'))]))
    to_update=[t for t in answ_list if t[3]  not in token_already_uploaded]
    len_tablesql=AnswerDjango.objects.count()
    
    for i in range(len(to_update)):
        if i % 100 == 0:
            print(i,'/',len(to_update))
        answer=to_update[i]
        AnswerDjango.objects.create(id=i+len_tablesql,userid=answer[2],email=answer[1],usertoken=answer[3],questionid=answer[0],date=answer[4],answer=answer[5],answer_text=answer[6])
    
    print(len(to_update),'/',len(to_update))
    return("It's done !")



def to_dataframe(quest,answ):
    token=list(set([t[3] for t in answ]))
    rep_all=[]
    for j in range(len(quest)):
        id_quest=quest[j][1]
        if (quest[j][4] in ['short_text','long_text','date','website','email'] or quest[j][3] in ['autre_text']):
            temp=[t[6] for t in answ_fr if t[0]==id_quest]
        else:
            temp=[t[5] for t in answ_fr if t[0]==id_quest]

        rep_all.append(temp)

    rep_all.append([t[1] for t in answ if t[0]==quest])
    rep_all.append([t[2] for t in answ if t[0]==quest])
    rep_DF=pd.DataFrame(rep_all,columns=token)
    rep_DF['id_quest']=[t[1] for t in quest]+['email','uuid']
    rep_DF['possible_answ']=[t[2] for t in quest]+['email','uuid']
    rep_DF['question']=[t[3] for t in quest]+['email','uuid']
    rep_DF.set_index(['id_quest','possible_answ','question'],inplace=True)
    rep_DF=rep_DF.T
    return(rep_DF)
    
    
