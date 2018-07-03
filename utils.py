# coding: utf-8
import requests
import pyarabic.araby as araby # for processing arabic 
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

acceptable_formats = ['*',"*()", "*{}"  , "*({})", '*()' , '*()()', '*({})', '*()', '*({})()', '*(){}', '*{()}' , '*(())', '*({()})']
special_formats = ['()', '()()' , '', '*(}})' , '*}}', '{}' , '*(' , '*({({()' , '*(}()(}']
wrong_skip = ['* نزع سلاح) جهود)' , ' * عن تقرير مصير) بيان)', '* عن تقرير مصير) بيان)' , '* ((مساعدات انسانية} (من أجل})']

#store things for later
special = []
to_be_replaced = []
error =[]

def check_and_reconstruct_rule(rule): 
    rule = " ".join(rule.split()) # to remove all white spaces and duplicate ones 
    if rule == '' :
        return 'ERROR'
    
    rule_encod =str(rule.encode('ascii', errors='ignore')).replace(" ", "")

    if rule_encod in acceptable_formats: #verb is already correct(rare cases)- apply regex stright
        return rule
    elif rule_encod in special_formats:
        return 'SPECIAL'
    else : 
        if rule_encod == '*({{)':
            t = rule.find('{')
            rule = rule[:t] + rule[t+1: -1] + '})'
            rule_encod =str(rule.encode('ascii', errors='ignore') ).replace(" ", "")
        elif rule_encod  =='*((':
            t =  rule.find('(')
            rule = rule[:t] + rule[t+1:] + ')'
            rule_encod =str(rule.encode('ascii', errors='ignore')).replace(" ", "")
        elif rule_encod  =='*{{':
            t =  rule.find('{')
            rule = rule[:t] + rule[t+1:] + '}'
            rule_encod =str(rule.encode('ascii', errors='ignore')).replace(" ", "")
        elif rule_encod =='*{((}' : 
            t = rule.find('(')
            rule = rule[:t] + rule[t+1: -1] + ')}'
            rule_encod =str(rule.encode('ascii', errors='ignore')).replace(" ", "") 
        elif rule_encod == '*{){)': 
            t = rule.find('{')
            rule = rule[:t] + '(' + rule[t+1: -1] + '}'
            rule_encod =str(rule.encode('ascii', errors='ignore') ).replace(" ", "") 
            
        
        if rule_encod not in acceptable_formats :
#             print('ERR | {} | {}'.format(rule, rule_encod))
            return 'ERROR'
        else :
#             print('FIX | {} | {}'.format(rule, rule_encod))
            return rule
    
    return rule

def rule(i):
   
    if not i: 
       return ''
    elif i.strip()[0] != '*' : # Wrong delete 
        print('NEED MANUAL FIX :{}'.format(i)) # delete those need to mananually fix
        special_formats.append(i)
        return i
    elif re.search('[a-zA-Z]', i) : 
        to_be_replaced.append(i)
        return i
    elif i in wrong_skip : 
        print('SKP | {}'.format(i))
        return i
    else : 
        if '$' in i or '+' in i or '^' in i or '/' in i or '|' in i :
            i = ''.join([c for c in i if c not in set(['$', '+', '^', '/' , '|'])])
        rule_fixed = check_and_reconstruct_rule(i.strip())
        if rule_fixed == i :
            return i
        elif rule_fixed == 'SPECIAL':
            print('NEED MANUAL FIX :{}'.format(i))
            special.append(i)
            return i
        elif rule_fixed == 'ERROR' :
            print('ERR :{}'.format(i))
            error.append(i)
            return i
        else :  # fixed by now
            return rule_fixed
            
        
# Get data from udpipe
def udpipe(string) :
    # Prepping String 
    words  = re.findall(u'[\u0600-\u06FF]+', string) #getting arabic characters 
    data = ' '.join(words)
    
    pipe_base_url = 'http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger' 
    attributes = {} 
    attributes['model'] = 'arabic-ud-2.0-170801'
    attributes['data'] = data

    data = requests.get(pipe_base_url , params = attributes)
    result = data.json()['result'].split('\n')
    udpipe_results = [re.findall(u'[\u0600-\u06FF]+', i) for i in result] # cleaning 
    udpipe_results = [i for i in udpipe_results if i !=[]]
    
    return udpipe_results

def udpipe_reconstruct(original_text) : 
    udpipe_results = udpipe(original_text)
    for i in range(1, len(udpipe_results)):
        if len(udpipe_results[i]) == 1 : # composite verbs get the next two words
            original_text =original_text.replace(udpipe_results[i][0] , '{} {}'.format(udpipe_results[i+1][1],udpipe_results[i+2][1]))
        else :
            original_text =original_text.replace(udpipe_results[i][0] , udpipe_results[i][1])
    original_text = araby.strip_tashkeel(original_text)
    return original_text


def master_reconstruct_input(text_input , input_type): 
    # type 0: none-rule just do just do udpipe_reconstruction
    # type 1 : fix the rule + do udpipe_reconstruction
    if input_type == 0:
        print('Processing Verb : [{}]'.format(text_input.strip()))
        return udpipe_reconstruct(text_input)
    else : 
        print('Processing RULE : [{}]'.format(text_input.strip()))
        return udpipe_reconstruct(rule(text_input.strip() ))
    