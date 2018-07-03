
# coding: utf-8
import json
from io import open
import io
import utils
import sys

language = "ar"

DATA_FOLDER = "data/"
OUTPUT_FOLDER = "output/"

synsetStatistics = json.load(open(DATA_FOLDER+"SynsetStatistics.json", "r"))

submissions = json.load(open(DATA_FOLDER+"Submission.json", "r"))

synsetCameoToSubmission = {}

wordIdToSubmissionId = {}

#Find users who provided the coding for this language
language_coders_ids = [x["id"] for x in json.load(open(DATA_FOLDER+"UserInfo.json", "r")) if x["language"] == language]

# # print ("Number of coders : ", str(len(language_coders_ids)))

language_submissions = [x for x in submissions if x["userId"] in language_coders_ids]

# # print ("Total Submission (all)", str(len(submissions)))
# print ("Total Submissions (", language, ")", str(len(language_submissions)))

language_submissions_ids = [x["id"] for x in language_submissions]



feedbacksOnSynsetWord = [x for x in json.load(open(DATA_FOLDER+"FeedbackOnSynsetWord.json","r"))
                         if x["submissionId"] in language_submissions_ids]

count = 0

for feedback in feedbacksOnSynsetWord:
    if "verdict" not in feedback:
        count += 1

# print (len(feedbacksOnSynsetWord), count)

# print (len(feedbacksOnSynsetWord))

synsetWordToEntry = {x["id"]: x["idSynsetEntry"] for x in json.load(open(DATA_FOLDER +"SynsetWord.json","r"))
                     if x["languageCode"] == language}

synsetToSubmission = {}

for feedback in feedbacksOnSynsetWord:
    if feedback["idWord"] not in synsetWordToEntry:
        # print ("Word Not found")
        continue

    synsetId = synsetWordToEntry[feedback["idWord"]]

    if synsetId not in synsetToSubmission:
        synsetToSubmission[synsetId] = []
    if feedback["submissionId"] not in synsetToSubmission[synsetId]:
        synsetToSubmission[synsetId].append(feedback["submissionId"])

## print synsetToSubmission

synsetCameoToSubmission = {}

submissionToCameo = {}

submissionToCameoID = {x["id"]: x["cameoId"] for x in language_submissions}

for synsetId in synsetToSubmission:
    if str(synsetId) not in synsetCameoToSubmission:
        synsetCameoToSubmission[str(synsetId)] = {}

    submissions = synsetToSubmission[synsetId]

    for submission in submissions:

        cameoId = submissionToCameoID[submission]

        if str(cameoId) not in synsetCameoToSubmission[str(synsetId)]:
            synsetCameoToSubmission[str(synsetId)][str(cameoId)] = []
        synsetCameoToSubmission[str(synsetId)][str(cameoId)].append(submission)

## print synsetCameoToSubmission
#sys.exit(0)
# for submission in submissions:
#     if submission["userId"] in language_coders_ids:
#         if str(submission["wordId"]) not in wordIdToSubmissionId:
#             wordIdToSubmissionId[str(submission["wordId"])] = {}
#         if str(submission["cameoId"]) not in wordIdToSubmissionId[str(submission["wordId"])]:
#             wordIdToSubmissionId[str(submission["wordId"])][str(submission["cameoId"])] = []
#         wordIdToSubmissionId[str(submission["wordId"])][str(submission["cameoId"])].append(submission["id"])
#
# # print len(wordIdToSubmissionId)

#x = input()

#synsetCameoToSubmission = json.load(open(OUTPUT_FOLDER+"SynsetCameoToSubmission.json","r"))

# synsetEntries = json.load(open(DATA_FOLDER+"SynsetEntry.json", "r"))
#
# synsetEntryToWordID = {str(x["id"]): str(x["idWord"]) for x in synsetEntries}
#
# # print len(synsetEntryToWordID)

#x = input()
# synsetCameoToSubmissionCopy = {}
#
# issue_count = 0
# for synsetId in synsetCameoToSubmission:
#     wordId = synsetEntryToWordID[synsetId]
#     synsetCameoToSubmissionCopy[synsetId] = {}
#     if wordId not in wordIdToSubmissionId:
#         # print "Word ID: ", wordId
#         continue
#     cameoToSubmission = wordIdToSubmissionId[wordId]
#
#     for cameoId in synsetCameoToSubmission:
#         if cameoId in cameoToSubmission:
#             synsetCameoToSubmissionCopy[synsetId][cameoId] = cameoToSubmission[cameoId]
#         else:
#             synsetCameoToSubmissionCopy[synsetId][cameoId] = []
#             issue_count += 1
#             ## print cameoId
# # print "issue count " + str(issue_count)
#
#
# synsetCameoToSubmission = synsetCameoToSubmissionCopy

