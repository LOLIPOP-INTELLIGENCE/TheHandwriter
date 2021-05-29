import numpy as np
import cv2
import math
from random import randint
import random
from PIL import Image
#input the string
f = open("/Users/blackhole/Desktop/Handwritten_Digits/input_data.txt", "r")
contents = f.read()
contents=contents.strip()
#Splitting the input file by words - "word"
words=contents.split(" ")


print(words)
print(len(words))
tau=len(words)
i=0

#Consider this input - ['mediators', 'are', '\\n\\n\\n\\n', 'seeking', 'to', 'cement']
#The below while loop along with the try except is trying to convert "\\n\\n\\n\\n" to ['mediators', 'are', '\n', '\n', '\n', '\n', 'seeking', 'to', 'cement']
#Reason to do this is because later in the program if the program finds a '\n' as a word, it will fill the current line with empty spaces
while(i<tau):
    if(words[i].startswith('\n') or words[i].startswith('\\n')):
        if(words[i].startswith('\n')):
            word_t=(words[i][1:])
        else:
            word_t=(words[i][2:])
        words.insert(i,'\n')
        words[i+1]=word_t
        tau=tau+1
    i=i+1

try:
    while True:
        words.remove('')
except ValueError:
    pass

#generate random errors
l=0
pop=0
#errors_for_number_for_words is the number of words for which the program adds one error
#If it is 5 => For every 5 words there is 1 error
errors_for_number_for_words=13

#The below code adds an error character, a ~ to the begining of a word selected randomly with a frequency of errors_for_number_for_words
randomlist = []
if(((len(words))/errors_for_number_for_words)-3>=0):
    pop=int(((len(words))/errors_for_number_for_words)-3)
for i in range(0,pop):
    n = random.randint(2, len(words) - 3)
    while(words[n]=='\n'):
        n = random.randint(2,len(words)-3)
    randomlist.append(n)
for i in range(0,pop):
    word____err=words[randomlist[i]]
    word____err="~"+word____err
    words[randomlist[i]]=word____err

print(words)
print(len(words))


