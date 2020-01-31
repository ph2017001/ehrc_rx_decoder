#!/usr/bin/env python
# coding: utf-8

# In[105]:


import traceback
import pandas as pd
import re
from text2digits import text2digits
import pprint


# In[2]:



def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False


# In[5]:


test_cases = { 'presc_text_list' : [ 
    'Oxazepam-10mg-1-0-1-2-days-After food.', 'Disulfiram, 500, morning-afternoon-night, 5, Days , After Food.',
    'Naltrexone, fifty mg, 1-0-0, 5, weeks, After Food.','Paracetamol/500/morning-evening/5/days/ Good sleep',
    'Risperidone, 0.5mg, 0-0-1, 6, days, After food ','Olanzapine, 5 mg, 2 Weeks, 1-0-0, Can be taken with or without food',
    'Haloperidol, 5 mg/mL, 1-1-1, 1, months','Chlorpromazine 10mg; 1-1-1-1; 15 days',
    'Injection Thiamine/Multivitamin 100mg/ml, 6 Months, once in 15 days. \n Chlorpromazine 10mg; 1-1-1-1; 15 days'
]}


# In[6]:


separator_list = ['-',',','/']


# In[7]:


dosage_patterns =['1-1-1-1','1-0-0-1','1-1-0-1','1-0-1-1']


# In[8]:


def extractMedicineName(pres_text, sep_symbol_arr):
    try:
        medicine_name = ""
        if "injection" not in pres_text.lower():
            for i in range(0,len(pres_text)):
                if pres_text[i] not in sep_symbol_arr and pres_text[i] !=" ":
                    medicine_name += pres_text[i]
                else:
                    break
        else:
            remaining_text = pres_text.lower().split("injection ")[1]
            print(remaining_text)
            medicine_name += "Injection "

#             min_sep_index = [remaining_text.find(k,0,remaining_text.find("mg")) for k in sep_symbol_arr]
#             print(min_sep_index)
            medicine_name += remaining_text[0: remaining_text.find(" ",0,remaining_text.find("mg"))]

    except Exception as e:
        print(e)
    return medicine_name.strip(), True


# In[9]:


def extractDosage(pres_text):
    
    if pres_text.find("mg/ml") != -1:
        drug_part = pres_text.split("mg/ml")[0]
        remaining_part = pres_text.split("mg/ml")[1]
        print(remaining_part, "  ** " , drug_part)
        return {'drug_part' : drug_part, 'remaining_part' : remaining_part}, True      
    elif pres_text.find("mg") != -1:
        drug_part = pres_text.split("mg")[0]
        remaining_part = pres_text.split("mg")[1]
        print(remaining_part, "  ** " , drug_part)
        {'drug_part' : drug_part, 'remaining_part' : remaining_part}
    else:
        print("No Dosage Found")
        return {'dosage':"_"}


# In[10]:


def tokenizePrescription(prescription_text_arr, medicine_map , num_lines = 1 ,accepted_suggestions_arr = []):
    
    #case 1 : All lines in the prescription have a corresponding accepted medince suggestion   
    if num_lines == len(accepted_suggestions_arr) and num_lines > 0:
        print("Case 1")
        
    #case 2 : Some lines (>=1) in the prescription have a corresponding accepted medince suggestion
    elif num_lines > len(accepted_suggestions) and len(accepted_suggestions_arr)!=0:
        print("Case 2")
    
    #case 3 : None of the lines (>=1) in the prescription have a corresponding accepted medince suggestion
    elif num_lines >=1 and len(accepted_suggestions_arr) == 0:
        print("Case 3")
        
    #case 4 : There is no prescription text
    else:
        print("Case 4")
        print("No prescription text present")  


# In[11]:


def splitPrescriptionLines(prescription_text):
    presc_text_arr = str(prescription_text).splitlines()
    presc_text_arr = [i.strip() for i in presc_text_arr]
    return presc_text_arr


# In[12]:


def generateTimingCombinations(timing_list):
    output = sum([list(map(list, combinations(timing_list, i))) for i in range(len(timing_list) + 1)], [])
    print(output)
    


# In[13]:


def findTimingWords(pres_text, timing_words):
   
    found = False
    
    time_check = []
    for j in timing_words:
        if j in pres_text:
            time_check.append(j)
            found = True
            
    return time_check, found


# In[34]:


def extractReplaceDrugName(pres_text, accepted_suggestion = [], replace_text = "xxxDrugNamexxx"):
    
    replaced_text = pres_text.lower()
    extracted_drug = accepted_suggestion
    found = False
    suggestion_matched = False
    
    if len(accepted_suggestion)!=0:
        for suggestion in accepted_suggestion:
            if suggestion.lower() in replaced_text and len(suggestion.strip()) !=0 and not(found):
                replaced_text = replaced_text.replace(suggestion.lower(),replace_text)
#                 print("replaced_text",replaced_text)
                extracted_drug = suggestion
                suggestion_matched = True
                found = True
    else:
        extracted_drug, foundDrug = extractMedicineName(pres_text, separator_list)
        if extracted_drug !="" and foundDrug:
            replaced_text = replaced_text.replace(extracted_drug.lower(),replace_text)
#             print("replaced_text",replaced_text)
            found = True
    
    if len(accepted_suggestion)!=0 and not(suggestion_matched): 
        extracted_drug, foundDrug = extractMedicineName(pres_text, separator_list)
        if extracted_drug !="" and foundDrug:
            replaced_text = replaced_text.replace(extracted_drug.lower(),replace_text)
#             print("replaced_text",replaced_text)
            found = True
            
    return replaced_text, extracted_drug, found


# In[15]:


def extractReplaceTimingWords(pres_text, timing_word_list, replace_text = "xxxTIMINGxxx"):
    
    timing_words, found_timing_words = findTimingWords(pres_text, timing_word_list)
    extracted_timing = ""
    final_str = pres_text
    
    if found_timing_words:
        first_time = timing_words[0]
        last_time = timing_words[-1]

        first_index = pres_text.index(first_time)
        last_end = pres_text.index(last_time)+len(last_time)-1

        final_str = pres_text[0:first_index] + replace_text + pres_text[last_end+1:]
        extracted_timing = pres_text[first_index:last_end+1]
    
    return final_str, extracted_timing, found_timing_words


# In[16]:


timing_codes = ['0-0-1', '0-1-0','0-1-1','1-0-0','1-0-1','1-1-0','1-1-1',
               '0-0-0-1', '0-0-1-0','0-0-1-1','0-1-0-0','0-1-1-0','0-1-1-1', '1-0-0-0',
               '1-0-0-1', '1-0-1-0','1-0-1-1','1-1-0-0','1-1-1-0','1-1-1-1']
timing_codes.reverse()
timing_words = ['morning', 'afternoon', 'evening','night']


# In[17]:


dosage_suffix =['mg/ml','mg / ml','mg /ml','mg/ ml','mg','ml','gm','drops','spoons','drop','spoon']
duration_suffix = ['years', 'year', "yrs." ,"yrs","yr", "monthly", "months", "month","mnth", "mth" ,"weeks", "week", "wks", "wk", "days", "day"]


# In[18]:


def extractReplaceTimingCode(pres_text, timing_codes, replace_text = "xxxTIMINGxxx"):
    
    final_str = pres_text
    found = False
    extracted_timing=''
       
    for i in timing_codes:
        first_pos = pres_text.find(i)
        if  first_pos != -1:
            final_str = pres_text[0:first_pos] + replace_text + pres_text[first_pos+len(i):]
            extracted_timing = i
            found = True
            break
    
    return final_str, extracted_timing, found  


# In[19]:


def extractReplaceDosage(pres_text, suffix_index, replace_text = "xxxDosageValuexxx"):
    
    found_dosage = False
    dosage_bound_text = pres_text[0:suffix_index].strip()
    final_text =""
    ptr = len(dosage_bound_text) - 1
    while ptr >=0 and (dosage_bound_text[ptr].isalpha() or dosage_bound_text[ptr].isnumeric() or dosage_bound_text[ptr]=='.'):
        final_text = dosage_bound_text[ptr:]
        found_dosage = True
        ptr-=1
        
    if found_dosage:
        pres_text = pres_text[0:ptr+1]+replace_text+ pres_text[ptr+1+len(final_text):]
        
    return pres_text, final_text, found_dosage


# In[20]:


def extractReplaceDosageSuffix(pres_text, dosage_suffix_arr, replace_text = "xxxDosageSuffxxx"):
    
    final_str = pres_text
    found = False
    extracted_suff=''
       
    for j in dosage_suffix_arr:
        first_pos = pres_text.find(j)
        if  first_pos != -1:
            #extractReplaceDosage(pres_text,first_pos)
            final_str = pres_text[0:first_pos] + replace_text + pres_text[first_pos+len(j):]
            extracted_suff = j
            found = True
            break
    #print('extractReplaceDosageSuffix', final_str, extracted_suff, found)
    return final_str, extracted_suff, found  
    


# In[21]:


def extractReplaceDurationSuffix(pres_text, duration_suffix_arr, replace_text = "xxxDurationSuffxxx"):
    
    final_str = pres_text
    found = False
    extracted_suff=''
       
    for j in duration_suffix_arr:
        first_pos = pres_text.lower().find(j.lower())
        if  first_pos != -1:
            #extractReplaceDosage(pres_text,first_pos)
            final_str = pres_text[0:first_pos] + replace_text + pres_text[first_pos+len(j):]
            extracted_suff = j
            found = True
            break
    #print('extractReplaceDosageSuffix', final_str, extracted_suff, found)
    return final_str, extracted_suff, found  


# In[22]:


def extractReplaceDuration(pres_text, suffix_index, replace_text = "xxxDurationValuexxx"):
    
    found_duration = False
    dosage_bound_text = pres_text[0:suffix_index].strip()
    final_text =""
    ptr = len(dosage_bound_text)-1


    while dosage_bound_text[ptr] in [" ", "/",",",";",".","-"]:
        ptr-=1
    
    ltr = ptr
    
    while ptr >=0 and (dosage_bound_text[ptr].isalpha() or dosage_bound_text[ptr].isnumeric() or dosage_bound_text[ptr]=='.'):
        final_text = dosage_bound_text[ptr:ltr+1]
        found_duration = True
        ptr-=1
        
    if found_duration:
        pres_text = pres_text[0:ptr+1]+replace_text+ pres_text[ptr+1+len(final_text):]
        
    return pres_text, final_text,found_duration


# In[23]:


def extractReplaceRemarks(pres_text, entity_frame, entity_index , replace_text = "xxxRemarksxxx"):
    
    max_entity_pos_index = max(entity_index)
    max_entity_tag = entity_frame[entity_index.index(max_entity_pos_index)]
    
    ptr = 0
    ltr = max_entity_pos_index+len(max_entity_tag)
    
    found_remarks = False
    remarks_text = pres_text[ltr:].strip()
       
    while ptr < len(remarks_text) and remarks_text[ptr] in [",","/",";","-"," "]:
        ptr+=1
        remarks_text = remarks_text[ptr:]    
    
    if len(remarks_text.strip()) > 0:
        found_remarks = True
        pres_text = pres_text[0:ltr]+replace_text
        
    return pres_text, remarks_text.strip(),found_remarks


# In[64]:


def updateEntityIndex(tagged_text, entity_arr):
    entity_pos = [tagged_text.find(e) for e in entity_arr]
    return entity_pos


# In[103]:


def guessDosageDurationValue(pres_text, entity_frame, entity_index , guess_type = "dosage" ,replace_text = "xxxDosageValuexxx"):
    try: 
        guessed_dosage = False

        if guess_type == "dosage":
            prev_entity = "xxxDrugNamexxx"
            current_entity_index = 1
            index_cnt = 2
        else:
            prev_entity = "xxxTIMINGxxx"
            current_entity_index = 4
            replace_text = "xxxDurationValuexxx"
            index_cnt = 5

        if entity_index[current_entity_index] == -1:
            #finding closes neighbors
            # Left Neighbor should be drug name or 0
            if pres_text.find(prev_entity) != -1:
                left_start = pres_text.find(prev_entity)+ len(prev_entity)
            #Right Neighbor should be found by walking till one reaches a found entity


            while entity_index[index_cnt] == -1:
                index_cnt+=1

            entity = entity_frame[index_cnt]  
            right_end = pres_text.find(entity)
            bound_text = pres_text[left_start:right_end]
            bound_text = bound_text.strip()
            #start removing separators from left and right

            ptr = 0
            while ptr<len(bound_text) and bound_text[ptr] in ["/",",",";","-"] and len(bound_text)>=0:
                ptr+=1
                if ptr<len(bound_text):
                    bound_text = bound_text[ptr:]
                elif ptr >= len(bound_text):
                    bound_text=""

            ptr = len(bound_text)-1

            while len(bound_text)>0 and ptr < len(bound_text) and bound_text[ptr] in ["/",",",";","-"]:
                if ptr<len(bound_text) and ptr!=0:
                    bound_text = bound_text[:ptr]
                    ptr-=1
                elif ptr==0:
                    bound_text=""
                    ptr-=1



            #double check if it is a dosage value or not