wordFeedbacks = json.load(open(DATA_FOLDER+"FeedbackOnSynsetWord.json", "r"))

synsetWords = json.load(open(DATA_FOLDER+"SynsetWord.json", encoding='UTF-8'),  "r")

synsetWords = [x for x in synsetWords if x["languageCode"] == language]

idToSynsetWordMap = {x["id"]: x for x in synsetWords}

count = 0

# print (len(wordFeedbacks))

filteredWordFeedbacks = []

for entry in wordFeedbacks:

    if entry['idWord'] in idToSynsetWordMap:
        entry["synset_id"] = idToSynsetWordMap[entry['idWord']]['idSynsetEntry']
        filteredWordFeedbacks.append(entry)
    else:
        count += 1


# print (len(filteredWordFeedbacks))



submissionToWordfeedbacks = {}

for entry in filteredWordFeedbacks:
    if entry['submissionId'] not in submissionToWordfeedbacks:
        submissionToWordfeedbacks[entry['submissionId']] = list()
    submissionToWordfeedbacks[entry['submissionId']].append(entry)


word_stat = {}

for synsetId in synsetCameoToSubmission:
    for cameoId in synsetCameoToSubmission[synsetId]:
        if cameoId not in word_stat:
            word_stat[cameoId]={}
        for submissionId in synsetCameoToSubmission[synsetId][cameoId]:
            if submissionId not in submissionToWordfeedbacks:
                continue

            for feedback in submissionToWordfeedbacks[submissionId]:
                if 'verdict' not in feedback:
                    continue
                if feedback['idWord'] not in word_stat[cameoId]:
                    word_stat[cameoId][feedback['idWord']] = {"correct": 0, "incorrect": 0, "ambiguous": 0}
                if feedback['verdict'] == "c":
                    word_stat[cameoId][feedback['idWord']]["correct"] += 1
                elif feedback['verdict'] == "ic":
                    word_stat[cameoId][feedback['idWord']]["incorrect"] += 1
                else:
                    word_stat[cameoId][feedback['idWord']]["ambiguous"] += 1

# # print word_stat
# sys.exit(0)
synsetEntryList = json.load(open(DATA_FOLDER+"SynsetEntry.json","r"))

synsetEntryToWordMap = {x["id"]: x["idWord"] for x in synsetEntryList}

wordList = json.load(open(DATA_FOLDER +"Word.json", "r"))

## print wordList

# # print (wordList[0]['text'])
wordIdToText ={}
for i in range(0, len(wordList)):
#    # print wordList[i]
    if 'text' in wordList[i]:
        wordIdToText[wordList[i]["id"]] = wordList[i]['text']
    else:
        # print ("ISSUE " +str(wordList[i]))
        print('')


cameo_word_translated = {}

for cameoId in word_stat:
    if cameoId not in cameo_word_translated:
        cameo_word_translated[cameoId] = {}
    for synsetWordId in word_stat[cameoId]:
        synsetWord = idToSynsetWordMap[synsetWordId]

        if word_stat[cameoId][synsetWordId]["correct"] >= word_stat[cameoId][synsetWordId]["incorrect"] + word_stat[cameoId][synsetWordId]["ambiguous"]:
            wordId = synsetEntryToWordMap[synsetWord["idSynsetEntry"]]
            wordEN = wordIdToText[wordId]
            if wordEN not in cameo_word_translated[cameoId]:
                cameo_word_translated[cameoId][wordEN] = set()
            cameo_word_translated[cameoId][wordEN].add(synsetWord['word'])

# # print (cameo_word_translated)

cameoEntryList = json.load(open(DATA_FOLDER+"CameoEntry.json", "r"))

codeToCameoId = {x['code']: x['id'] for x in cameoEntryList}

cameoRulesList = json.load(open(DATA_FOLDER+"CameoRule.json","r", encoding='UTF-8'))

cameoRuleToCameoCodeWord = {x["id"]:(x["cameoCode"], x["word"]) for x in cameoRulesList}
count = 0

listCameoIDs = []
for key in codeToCameoId:
     listCameoIDs.append(codeToCameoId[key])

