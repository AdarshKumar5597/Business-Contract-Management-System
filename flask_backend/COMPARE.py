import re
from sklearn.cluster import KMeans
import numpy as np
from sentence_transformers import SentenceTransformer, util
from termcolor import colored
from sklearn.metrics import silhouette_score

model = SentenceTransformer("all-MiniLM-L6-v2")


def getOptimalKValue(K, data):
    label_score_array = []
    label_score = []
    for k in range(2, min(K, len(data))):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        score = silhouette_score(data, kmeans.labels_, metric='euclidean')
        label_score = [k, score]
        label_score_array.append(label_score)
    
    label_score_array = sorted(label_score_array, key=lambda x: x[1], reverse=True)
    print(label_score_array)
    return label_score_array[0][0]
        
        
    

def split_into_sentences(text: str) -> list[str]:
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'
    text = text.replace('\n', ' ').replace('\r', '')
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    text = text.replace("**", "")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences


def generate_filtered_sentences(para):
    para = split_into_sentences(para)
    sentences = para
    # Regular expression pattern to match strings that contain only a number followed by a period
    pattern = re.compile(r'^\d+\.$')
    # Filter out the elements that match the pattern
    filtered_sentences = [sentence for sentence in sentences if not pattern.match(sentence.strip())]
    # Print the filtered list
    return filtered_sentences


def compare(template, original):
    filtered_template = generate_filtered_sentences(template)
    filtered_original = generate_filtered_sentences(original)
    
    # Compute embeddings
    filtered_original_embeddings = model.encode(filtered_original, convert_to_tensor=True)
    filtered_template_embeddings = model.encode(filtered_template, convert_to_tensor=True)
    filtered_template_embeddings = filtered_template_embeddings / np.linalg.norm(filtered_template_embeddings, axis = 1, keepdims=True)
    
    k_value = getOptimalKValue(10, filtered_template_embeddings)
    
    filtered_contract_template_model = KMeans(n_clusters=k_value, random_state=0)
    filtered_contract_template_model.fit(filtered_template_embeddings)
    filtered_contract_template_assignment = filtered_contract_template_model.labels_
    print(filtered_contract_template_assignment)
    
    template_clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(filtered_contract_template_assignment):
        if cluster_id not in template_clustered_sentences:
            template_clustered_sentences[cluster_id] = []
        template_clustered_sentences[cluster_id].append(filtered_template[sentence_id])
        

    cluster_list = filtered_contract_template_assignment
    cluster_list = list(set(cluster_list))
    cluster_list
    
    filtered_template_embeddings = model.encode(filtered_template)
    cs_sim_new = util.pytorch_cos_sim(filtered_template_embeddings, filtered_original_embeddings)
    
    most_similar_sentences = []
    maxNum = 0
    for i in range(len(filtered_template)):
        maxNum = 0
        for j in range(len(filtered_original)):
            if cs_sim_new[i][j].item() > maxNum:
                maxNum = cs_sim_new[i][j].item()
                similar_sentence = [maxNum, i, j]
        most_similar_sentences.append(similar_sentence)
    most_similar_sentences
    
    filtered_sentences_cluster = {}
    for sentence in most_similar_sentences:
        for cluster in template_clustered_sentences:
            if filtered_template[sentence[1]] in template_clustered_sentences[cluster]:
                if cluster not in filtered_sentences_cluster:
                    filtered_sentences_cluster[cluster] = []
                filtered_sentences_cluster[cluster].append(filtered_original[sentence[2]])
       
    # 10 random colors         
    colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'grey', 'black', 'purple']
    
    original_contract_text = ''
    sentence_is_present = False
    for sentence in filtered_original:
        sentence_is_present = False
        for cluster in filtered_sentences_cluster:
            if sentence in filtered_sentences_cluster[cluster]:
                sentence_is_present = True
                original_contract_text += colored(sentence, colors[cluster]) + '\n'
                break
        if not sentence_is_present:
            original_contract_text += sentence + '\n'
            
    
    template_text = ''
    for cluster in template_clustered_sentences:
        for sentence in template_clustered_sentences[cluster]:
            template_text += colored(sentence, colors[cluster]) + '\n'
            
    print("TEMPLATE TEXT: ", template_text)
    print("ORIGINAL TEXT: ", original_contract_text)

    return filtered_sentences_cluster, template_clustered_sentences, filtered_original