# @ Tarea 2 - Tecnologias de busqueda en la Web
#             Leonardo Santis - 2010735478 - leonardo.santis@alumnos.usm.cl
#             Alonso Orellana - rol - mail
#             Rodrigo Martinez - rol - mail

import os
import re
import math
import time

# This method is used to parse the doc-topic documents generated
# by Mallet, it saves them into an dictionary where the key is 
# part of the filename (that specifies its parameters) 
# Each entry is saved as a dictionary with its respective parameters
# and a list that has the respective weights for every document
# for each topic
def get_doc_topics():

    doc_topics = dict()

    for file in os.listdir("doc-topics"):
        if file.endswith(".mallet"):
            
            # Get parameters form filename}

            file_split = file[len("doc-topics-"):-len(".mallet")]
            part,alpha,beta,k = (i for i in file_split.split('-'))

            # Put into doc_topic

            doc_topic = {}
            doc_topic["alpha"] = int(alpha)
            doc_topic["beta"] = float(beta)
            doc_topic["k"] = int(k)
            doc_topic["part"] = part
            doc_topic["proportions"] = dict()

            # Read Text

            f = open("doc-topics/" + file,"r")

            file_lines = f.readlines()

            # For each line..

            for line in file_lines[1:]:

                params = re.findall(r"[\S']+", line)

                doc_data = {}
                doc_data["name"] = params[1]
                doc_data["z_d"] = {}

                for i in range(doc_topic["k"]):
                    doc_data["z_d"][int(params[2+i*2])] = float(params[3+i*2])

                # Insert into proportions

                doc_topic["proportions"][doc_data["name"]] = doc_data

            # Insert into doc_topics

            doc_topics[file_split] = doc_topic

            # Close file

            f.close()

    return doc_topics

# This method is used to parse the topic-word-weights documents generated
# by Mallet, it saves them into an dictionary where the key is 
# part of the filename (that specifies its parameters) 
# Each entry is saved as a dictionary with its respective parameters
# and a matrix that has the respective weights for every topic
# and for each vocabulary term
def get_topic_words():

    topic_words = dict()

    for file in os.listdir("topic-word"):
        if file.endswith(".mallet"):
            
            # Get parameters form filename}

            file_split = file[len("topic-word-weights-"):-len(".mallet")]
            part,alpha,beta,k = (i for i in file_split.split('-'))

            # Put into doc_topic

            topic_word = {}
            topic_word["alpha"] = int(alpha)
            topic_word["beta"] = float(beta)
            topic_word["k"] = int(k)
            topic_word["part"] = part
            topic_word["proportions"] = []

            for i in range(topic_word["k"]):
                topic_word["proportions"].append(list())

            # Read Text

            f = open("topic-word/" + file,"r")

            file_lines = f.readlines()

            # For each line..

            for line in file_lines:

                params = re.findall(r"[\S']+", line)

                vocab_data = {}
                vocab_data["z"] = int(params[0])
                vocab_data["vocab"] = params[1]
                vocab_data["w_z"] = float(params[2])

                topic_word["proportions"][vocab_data["z"]].append(vocab_data)

            # Insert into topic_words

            topic_words[file_split] = topic_word

            # Close file

            f.close()

    return topic_words

# This method calculates the verisimilitude L_z from each configuration
# of parameters, using the formula seen in the course
def calculate_verisimilitude(doc_topics,topic_words):

    l_z = dict()

    for file_split, doc_topic in doc_topics.items():

        if doc_topic["part"] != "both":
                continue
        a = 0.0
        for doc_name,d in doc_topic["proportions"].items():
            topic_word = topic_words[file_split]
            b = 1.0
            for w in range(doc_topic["k"]):
                c = 0.0
                for z in topic_word["proportions"][w]:
                    c = c + z["w_z"]*doc_topic["proportions"][doc_name]["z_d"][w]
                b = b*c
            a = a + math.log(b,2)
        l_z[file_split] = a

    return l_z

# Homework 2 -

# Timer

start_time = time.time()

# Open ALL doc-topics

doc_topics = get_doc_topics()

# Open ALL topic-words

topic_words = get_topic_words()

# Calculate ALL L_z values for every configuration

l_z = calculate_verisimilitude(doc_topics,topic_words)

# Write the verisimilitudes from each configuration to file

i = open("l_z.txt","w")
for k,v in sorted(l_z.items(),key=lambda tuple: tuple[1]):
    i.write("'" + k + "' : L_z = " + str(v) + "\n")
i.close()

print("$ {0} L_z indexes calculated in {1} seconds, Values saved > l_z.txt".format(len(l_z), time.time() - start_time))