## print sorted(listCameoIDs)
listCameoIDs = []
for key in cameo_word_translated:
    listCameoIDs.append(key)
## print sorted(listCameoIDs)

# print cameo_word_translated

outputFile = open(OUTPUT_FOLDER+"Cameo_"+language+"_v0.0.1.txt", "w+", encoding="UTF-8")

language_submissions_ids_str = [str(x) for x in language_submissions_ids]

for x in cameoRulesList:
    if x['source'] != 'CAMEO2' and x['source'] in language_submissions_ids_str:
        cameoId = str(codeToCameoId[x['cameoCode']])
        if cameoId in cameo_word_translated:
            translatedWords = cameo_word_translated[cameoId]
            if x['word'] in translatedWords:
                outputFile.write('- ' +x['ruleText']+'['+x['cameoCode']+'] #'+ ', '.join(translatedWords[x["word"]])+'\n')
            else:
                outputFile.write('- ' + x['ruleText'] + '[' + x['cameoCode'] + '] #' + "NTA "+x['word']+"\n")
            count += 1
# print (count)

cameo_translated_rule = [x for x in json.load(open(DATA_FOLDER+"CameoTranslatedRule.json", "r")) if x['languageCode'] == language]

# print (len(cameo_translated_rule))

count = 0
for tRule in cameo_translated_rule:
    cameoCode, word = cameoRuleToCameoCodeWord[tRule["ruleID"]]
    cameoId = str(codeToCameoId[cameoCode])
    if cameoId in cameo_word_translated:
        translatedWords = cameo_word_translated[cameoId]
        if word in translatedWords:
            outputFile.write(
                '- ' + tRule['text'] + '[' + cameoCode + '] #' + ', '.join(translatedWords[word]) + '\n')
        else:
            outputFile.write('- ' + tRule['text'] + '[' + cameoCode + '] #' + "NTA " + word + "\n")
        count += 1


outputFile.close()

#=======================================
import re
import json
from pprint import pprint


def get_verb_and_code(line):
    matcher = regex.search(line)
    if matcher != None:
        verb = matcher.group(0).strip().split(" ")[0]

        code = matcher.group(1)
        if code != None:
            code = code.replace("[", "").replace("]", "")

        return verb.strip(), code
    return None, None




cameo_file = open("CAMEO.2.0.txt","r")
verbs_map = {}
current_lead_verb = ""
regex = re.compile("[a-zA-Z ]+(\[[-|[0-9]*\])?")
for line in cameo_file:
    line = line.lower()
    if line.strip() == "":
        continue

    if line.strip().startswith("---"):
        verb, code = get_verb_and_code(line)
        current_lead_verb = verb
        verbs_map[current_lead_verb]={"code": code, "related_verbs": {}}


    elif line.startswith("-") and current_lead_verb != "":

        current_lead_verb  = ""
    elif current_lead_verb != "":
        verb, code = get_verb_and_code(line)
        if verb != None:
            verbs_map[current_lead_verb]["related_verbs"][verb] = {'code': code}
        else:
            # print "NOT Inserting"
            print('\n')



# print (len(verbs_map))

verbs_db = [x for x in json.load(open(DATA_FOLDER +"Word.json","r"))]

# print (len(verbs_db))

v_map = {}

for v in verbs_db:
    if 'text' in v:
        v_map[v['text']] = v['id']

# print (v_map['develop'])
count = 0;
for verb in verbs_map:
    if verb.lower() in v_map:
        verbs_map[verb]["id"] = v_map[verb.lower()]
    else:
        # print verb
        count += 1
    for rverb in verbs_map[verb]['related_verbs']:

        if rverb.lower() in v_map:
            ## print rverb
            ## print verbs_map[verb]['related_verbs'][rverb]
            verbs_map[verb]['related_verbs'][rverb]["id"] = v_map[rverb.lower()]
        else:
            # print "+", rverb
            count += 1
# print (count)
# pprint(verbs_map)


word_cameo_rules_map = {}

for x in cameoRulesList:
    if x["source"] != "CAMEO2" and x["source"] in language_submissions_ids_str:
        if x['word'] not in word_cameo_rules_map:
            word_cameo_rules_map[x['word']] = {}

        cameo_rules_map = word_cameo_rules_map.get(x['word'])

        if x['cameoCode'] not in cameo_rules_map:
            cameo_rules_map[x['cameoCode']] = list()

        cameo_rules_map[x['cameoCode']].append(x['ruleText'])