#Code to generate a word
def generate_word(img_prev, word__k, k,N___K,K___K,add_blank):
    #Random Set of Letters
    value = randint(2,3)
    #Random Error
    value_err = randint(1,11)

    #Retrieving path of revelant character

    #Convertng the word to characters
    sentence__k = list(word__k)
    if(str(sentence__k[0]).islower()):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[0] + '.jpg'
    elif(str(sentence__k[0])=='.'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_'+str(value)+'/' + 'dot' + '.jpg'
    elif (str(sentence__k[0]) == ','):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'comma' + '.jpg'
    elif (str(sentence__k[0]) == '"'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'quote' + '.jpg'
    elif (str(sentence__k[0]) == '\''):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'Squote' + '.jpg'

    elif (str(sentence__k[0]) == '!'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/!' + '.jpg'
    elif (str(sentence__k[0]) == '-'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/-' + '.jpg'
    elif (str(sentence__k[0]) == '%'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/%' + '.jpg'
    elif (str(sentence__k[0]) == '|'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/|' + '.jpg'
    elif (str(sentence__k[0]) == '\\'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/back' + '.jpg'
    elif (str(sentence__k[0]) == '='):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '=' + '.jpg'
    elif (str(sentence__k[0]) == '('):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '(' + '.jpg'
    elif (str(sentence__k[0]) == ')'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + ')' + '.jpg'
    elif (str(sentence__k[0]) == '*'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '*' + '.jpg'
    elif (str(sentence__k[0]) == '_'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '_' + '.jpg'
    elif (str(sentence__k[0]) == '/'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '/' + '.jpg'
    elif (str(sentence__k[0]) == ':'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'colon' + '.jpg'
    elif (str(sentence__k[0]) == '>'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '>' + '.jpg'
    elif (str(sentence__k[0]) == '<'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '<' + '.jpg'
    elif (str(sentence__k[0]) == '?'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '?' + '.jpg'
    elif (str(sentence__k[0]) == '}'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '}' + '.jpg'
    elif (str(sentence__k[0]) == '{'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '{' + '.jpg'
    elif (str(sentence__k[0]) == ';'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + ';' + '.jpg'
    elif (str(sentence__k[0]) == '+'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/+' + '.jpg'
    elif (str(sentence__k[0]) == '&'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/&' + '.jpg'
    elif (str(sentence__k[0]) == '['):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/[' + '.jpg'
    elif (str(sentence__k[0]) == ']'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/]' + '.jpg'



    elif (str(sentence__k[0]) == ' 'or str(sentence__k[0]) == '' or str(sentence__k[0]) == '\n'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank2' + '.jpg'
    elif (str(sentence__k[0]) == '~'):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Errors/' + 'Error' +str(value_err)+ '.jpg'
    elif (str(sentence__k[0]).isdigit()):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + sentence__k[0] + '.jpg'
    elif(str(sentence__k[0]).isupper()):
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[0] + sentence__k[0]+'.jpg'
    else:
        path__k = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'

    #path_k holds the path to the first character in a word. If the word is Hello, path_k is the path to 'H'
    print(path__k)

    #creating the first image

    #To create more difference between characters, we add a rotation of the image by -10º to 10º
    degree=random.randint(-10,10)
    #Read image
    img = cv2.imread(path__k)

    #The below code converts all the black pixel values of that character to a standard value
    #For example consider an image has a black pixel of (0,0,0) and a black pixel of (30,30,30). For a standard look for the character,
    #we convert all the black pixels to a random value between 0-50
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([50, 50, 50])
    mask = cv2.inRange(hsv, black_low, black_high)
    color_shade=randint(0,50)
    img[mask > 0] = (color_shade,color_shade,color_shade)

    #Adding a white padding of 3 pixels to the left and right of the image
    border = cv2.copyMakeBorder(
        img,
        top=0,
        bottom=0,
        left=3,
        right=3,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    #Adding the rotation
    im_pil = Image.fromarray(border)
    im_np = im_pil.rotate(degree,fillcolor='white')

    #Resizing the image and converting to numpy array so that we can concatenate images later on
    im_np = np.asarray(im_np)
    img = cv2.resize(im_np, (40, 114))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(img)
    final_img = img_np

    #doing the above for n-1 characters
    for i in range(1, len(sentence__k)):
        value_err = randint(1, 11)
        value = randint(2, 3)

        #Do note that the same thing is happening for the rest of the word which is from character [1,n-1]

        #DEGREE OF ROTATION FOR PHYSICS PROJECT
        #degree=random.randint(-6,6)

        #REAL DEGREE OF ROTATION
        degree = random.randint(-10,10)

        if (str(sentence__k[i]).islower()):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + '.jpg'
        elif (str(sentence__k[i]) == '.'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'dot' + '.jpg'
        elif (str(sentence__k[i]) == ','):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'comma' + '.jpg'
        elif (str(sentence__k[i]) == '\"'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'quote' + '.jpg'
        elif (str(sentence__k[i]) == '\''):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'Squote' + '.jpg'
        elif (str(sentence__k[i]) == ' ' or str(sentence__k[i]) == '' or str(sentence__k[i]) == '\n'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'
        elif (str(sentence__k[i]) == '~'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Errors/' + 'Error' +str(value_err)+'.jpg'
        elif (str(sentence__k[i]).isdigit()):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + sentence__k[i] + '.jpg'
        elif(str(sentence__k[i]).isupper()):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + sentence__k[i] + '.jpg'

        elif (str(sentence__k[i]) == '!'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/!' + '.jpg'
        elif (str(sentence__k[i]) == '-'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/-' + '.jpg'
        elif (str(sentence__k[i]) == '%'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/%' + '.jpg'
        elif (str(sentence__k[i]) == '|'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/|' + '.jpg'
        elif (str(sentence__k[i]) == '\\'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/back' + '.jpg'
        elif (str(sentence__k[i]) == '='):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '=' + '.jpg'
        elif (str(sentence__k[i]) == '('):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '(' + '.jpg'
        elif (str(sentence__k[i]) == ')'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + ')' + '.jpg'
        elif (str(sentence__k[i]) == '*'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '*' + '.jpg'
        elif (str(sentence__k[i]) == '_'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '_' + '.jpg'
        elif (str(sentence__k[i]) == '/'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'forward' + '.jpg'
        elif (str(sentence__k[i]) == ':'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + 'colon' + '.jpg'
        elif (str(sentence__k[i]) == '>'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '>' + '.jpg'
        elif (str(sentence__k[i]) == '<'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '<' + '.jpg'
        elif (str(sentence__k[i]) == '?'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '?' + '.jpg'
        elif (str(sentence__k[i]) == '}'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '}' + '.jpg'
        elif (str(sentence__k[i]) == '{'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + '{' + '.jpg'
        elif (str(sentence__k[i]) == ';'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/' + ';' + '.jpg'
        elif (str(sentence__k[i]) == '+'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/+' + '.jpg'
        elif (str(sentence__k[i]) == '&'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/&' + '.jpg'
        elif (str(sentence__k[i]) == '['):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/[' + '.jpg'
        elif (str(sentence__k[i]) == ']'):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_' + str(value) + '/]' + '.jpg'


        else:
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'
        print(path)
        img2 = cv2.imread(path)
        try:
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        except:
            print(path)
        black_low = np.array([0, 0, 0])
        black_high = np.array([50, 50, 50])
        mask = cv2.inRange(hsv, black_low, black_high)
        color_shade = randint(0, 100)
        img2[mask > 0] = (color_shade, color_shade, color_shade)
        border = cv2.copyMakeBorder(
            img2,
            top=0,
            bottom=0,
            left=3,
            right=3,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )
        im_pil = Image.fromarray(border)
        im_np = im_pil.rotate(degree,fillcolor='white')
        im_np = np.asarray(im_np)
        img2 = cv2.resize(im_np, (40, 114))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img_np2 = np.array(img2)
        final_img = np.concatenate((img_np, img_np2), axis=1)
        img_np = final_img


    #This is there to add the image of previous words from img_prev

    #Decide wether to add the previous part of the sentence to this word
    #For example, let the sentence be - "Hello there my name is Teddy"
    #After generating "Hello", k will be false since we don't have a previous image
    #After generating "there", k will be true and we will concatenate img_prev to final_img
    #Similarly, after generating "my", k will be true and the image for "Hello there"(stored in img_prev)
    #will be concatenated with final_img
    if (k):
        final_img = np.concatenate((img_prev, final_img), axis=1)


    if(add_blank):
        final_img = generate_blank(img_prev__k=final_img, N__k=N___K, k__k=K___K)

    return final_img



#Very similar logic for generating blank space
def generate_blank(img_prev__k, N__k, k__k):

    if(N__k>0):
        path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
        print(path)
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (40, 114))
        img_np = np.array(img)
        final_img = img_np
        for i in range(1, N__k):
            path = '/Users/blackhole/Desktop/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
            img2 = cv2.imread(path, 0)
            img2 = cv2.resize(img2, (40, 114))
            img_np2 = np.array(img2)
            final_img = np.concatenate((img_np, img_np2), axis=1)
            img_np = final_img
        if (k__k):
            final_img = np.concatenate((img_prev__k, final_img), axis=1)

        return final_img
    else:
        return img_prev__k


#f is the word number
f=0
#line output for each line
output=0
#array of sentences
sentences=[]

#The below 2 variables are debug that will be printed out later
MY_OUTPUT=''
MY_SENTENCE_OUTPUT=[]

#the word count should be less than total number of words
while(f<len(words)):
    k=60
    #Adding 60 characters in a line

    #k>0 so that we don't overflow in a line
    while(k>0):
        try:
            #Handle separate case for \n as a word. Hence checking here first
            if(words[f]!='\n'):

                #If we have not started with the line, ie 60 characters still remain
                if(k==60):

                    #To make it look random, we generate either 1 blank space or 2 before starting with the word
                    #X-holds the number of spaces to be generated(either 1 or 2)
                    #Here img_prev_k is 0 because we don't have a previous image to concatenate
                    #N__k is X(the number of spaces to add)
                    #k__k is false because we are not concatenating the previous image
                    X=randint(1,2)
                    output=generate_blank(img_prev__k=0,N__k=X,k__k=False)

                    #From 60 characters, we remove X characters as we have added that many spaces
                    k=k-X

                    #Now we generate our first word
                    #f is 0
                    #k is true because we want to add the previous image(the initial blank space(s)) generated above
                    #N__K is 3 because we add 3 units of blank space characters
                    #K__K is true because when we call generate_blank() function inside the generate_word() function, we
                    #would have generated the word and hence we want the generate_blank() function to also concatenate the word
                    #add_blank is also true since we want 3 blank spaces
                    output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=3, K___K=True, add_blank=True)

                    #NOTE: My_OUTPUT is just a debug variable and has no significance to the running of the program
                    MY_OUTPUT = MY_OUTPUT + words[f] + '   '

                    #Remove the number of characters of word[f] and 3 spaces from k
                    k=k-(len(words[f])+3)

                    #Successfuly added the first word
                    f=f+1

                #Now if we do not have 60 characters left in a line
                else:

                    #Here we check if we can completely add the word in the given line
                    #For exmaple, If our sentence is - Hello there my name is bcdgdcdgchdghghcghjs
                    #Obviously bcdgdcdgchdghghcghjs cannot be added in the same line so the below condition checks for that
                    if(k-len(words[f])>=0):

                        #t tells us how many blank spaces we can add after adding our current word
                        #The standrad is 3 spaces but in the case that after adding the word, there is only 1 character left
                        #we take the minimum of 3 and k-len(words[f)
                        t=min(3,k-len(words[f]))
                        #Now we generate the word
                        #The parameters mean the same as they did above when k was == 60
                        output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=t, K___K=True, add_blank=True)

                        #Debug variable
                        MY_OUTPUT=MY_OUTPUT+words[f]
                        MY_OUTPUT = MY_OUTPUT.ljust(t + len(MY_OUTPUT), ' ')

                        #Subtracting the length of the word and the number of spaces added(t) from k
                        k=k-(len(words[f])+t)

                        #Successfuly added the word, and increment f
                        f=f+1


                    #This is the case when the full word cannot be accomodated in the same line and so we just add blank
                    #spaces to the rest of the line
                    else:

                        #We generate k number of blank spaces since we cannot accomodate any word on that line
                        output=generate_blank(img_prev__k=output,N__k=k,k__k=True)

                        #Debug var
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                        #END OF LINE, k>0 condition will fail in the above while loop
                        k=-1


            #This is the case when we have encountered a '\n' word. We now need to add an empty line
            else:

                #We check if '\n' is not the first word
                if(k!=60):

                    #We generate as many blank spaces as are left on that line, ie k
                    output = generate_blank(img_prev__k=output, N__k=k, k__k=True)

                    #Debug var
                    MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                    #END OF LINE
                    k = -1

                    #Increment the word('\n')
                    f=f+1

                #This is the case when '\n' is the first word
                else:

                    #We generate 60 blanks, which is = k.
                    #Note the only difference here is that k__k is false since we don't have a previous image
                    output = generate_blank(img_prev__k=output, N__k=k, k__k=False)

                    #Debug var
                    MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                    #End of line
                    k=-1

                    #Increment the word('\n')
                    f=f+1

        #In the case that some random error occurs, we just add that many blank spaces to the line:)
        except IndexError:
            output = generate_blank(img_prev__k=output, N__k=k, k__k=True)

            #Debug var
            MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

            #END OF LINE
            k=-1
            pass

    #Debug var
    MY_OUTPUT = MY_OUTPUT + '!'
    MY_SENTENCE_OUTPUT.append(MY_OUTPUT)
    MY_OUTPUT = ''

    #Sentences hols all the sentences. output is the output for that line
    sentences.append(output)
    output = 0


#Debug printing
for i in range(len(MY_SENTENCE_OUTPUT)):
    print(MY_SENTENCE_OUTPUT[i])


#Concatenatig all sentences to produce the final image
final_output = sentences[0]
print(final_output.shape)
for i in range(1,len(sentences)):
    print(sentences[i].shape)
    final_output = np.concatenate((final_output, sentences[i]), axis=0)


#BORDER VALUES FOR PHYSICS PROJECT
# border = cv2.copyMakeBorder(
#     final_output,
#     top=120,
#     bottom=40,
#     left=100,
#     right=30,
#     borderType=cv2.BORDER_CONSTANT,
#     value=[255,255,255]
# )
# border = cv2.copyMakeBorder(
#     border,
#     top=5,
#     bottom=5,
#     left=5,
#     right=5,
#     borderType=cv2.BORDER_CONSTANT,
#     value=[38,38,38]
# )
# border = cv2.copyMakeBorder(
#     border,
#     top=100,
#     bottom=100,
#     left=100,
#     right=100,
#     borderType=cv2.BORDER_CONSTANT,
#     value=[255,255,255]
#)


#REAL BORDER VALUES
#Adding a border for the page
border = cv2.copyMakeBorder(
    final_output,
    top=120,
    bottom=40,
    left=100,
    right=30,
    borderType=cv2.BORDER_CONSTANT,
    value=[255,255,255]
)

#COMP BORDERS
# border = cv2.copyMakeBorder(
#     final_output,
#     top=240,
#     bottom=40,
#     left=100,
#     right=30,
#     borderType=cv2.BORDER_CONSTANT,
#     value=[255,255,255]
# )


#SAVING
path='/Users/blackhole/Desktop/Handwritten_Digits/FINAL_RESULToutput.jpg'
cv2.imwrite(path, border)