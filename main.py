import utilities


## 1
def parse_story(file_name):
    '''
    Don't forget to fill in your docstrings
    '''
    final = []
    f =  open(file_name,"rt")

    lines = f.read().lower()

    for ch in utilities.BAD_CHARS:
        lines = lines.replace(ch, '')
    for ch in utilities.VALID_PUNCTUATION:
        lines = lines.replace(ch, ' ' + ch + ' ')


    final = lines.split()

    return final

    
    f.close()


## 2
def get_prob_from_count(counts):
    '''
    Don't forget to fill in your docstrings
    '''

    return [counts[i]/sum(counts) for i in range(len(counts))]


## 3
def build_ngram_counts(words, n):
    '''
    Don't forget to fill in your docstrings
    '''
    
    word_list = []
    alt_list = []
   
    # forming keys (tuple list)
    for i in range(0,len(words)-n+1):
        temp = []
        temp = [words[i+j] for j in range(n)]
        word_list.append(tuple(temp))
        alt_list.append(temp)
    
    #main_set = set(word_list) 
        
    l = len(word_list)
    values = []

    #X = word_list[:] 
    
    predictions = []
    alt_preds = []


    # counts and pred_words
    for k in range(l):
        pred1 = []
        pred2 = [] 

        for i in range(l-1):
            
            if ( word_list[i] == word_list[k]) :
                pred1.append(word_list[i+1][1])
                print(word_list[i+1][1])
            if ( word_list[i] == word_list[k] and word_list[i+1][1] not in pred2) :
                pred2.append(word_list[i+1][1])

        alt_preds.append(pred1)
        predictions.append(pred2)
    
    counts = []

    for i in range(len(predictions)):
        tcount = []
        for j in range(len(predictions[i])):
            tcount.append(alt_preds[i].count(predictions[i][j]))

            
        counts.append(tcount)


    
    final = {word_list[i]:[predictions[i], counts[i]] for i in range(l-1)}   ######## CKECK "l-1" term

    return final


## 4
def prune_ngram_counts(counts, prune_len):
    '''
    Don't forget to fill in your docstrings
    '''

    pred_list = [counts[i][0] for i in counts]
    count_nums = [counts[i][1] for i in counts]
    keys = [k for k in counts]

    newt = []

    np=[]
    nc= []

    for r in range(len(keys)):
        newf= []
        t1 = []
        t2 = []
        newf = [(count_nums[r][i] ,pred_list[r][i]) for i in range(len(pred_list[r]))]
        print(newf)
        newf = sorted(newf, key = lambda a : a[0])                  # [ [(counts, preds),(counts, preds)]  ,  [(),()] ]
        newf.reverse()
        print(newf)
        newt.append(newf)

        new_preds = [newf[i][1] for i in range(len(newf)) ]
        np.append(new_preds)

        new_counts = [newf[i][0] for i in range(len(newf)) ]
        nc.append(new_counts)


    f = { keys[i]:[np[i],nc[i]] for i in range(len(keys)) }
    
    for k in keys:
        if(len(f[k][1])>prune_len):
            M = f[k][1][prune_len-1]
            eliminator = []
            for n in range(prune_len, len(f[k][1])):
                if(f[k][1][n] != M):
                    eliminator.append(n)
                    break
            if(eliminator):
                for e in range(len(f[k][1])-1, eliminator[0]-1, -1):
                    del f[k][1][e]
                    del f[k][0][e]
            
        print(f)

    
    return f

## 5
def probify_ngram_counts(counts):
    '''
    Don't forget to fill in your docstrings
    '''

    
    keys = [k for k in counts]
    pred_list = [counts[i][0] for i in counts]
    count_nums = [counts[i][1] for i in counts]

    probs = [get_prob_from_count(counts[i][1]) for i in counts]


    final = {keys[a]: [ pred_list[a], probs[a]] for a in range(len(counts))}

    return final