#             print("BOUND ", bound_text, "  len" , len(bound_text))

            if len(bound_text) >0 and is_number(bound_text):
                guessed_dosage = True
                pres_text = pres_text[0:pres_text.find(bound_text)] + replace_text + pres_text[right_end:]
                return pres_text, bound_text, guessed_dosage
            elif len(bound_text) >0:
                t2di = text2digits.Text2Digits()
                extracted_value = t2di.convert(bound_text).strip()

                if is_number(extracted_value):
                    guessed_dosage = True
                    pres_text = pres_text[0:pres_text.find(bound_text)] + replace_text + pres_text[right_end:]
                    return pres_text, bound_text, guessed_dosage
                else:
                    return pres_text, "Guessed Value May Not be a Dosage/Duration", False
        else:
            return pres_text, "No need to guess, it is already there.", False
    except Exception as ee:
        print(ee)
        track = traceback.format_exc()
        print(track)
    
    return pres_text, "Some exception occurred", False           
        


# In[26]:


def validateDosageValue(result_dict , ehrc_df):
    try:
        drugName = result_dict.get('medicine_name').lower()
        extracted_dosage_value = result_dict.get('dosage_value',"")
        
        if extracted_dosage_value !="":
            if not(is_number(extracted_dosage_value)):
                t2d = text2digits.Text2Digits()
                extracted_dosage_value = t2d.convert(extracted_dosage_value).strip()

            extracted_dosage_suffix = result_dict.get('dosage_suffix',"")
            dosage_value = extracted_dosage_value.lower().replace(" ","").strip()+extracted_dosage_suffix.lower().replace(" ","").strip()
            ehrc_df['MOLECULE_NAME'] = ehrc_df['MOLECULE_NAME'].str.lower()
            if dosage_value != "" and sum(ehrc_df["MOLECULE_NAME"].astype("str").str.contains(drugName)) > 0:
                correct_dosage_values = ehrc_df.loc[ehrc_df['MOLECULE_NAME'] == drugName.lower(), 'DOSAGE'].iloc[0].split(',')
                correct_dosage_v_list = [i.replace(" ","").strip() for i in correct_dosage_values]

                if dosage_value in correct_dosage_v_list:
                    return True
                else:
                    return False
            elif sum(ehrc_df["MOLECULE_NAME"].astype("str").str.contains(drugName)) == 0:
                print("Molecule Not Found in Master >> " + drugName )
                return "Molecule Not Found in Master"
            else:
                return "Exception"
#                 print("Something went wrong", result_dict)
        else:
#             print("Dosage Value Missing")
            return "Dosage Value Missing"
    except Exception as e:
        print(e)
        return "Exception"


# In[108]:


