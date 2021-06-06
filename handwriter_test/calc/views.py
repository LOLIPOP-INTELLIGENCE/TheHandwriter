from django.shortcuts import render
from django.http import HttpResponse


import numpy as np
import cv2
import math
from random import randint
import random
from PIL import Image
#input the string
def hand_w(input_string):
    contents=input_string
    contents=contents.strip()
    words=contents.split(" ")


    print(words)
    print(len(words))
    tau=len(words)
    i=0
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
    errors_for_number_for_words=13

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

    image=func_two(words)
    return image

def generate_word(img_prev, word__k, k,N___K,K___K,add_blank):
    #Random Set of Letters
    value = randint(2,3)
    #Random Error
    value_err = randint(1,11)

    #Retrieving path of revelant character
    sentence__k = list(word__k)
    if(str(sentence__k[0]).islower()):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[0] + '.jpg'
    elif(str(sentence__k[0])=='.'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + 'dot' + '.jpg'
    elif (str(sentence__k[0]) == ','):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'comma' + '.jpg'
    elif (str(sentence__k[0]) == '"'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'quote' + '.jpg'
    elif (str(sentence__k[0]) == '\''):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'Squote' + '.jpg'

    elif (str(sentence__k[0]) == '!'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/!' + '.jpg'
    elif (str(sentence__k[0]) == '-'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/-' + '.jpg'
    elif (str(sentence__k[0]) == '%'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/%' + '.jpg'
    elif (str(sentence__k[0]) == '|'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/|' + '.jpg'
    elif (str(sentence__k[0]) == '\\'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/back' + '.jpg'
    elif (str(sentence__k[0]) == '='):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '=' + '.jpg'
    elif (str(sentence__k[0]) == '('):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '(' + '.jpg'
    elif (str(sentence__k[0]) == ')'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + ')' + '.jpg'
    elif (str(sentence__k[0]) == '*'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '*' + '.jpg'
    elif (str(sentence__k[0]) == '_'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '_' + '.jpg'
    elif (str(sentence__k[0]) == '/'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '/' + '.jpg'
    elif (str(sentence__k[0]) == ':'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'colon' + '.jpg'
    elif (str(sentence__k[0]) == '>'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '>' + '.jpg'
    elif (str(sentence__k[0]) == '<'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '<' + '.jpg'
    elif (str(sentence__k[0]) == '?'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '?' + '.jpg'
    elif (str(sentence__k[0]) == '}'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '}' + '.jpg'
    elif (str(sentence__k[0]) == '{'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '{' + '.jpg'
    elif (str(sentence__k[0]) == ';'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + ';' + '.jpg'
    elif (str(sentence__k[0]) == '+'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/+' + '.jpg'
    elif (str(sentence__k[0]) == '&'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/&' + '.jpg'
    elif (str(sentence__k[0]) == '['):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/[' + '.jpg'
    elif (str(sentence__k[0]) == ']'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/]' + '.jpg'



    elif (str(sentence__k[0]) == ' 'or str(sentence__k[0]) == '' or str(sentence__k[0]) == '\n'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank2' + '.jpg'
    elif (str(sentence__k[0]) == '~'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Errors/' + 'Error' +str(value_err)+ '.jpg'
    elif (str(sentence__k[0]).isdigit()):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + sentence__k[0] + '.jpg'
    elif(str(sentence__k[0]).isupper()):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[0] + sentence__k[0]+'.jpg'
    else:
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'

    print(path__k)

    #creating the first image
    degree=random.randint(-10,10)
    img = cv2.imread(path__k)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([50, 50, 50])
    mask = cv2.inRange(hsv, black_low, black_high)
    color_shade=randint(0,50)
    img[mask > 0] = (color_shade,color_shade,color_shade)
    border = cv2.copyMakeBorder(
        img,
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
    img = cv2.resize(im_np, (40, 114))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(img)
    final_img = img_np
    #doing the above for n-1 characters
    for i in range(1, len(sentence__k)):
        value_err = randint(1, 11)
        value = randint(2, 3)

        #DEGREE OF ROTATION FOR PHYSICS PROJECT
        #degree=random.randint(-6,6)

        #REAL DEGREE OF ROTATION
        degree = random.randint(-10,10)

        if (str(sentence__k[i]).islower()):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + '.jpg'
        elif (str(sentence__k[i]) == '.'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'dot' + '.jpg'
        elif (str(sentence__k[i]) == ','):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'comma' + '.jpg'
        elif (str(sentence__k[i]) == '\"'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'quote' + '.jpg'
        elif (str(sentence__k[i]) == '\''):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'Squote' + '.jpg'
        elif (str(sentence__k[i]) == ' ' or str(sentence__k[i]) == '' or str(sentence__k[i]) == '\n'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'
        elif (str(sentence__k[i]) == '~'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Errors/' + 'Error' +str(value_err)+'.jpg'
        elif (str(sentence__k[i]).isdigit()):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + sentence__k[i] + '.jpg'
        elif(str(sentence__k[i]).isupper()):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + sentence__k[i] + '.jpg'

        elif (str(sentence__k[i]) == '!'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/!' + '.jpg'
        elif (str(sentence__k[i]) == '-'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/-' + '.jpg'
        elif (str(sentence__k[i]) == '%'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/%' + '.jpg'
        elif (str(sentence__k[i]) == '|'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/|' + '.jpg'
        elif (str(sentence__k[i]) == '\\'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/back' + '.jpg'
        elif (str(sentence__k[i]) == '='):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '=' + '.jpg'
        elif (str(sentence__k[i]) == '('):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '(' + '.jpg'
        elif (str(sentence__k[i]) == ')'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + ')' + '.jpg'
        elif (str(sentence__k[i]) == '*'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '*' + '.jpg'
        elif (str(sentence__k[i]) == '_'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '_' + '.jpg'
        elif (str(sentence__k[i]) == '/'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'forward' + '.jpg'
        elif (str(sentence__k[i]) == ':'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + 'colon' + '.jpg'
        elif (str(sentence__k[i]) == '>'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '>' + '.jpg'
        elif (str(sentence__k[i]) == '<'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '<' + '.jpg'
        elif (str(sentence__k[i]) == '?'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '?' + '.jpg'
        elif (str(sentence__k[i]) == '}'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '}' + '.jpg'
        elif (str(sentence__k[i]) == '{'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + '{' + '.jpg'
        elif (str(sentence__k[i]) == ';'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/' + ';' + '.jpg'
        elif (str(sentence__k[i]) == '+'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/+' + '.jpg'
        elif (str(sentence__k[i]) == '&'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/&' + '.jpg'
        elif (str(sentence__k[i]) == '['):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/[' + '.jpg'
        elif (str(sentence__k[i]) == ']'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_' + str(value) + '/]' + '.jpg'


        else:
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'
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
    if (k):
        final_img = np.concatenate((img_prev, final_img), axis=1)
    if(add_blank):
        final_img = generate_blank(img_prev__k=final_img, N__k=N___K, k__k=K___K)

    return final_img



#Very similar logic for generating blank space
def generate_blank(img_prev__k, N__k, k__k):

    if(N__k>0):
        path = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
        print(path)
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (40, 114))
        img_np = np.array(img)
        final_img = img_np
        for i in range(1, N__k):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
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


#f-word number
def func_two(words):
    f=0
    #line output
    output=0
    #array of sentences
    sentences=[]

    MY_OUTPUT=''
    MY_SENTENCE_OUTPUT=[]
    while(f<len(words)):
        k=60
        #Adding 60 characters in a line
        while(k>0):
            try:
                if(words[f]!='\n'):
                    if(k==60):
                        X=randint(1,2)
                        output=generate_blank(img_prev__k=0,N__k=X,k__k=False)
                        k=k-X
                        output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=3, K___K=True, add_blank=True)
                        MY_OUTPUT = MY_OUTPUT + words[f] + '   '
                        k=k-(len(words[f])+3)
                        f=f+1
                    else:
                        if(k-len(words[f])>=0):
                            t=min(3,k-len(words[f]))
                            output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=t, K___K=True, add_blank=True)
                            MY_OUTPUT=MY_OUTPUT+words[f]
                            MY_OUTPUT = MY_OUTPUT.ljust(t + len(MY_OUTPUT), ' ')
                            k=k-(len(words[f])+t)
                            f=f+1

                        else:
                            output=generate_blank(img_prev__k=output,N__k=k,k__k=True)
                            MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                            k=-1
                else:
                    if(k!=60):
                        output = generate_blank(img_prev__k=output, N__k=k, k__k=True)
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                        k = -1
                        f=f+1
                    else:
                        output = generate_blank(img_prev__k=output, N__k=k, k__k=False)
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                        k=-1
                        f=f+1
            except IndexError:
                output = generate_blank(img_prev__k=output, N__k=k, k__k=True)
                MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                k=-1
                pass

        MY_OUTPUT = MY_OUTPUT + '!'
        MY_SENTENCE_OUTPUT.append(MY_OUTPUT)
        MY_OUTPUT = ''
        sentences.append(output)
        output = 0


    for i in range(len(MY_SENTENCE_OUTPUT)):
        print(MY_SENTENCE_OUTPUT[i])

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

    path='D:\TheHandwriter\handwriter_test\static\FINAL_RESULToutput.png'
    cv2.imwrite(path, border)

    return border
# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': ''})

val1=''
def add(request):
    global val1

    val1 = request.GET['text_string']
    image=hand_w(val1)
    return render(request, "choice.html")

def h1(request):
    return render(request, "result.html")
    
def h2(request):
    return render(request, "result.html")

def h3(request):
    return render(request, "result.html")

def h4(request):
    return render(request, "result.html")

def h5(request):
    return render(request, "result.html")

def h6(request):
    return render(request, "result.html")

def own_handwriting(request):
    return render(request, "io.html")