## 6
def build_ngram_model(words, n):
    '''
    Don't forget to fill in your docstrings
    '''
    counts = probify_ngram_counts( prune_ngram_counts( build_ngram_counts(words, n), 15 ) )
  
    
    pred_list = [counts[i][0] for i in counts]
    count_nums = [counts[i][1] for i in counts]
    keys = [k for k in counts]

    newt = []

    np=[]
    nc= []

    for r in range(len(keys)):
        newf= []
        t1 = []
        t2 = []
        newf = [(count_nums[r][i] ,pred_list[r][i]) for i in range(len(pred_list[r]))]
        print(newf)
        newf = sorted(newf, key = lambda a : a[0])                  # [ [(counts, preds),(counts, preds)]  ,  [(),()] ]
        newf.reverse()
        print(newf)
        newt.append(newf)

        new_preds = [newf[i][1] for i in range(len(newf)) ]
        np.append(new_preds)

        new_counts = [newf[i][0] for i in range(len(newf)) ]
        nc.append(new_counts)




    print(np)    #[[c1,c2],[c1,c2,c3,c4]]
    # new_counts = [newt[r][i][0] for r in range(len(newt)) for i in range(len(newt[r]))]
    print(nc)    #[[c1,c2],[c1,c2,c3,c4]]
    print()

    f = { keys[i]:[np[i],nc[i]] for i in range(len(keys)) }
    
    return f





## 7
def gen_bot_list(ngram_model, seed, num_tokens=0):
    '''
    Don't forget to fill in your docstrings
    '''
    s = tuple(list(seed)[:])
    l = len(seed)
    nl = list(seed)

    if(num_tokens==0):
        return []

    if(len(nl) >= num_tokens):
        return nl[0:num_tokens-1]

    else:

        if(s not in ngram_model):
            return nl

        else:

            ctr = 1
            while((s in ngram_model) and(len(nl)<num_tokens)):   
                newt = utilities.gen_next_token(s, ngram_model)
                nl.append(newt)
                s = tuple(nl[f] for f in range(ctr, l+ctr))
                ctr += 1
            return nl 


        

    
    # while(len(final)<num_tokens))
    

## 8
def gen_bot_text(token_list, bad_author):
    '''
    Don't forget to fill in your docstrings
    '''
    s = ''
    if(bad_author == True):
        for i in token_list:
            s = s + i + ' '
        s = s.strip(' ')

        return s

    else:
        t = token_list[:]
        for i in range(len(token_list)):
            if (t[i] in utilities.VALID_PUNCTUATION):
                s = s.strip(' ')
                s = s + t[i] + ' '
            elif(t[i-1] in utilities.END_OF_SENTENCE_PUNCTUATION):
                s = s + t[i].capitalize() + ' '
            
            elif(t[i].capitalize() in utilities.ALWAYS_CAPITALIZE):
                s = s + t[i].capitalize() + ' '
            
            else:
                s = s + t[i] + ' '
            
        
        s = s.strip(' ')
        return s 

## 9
def write_story(file_name, text, title, student_name, author, year):
    '''
    Don't forget to fill in your docstrings
    '''

    f = open(file_name, "wt")
    f.write("\n\n\n\n\n\n\n\n\n\n"+ title + ": " + str(year) + ", UNLEASHED\n" + student_name + ", inspired by "+ author+ "\nCopyright year published (" + str(year) + "), publisher: EngSci press\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    
    line = []
    t = text.split()

    t = gen_bot_text(t, False)

    t = t.split()

    print(t)
    
    l = 1   # line number
    p = 1   # page number
    ch = 1  # chapter number

    pn = 1  # pg no. (to show)
    chn = 1  # ch no. (to show)

    f.write("CHAPTER "+ str(chn) + "\n\n")
    l += 2
    ch += 1
    chn += 1

    for i in t:

        if (p == 13 and l == 1):
            f.write("CHAPTER "+ str(chn) + "\n"*2)
            ch += 1 
            chn += 1
            p = 1
            l+=2
            line.append(i)
             


        elif (l == 29):
            f.write('\n'+ str(pn) +'\n')
            p += 1
            pn += 1
            l = 1            
            line.append(i)      # writing first word, so dont worry about len going over 90
            


        elif (len(" ".join(line)) + len(i) >= 90):
            line = " ".join(line)
            line.strip()
            line += '\n'
            f.write(line)
            line = []
            line.append(i)
            l += 1

        else:
            line.append(i)
    
    if(line):                                       # re-ckeck correctness of this later
        f.write(" ".join(line) + '\n')
        l += 1

    for i in range(l,30):
        f.write('\n')

    f.write(str(pn))
    f.close()
