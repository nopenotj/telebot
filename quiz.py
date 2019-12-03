import requests

link = "https://opentdb.com/api.php?amount=10"

def initialiseQnBank(link):
    response = requests.get(link)
    response.encoding = 'utf-8'
    results = response.json()
    qn = results['results'] 
    return qn

def next_qn(qb):

    data = qb.pop()
    data['category']
    data['difficulty']
    ans = data['correct_answer']
    incorrect  = data['incorrect_answers']
    qn = data['question']

    choices = []
    choices.append(ans)
    choices.extend(incorrect)
    
    dic = { 'qn' : qn , 'choices' : choices,'ans' :ans } 
    return dic