for x in cameo_translated_rule:
    cameoCode, word = cameoRuleToCameoCodeWord[x["ruleID"]]

    if word not in word_cameo_rules_map:
        word_cameo_rules_map[word] = {}
    cameo_rules_map = word_cameo_rules_map.get(word)

    if cameoCode not in cameo_rules_map:
        cameo_rules_map[cameoCode] = list()
    cameo_rules_map[cameoCode].append(x['text'])

cameo_es_dictionary = {}

for lead_verb in verbs_map:
    cameo_rules_map = word_cameo_rules_map.get(lead_verb)


    if cameo_rules_map != None:
        for cameo_code in cameo_rules_map:
            cameoId = str(codeToCameoId[cameo_code])
            if cameoId in cameo_word_translated:
                translatedWords = cameo_word_translated[cameoId]
                if lead_verb in translatedWords:
                    if 'translation' not in verbs_map[lead_verb]:
                        verbs_map[lead_verb]['translation'] = []
                    for word in translatedWords[lead_verb]:
                        if len(word.strip()) > 0:
                            verbs_map[lead_verb]['translation'].append(word.strip().replace(" ","+"))
                if "translated_rule" not in verbs_map[lead_verb]:
                    verbs_map[lead_verb]['translated_rule'] = []
                for rule in cameo_rules_map[cameo_code]:
                    verbs_map[lead_verb]['translated_rule'].append({"cameoCode": cameo_code, "rule": rule})

    for related_verb in verbs_map[lead_verb]['related_verbs']:
        cameo_rules_map = word_cameo_rules_map.get(related_verb)

        if cameo_rules_map != None:
            for cameo_code in cameo_rules_map:
                cameoId = str(codeToCameoId[cameo_code])
                if cameoId in cameo_word_translated:
                    translatedWords = cameo_word_translated[cameoId]
                    if related_verb in translatedWords:
                        if 'translation' not in verbs_map[lead_verb]['related_verbs'][related_verb]:
                            verbs_map[lead_verb]['related_verbs'][related_verb]['translation'] = []
                        for word in translatedWords[related_verb]:
                            if len(word.strip()) > 0:
                                verbs_map[lead_verb]['related_verbs'][related_verb]['translation'].append(word.strip().replace(" ","+"))
                    if "translated_rule" not in verbs_map[lead_verb]['related_verbs'][related_verb]:
                        verbs_map[lead_verb]['related_verbs'][related_verb]['translated_rule'] = []
                    for rule in cameo_rules_map[cameo_code]:
                        verbs_map[lead_verb]['related_verbs'][related_verb]['translated_rule'].append({"cameoCode": cameo_code, "rule": rule})


#json.dump(verbs_map, open("cameo_dict.json","w+"), ensure_ascii=False)
with io.open("testJson.json",'w',encoding="utf-8") as outfile:
    outfile.write(unicode(json.dumps(verbs_map, ensure_ascii=False)))


###### KJ ####

cameo_file = open("CAMEO.2.0.txt","r")

cameo_es_file = io.open(OUTPUT_FOLDER+"CAMEO."+language+".0.1.txt","w+", encoding="UTF-8")


current_lead_verb = ""
regex = re.compile("[a-zA-Z ]+(\[[-|[0-9]*\])?")
lead_translations = set()
all_translations = {}

default_code_map = {}