def startExtraction(pres_text, separator_list, dosage_suffix , ehrc_df,suggestions_accepted = []):
    
    current_text_str = pres_text.lower()
    result = dict()
    info_arr = []
    
    entity_frame = ["xxxDrugNamexxx","xxxDosageValuexxx","xxxDosageSuffxxx","xxxTIMINGxxx", "xxxDurationValuexxx","xxxDurationSuffxxx","xxxRemarksxxx"]
    
    entity_index = [-1,-1,-1,-1,-1,-1,-1]
    found_drug = False
    found_suffix = False
    found_dosageValue = False
    found_timing_c = False
    found_timing_w = False
    found_suffix_d = False
    found_durationValue = False
    found_remarks = False
    
    try:
        
        #Finding Medicine Name
        current_text_str, extracted_drug, found_drug = extractReplaceDrugName(current_text_str, suggestions_accepted) 
        if found_drug:
            result["medicine_name"] = extracted_drug.title()
            entity_index = updateEntityIndex(current_text_str,entity_frame)
        
        #Finding Dosage Suffix 
        current_text_str, extracted_suffix, found_suffix = extractReplaceDosageSuffix(current_text_str, dosage_suffix)
        
        if found_suffix:
            result["dosage_suffix"] = extracted_suffix
            entity_index = updateEntityIndex(current_text_str,entity_frame)
            
            current_text_str, extracted_dosageValue, found_dosageValue = extractReplaceDosage(current_text_str,current_text_str.find("xxxDosageSuffxxx"))
            if found_dosageValue:
                result["dosage_value"] = extracted_dosageValue
                entity_index = updateEntityIndex(current_text_str,entity_frame)
        
        #Finding timing words : Morning, Afternoon, Evening, Night     
        current_text_str_w, extracted_timing_w, found_timing_w  = extractReplaceTimingWords(current_text_str, timing_words)
        
        #Finding timing codes : eg 1-0-1, 1-0-0-1 etc.
        current_text_str_c, extracted_timing_c, found_timing_c  = extractReplaceTimingCode(current_text_str, timing_codes)
        
        if found_timing_c and not(found_timing_w):
            result["dosage_timing"] = extracted_timing_c
            current_text_str = current_text_str_c
            entity_index = updateEntityIndex(current_text_str,entity_frame)
            
        elif found_timing_w and not(found_timing_c):
            result["dosage_timing"] = extracted_timing_w
            current_text_str = current_text_str_w
            entity_index = updateEntityIndex(current_text_str,entity_frame)
        elif found_timing_w and found_timing_c:
            print("Found both timing Codes and Words")
            result["dosage_timing"] = extracted_timing_c
            current_text_str = current_text_str_c
            entity_index = updateEntityIndex(current_text_str,entity_frame)
        else:
            result["dosage_timing"] = "-"
            info_arr.append("No Dosage Time found in first pass")
            
        #Finding Duration Suffix 
        current_text_str, extracted_suffix_d, found_suffix_d = extractReplaceDurationSuffix(current_text_str, duration_suffix)
        
        if found_suffix_d:
            result["duration_suffix"] = extracted_suffix_d
            entity_index = updateEntityIndex(current_text_str,entity_frame)
            current_text_str, extracted_durationValue, found_durationValue = extractReplaceDuration(current_text_str,current_text_str.find("xxxDurationSuffxxx"))
            if found_durationValue:
                result["duration_value"] = extracted_durationValue
                entity_index = updateEntityIndex(current_text_str,entity_frame)
        
        
        #Finding Duration Suffix 
        current_text_str, extracted_remarks, found_remarks = extractReplaceRemarks(current_text_str, entity_frame, entity_index)
        
        if found_remarks:
            result["remarks"] = extracted_remarks
            entity_index = updateEntityIndex(current_text_str,entity_frame)
        else:
            result["remarks"] = "-"
                  
        
        #Find missing values from the first pass
        if not(found_drug):
            result["medicine_name"] ="-"
            info_arr.append("Drug Not Found in prescription text")
        if not(found_suffix):
            result["dosage_suffix"] =""
            info_arr.append("Dosage Suffix i.e. mg, mg/ml, gm not found in prescription text")
        
        if not(found_dosageValue):
            #try guessing
            current_text_str, guessed_value, found_dosageValue = guessDosageDurationValue(current_text_str,entity_frame, entity_index)
            if found_dosageValue:
                result["dosage_value"] = guessed_value.strip()
                entity_index = updateEntityIndex(current_text_str,entity_frame)
            else:
                result["dosage_value"] = 0
                info_arr.append("Dosage Value Not Found in prescription text")
        
        if not(found_suffix_d):
            result["duration_suffix"] = "-"
            info_arr.append("Duration Type Not Found in prescription text")
        
        if not(found_durationValue):
            current_text_str, guessed_value_d, found_durationValue = guessDosageDurationValue(current_text_str,entity_frame, entity_index,"duration")
            if found_durationValue:
                result["duration_value"] = guessed_value_d.strip()
                entity_index = updateEntityIndex(current_text_str,entity_frame)
            else:
                result["duration_value"] = 0
                info_arr.append("Duration Value Not Found in prescription text")
        
        
        #Validate Dosage
        dosage_check = validateDosageValue(result,ehrc_df)
        
        if dosage_check == False:
            result["dosageIncorrect"] = True
        elif dosage_check:
            result["dosageIncorrect"] = False
        elif dosage_check == "Molecule Not Found in Master":
            info_arr.append("Molecule Not Found in Master")
        else:
            result["dosageIncorrect"] = False
        
        result["info"]= info_arr
#         print(entity_index)
        return result
        
    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)
    
    return result    