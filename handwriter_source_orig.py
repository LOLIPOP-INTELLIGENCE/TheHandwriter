
import math, random
import cv2
import PIL
import numpy as np

chars_path  = 'D:\\TheHandwriter\\Handwritten_Digits\\'
set_path    = chars_path + 'Set_{}\\'

# Input the string
f           = open(chars_path + 'input_data.txt' 'r')
contents    = f.read().strip()
words       = contents.split(" ")

tau         = len(words)
print(words, '\n', tau)

i = 0
while i < tau:
    if words[i][0] == '\n' or words[i][0] == '\\n':
        if(words[i].startswith('\n')):
            word_t=(words[i][1:])
        else:
            word_t=(words[i][2:])
        words.insert(i,'\n')
        words[i+1]=word_t
        tau=tau+1
    i += 1

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

def generate_word( img_prev, word__k, k, N___K, K___K, add_blank ):

    # Random Set of Letters and errors
    value       = random.randint( 2, 3 )
    my_path     = set_path.format( value ) + '\\{}.jpg'
    value_err   = random.randint( 1, 11 )

    # Retrieving path of relevant character
    sentence__k = list( word__k )
    init__k     = str( sentence__k[0] )

    char__lst   = [('.', 'dot'), (',', 'comma'), ('"', 'quote'), ("'", 'squote'),
                ('!', '!'), ('-', '-'), ('%', '%'), ('|', '|'),
                ('\\', 'back'), ('=', '='), ('(', '('), (')', ')'),
                ('*', '*'), ('_', '_'), ('/', '/'), (':', 'colon'),
                ('>', '>'), ('<', '<'), ('?', '?'), ('}', '}'),
                ('{', '{'), (';', ';'), ('+', '+'), ('&', '&'),
                ('[', '['), (']', ']')]

    # If lower case, digit or upper case then use self
    if init__k.islower() or init__k.isdigit():
        path__k = my_path.format(sentence__k[0])
    elif init__k.isupper():
        path__k = my_path.format(sentence__k[0] * 2)

    # If space or newline or invalid then use blank
    elif init__k == ' ' or init__k == '' or init__k == '\n':
        path__k = chars_path + 'Set_1\\blank2.jpg'

    # If tilda then error
    elif (init__k == '~'):
        path__k = chars_path + 'Errors\\Error{}.jpg'.format(value_err)

    # Go through list of specials if nothing is found
    else:
        path__k = chars_path + 'Set_1\\blank1.jpg'
        for pair in char__lst:
            if init__k == pair[0]:
                path__k = my_path.format(pair[1])
                break

    print(path__k)

    # Creating the first image
    degree=random.randint(-10,10)
    img = cv2.imread(path__k)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([50, 50, 50])
    mask = cv2.inRange(hsv, black_low, black_high)
    color_shade=random.randint(0,50)
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
    im_pil = PIL.Image.fromarray(border)
    im_np = im_pil.rotate(degree,fillcolor='white')
    im_np = np.asarray(im_np)
    img = cv2.resize(im_np, (40, 114))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(img)
    final_img = img_np
    #doing the above for n-1 characters

    for i in range(1, len(sentence__k)):
        value_err   = random.randint(1, 11)
        value       = random.randint(2, 3)

        #DEGREE OF ROTATION FOR PHYSICS PROJECT
        #degree=random.randint(-6,6)

        #REAL DEGREE OF ROTATION
        degree = random.randint(-10,10)

        init__ki = str( sentence__k[i] )

        if init__ki.islower() or init__ki.isdigit():
            path = my_path.format(sentence__k[i])
        elif init__k.isupper():
            path = my_path.format(sentence__k[i] * 2)
        elif init__ki == '~':
            path = chars_path + 'Errors\\Error{}.jpg'.format(value_err)
        elif init__ki == ' ' or str(sentence__k[i]) == '' or str(sentence__k[i]) == '\n':
            path = chars_path + 'Set_1\\blank1.jpg'
        else:
            path = chars_path + 'Set_1\\blank1.jpg'
            for pair in char__lst:
                if init__ki == pair[0]:
                    path = my_path.format(pair[1])
                    break

        print(path)


        img2 = cv2.imread(path)
        try:
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        except:
            print(path)
        black_low = np.array([0, 0, 0])
        black_high = np.array([50, 50, 50])
        mask = cv2.inRange(hsv, black_low, black_high)
        color_shade = random.randint(0, 100)
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
        im_pil = PIL.Image.fromarray(border)
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
        path = 'D:/handwriter/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
        print(path)
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (40, 114))
        img_np = np.array(img)
        final_img = img_np
        for i in range(1, N__k):
            path = 'D:/handwriter/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank' +str(1)+ '.jpg'
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
                    X=random.randint(1,2)
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

path='D:/handwriter/TheHandwriter/Handwritten_Digits/FINAL_RESULToutput.jpg'
cv2.imwrite(path, border)