for line in cameo_file:
    line = line.lower()
    if line.strip() == "":
        continue

    if line.strip().startswith("---"):
        verb, code = get_verb_and_code(line)
        current_lead_verb = verb
        lead_translations.clear()
        all_translations.clear()

        if 'translation' in verbs_map[current_lead_verb]:

            for tword in verbs_map[current_lead_verb]['translation']:
                lead_translations.add(tword)
                if tword not in all_translations:
                    all_translations[tword] = set()
                all_translations[tword].add(current_lead_verb)


    elif line.startswith("-") and current_lead_verb != "":
        translated_lead_verb = None
        if len(lead_translations) > 0:
            translated_lead_verb = lead_translations.pop()
            lead_translations.add(translated_lead_verb)
        elif len(all_translations) > 0:
            translated_lead_verb = all_translations.keys()[0]
        if translated_lead_verb is not None:
            code = default_code_map.get(translated_lead_verb)
            translated_lead_verb = translated_lead_verb.split('_')[0]
            if code is None:
                cameo_es_file.write("--- "+translated_lead_verb+" [---] ---\n")
            else:
                cameo_es_file.write("--- " + translated_lead_verb + " ["+code+"] ---\n")

            for trans_verb in all_translations:
                clean_verb = trans_verb.split('_')[0]
                clean_verb = utils.master_reconstruct_input(clean_verb , 0)
                
                code = default_code_map.get(trans_verb)
                code_str = ""
                if code is not None:
                    code_str = " ["+code+"]"
                str = "%-20s %-10s %s" % (clean_verb, code_str, "# "+",".join(all_translations[trans_verb])+"\n")
                # str = "%-20s %-10s" % (clean_verb, code_str +"\n")
                
                # print('----> VERB : {} | CODE : {} '.format(clean_verb.encode('utf-8').strip() , code_str.encode('utf-8').strip()))
                # print('----> TRANSLATIONS : \n{}\n******\n'.format("\n".join(all_translations[trans_verb])))
                cameo_es_file.write(str)

            ## print THE RULES
            trans_rules = set()
            if "translated_rule" in verbs_map[current_lead_verb]:
                for rule in verbs_map[current_lead_verb]["translated_rule"]:
                    if rule['cameoCode']+" "+rule['rule'] not in trans_rules:
                        associated_verbs = set()
                        if 'translation' in verbs_map[current_lead_verb]:
                            for verb in verbs_map[current_lead_verb]['translation']:
                                associated_verbs.add(verb)
                            rule['rule'] = utils.master_reconstruct_input(rule['rule'], 1)
                            trans_rules.add(rule['cameoCode']+" "+rule['rule'])
                            str = "%s %-s %s" % ("- "+rule['rule'], "  ["+rule['cameoCode']+"]", "# "+ ",".join(associated_verbs)+"\n")
                            # str = "%s %-s" % ("+ "+rule['rule'], "  ["+rule['cameoCode']+"]"+ "\n")
                            
                            # print('{}'.format(rule['rule'].encode('utf-8').strip() ))
                            # print('{}'.format(str(rule['rule']).strip() ))
                            
                            
                            cameo_es_file.write(str)
                            for verb_t in verbs_map[current_lead_verb]['translation']:
                                default_code_map[verb_t] = rule['cameoCode']
            for rel_word in verbs_map[current_lead_verb]['related_verbs']:

                if "translated_rule" in verbs_map[current_lead_verb]['related_verbs'][rel_word]:
                    for rule in verbs_map[current_lead_verb]['related_verbs'][rel_word]["translated_rule"]:
                        if rule['cameoCode'] + " " + rule['rule'] not in trans_rules:
                            associated_verbs = set()
                            if 'translation' in verbs_map[current_lead_verb]['related_verbs'][rel_word]:
                                for verb in verbs_map[current_lead_verb]['related_verbs'][rel_word]['translation']:
                                    associated_verbs.add(verb)
                                rule['rule'] = utils.master_reconstruct_input(rule['rule'], 1)
                                trans_rules.add(rule['cameoCode'] + " " + rule['rule'])
                                str = "%s %-s %s" % ("- " + rule['rule'], "  [" + rule['cameoCode'] + "]",
                                                          "# " + ",".join(associated_verbs) + "\n")
                                # str = "%s %-s " % ("+ " + rule['rule'], "  [" + rule['cameoCode'] + "]" + "\n")
                                # print('{}'.format(rule['rule'].encode('utf-8').strip() ))
                                # print('{}'.format(str(rule['rule']).strip() ))
                                
                                cameo_es_file.write(str)
                                for verb_t in verbs_map[current_lead_verb]['related_verbs'][rel_word]['translation']:
                                    if verb_t not in default_code_map:
                                        default_code_map[verb_t] = rule['cameoCode']


        cameo_es_file.write(unicode("\n\n"))
        current_lead_verb  = ""
    elif current_lead_verb != "":
        verb, code = get_verb_and_code(line)
        if verb != None and verb in verbs_map[current_lead_verb]['related_verbs']:
            if 'translation' in verbs_map[current_lead_verb]['related_verbs'][verb]:
                for tword in verbs_map[current_lead_verb]['related_verbs'][verb]['translation']:
                    if tword not in all_translations:
                        all_translations[tword] = set()
                    all_translations[tword].add(verb)
        else:
            # print ("NOT Inserting")
            print('\n')

cameo_es_file.close()

























