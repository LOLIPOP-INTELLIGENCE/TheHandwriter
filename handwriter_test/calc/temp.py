
def generate_word(img_prev, word__k, k,N___K,K___K,add_blank):
    #Random Set of Letters
    value = randint(2,3)
    #Random Error
    value_err = randint(1,11)

    #Retrieving path of revelant character
    sentence__k = list(word__k)
    str_k       = str_k

    base_path = 'D:/TheHandwriter/Handwritten_Digits/Set_'
    base_path_set = base_path + str( value ) + '/{}.jpg'

    if str_k.islower() or str_k.isdigit() or str_k.isupper():
        path__k = base_path_set + ( sentence__k[0] * ( int( str_k.isupper() ) + 1 ) ) + '.jpg'
    elif(str_k=='.'):
        path__k = base_path_set.format( 'dot' )
    elif (str_k == ','):
        path__k = base_path_set.format( 'comma' )
    elif (str_k == '"'):
        path__k = base_path_set.format( 'quote' )
    elif (str_k == '\''):
        path__k = base_path_set.format( 'Squote' )
    elif (str_k == '!'):
        path__k = base_path_set.format( '!' )
    elif (str_k == '-'):
        path__k = base_path_set.format( '-' )
    elif (str_k == '%'):
        path__k = base_path_set.format( '%' )
    elif (str_k == '|'):
        path__k = base_path_set.format( '|')
    elif (str_k == '\\'):
        path__k = base_path_set.format( 'back' )
    elif (str_k == '='):
        path__k = base_path_set.format( '=' )
    elif (str_k == '('):
        path__k = base_path_set.format( '(' )
    elif (str_k == ')'):
        path__k = base_path_set.format( ')' )
    elif (str_k == '*'):
        path__k = base_path_set.format( '*' )
    elif (str_k == '_'):
        path__k = base_path_set.format( '_' )
    elif (str_k == '/'):
        path__k = base_path_set.format( '/' )
    elif (str_k == ':'):
        path__k = base_path_set.format( 'colon' )
    elif (str_k == '>'):
        path__k = base_path_set.format( '>' )
    elif (str_k == '<'):
        path__k = base_path_set.format( '<' )
    elif (str_k == '?'):
        path__k = base_path_set.format( '?' )
    elif (str_k == '}'):
        path__k = base_path_set.format( '}' )
    elif (str_k == '{'):
        path__k = base_path_set.format( '{' )
    elif (str_k == ';'):
        path__k = base_path_set.format( ';' )
    elif (str_k == '+'):
        path__k = base_path_set.format( '+' )
    elif (str_k == '&'):
        path__k = base_path_set.format( '&' )
    elif (str_k == '['):
        path__k = base_path_set.format( '[' )
    elif (str_k == ']'):
        path__k = base_path_set.format( ']' )
    elif (str_k == '~'):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Errors/Error{}.jpg'.format( value_err )
    elif (str_k == ' ' or str_k == '\n' or str_k == ''):
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_1/blank2.jpg'
    else:
        path__k = 'D:/TheHandwriter/Handwritten_Digits/Set_1/blank1.jpg'

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

        str__ki = str( sentence__k[i] )

        if (str__ki.islower()):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + '.jpg'
        elif (str__ki == '.'):
            path = base_path_set.format() + 'dot' + '.jpg'
        elif (str__ki == ','):
            path = base_path_set.format() + 'comma' + '.jpg'
        elif (str__ki == '\"'):
            path = base_path_set.format() + 'quote' + '.jpg'
        elif (str__ki == '\''):
            path = base_path_set.format() + 'Squote' + '.jpg'
        elif (str__ki == ' ' or str__ki == '' or str__ki == '\n'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_1/' + 'blank1' + '.jpg'
        elif (str__ki == '~'):
            path = 'D:/TheHandwriter/Handwritten_Digits/Errors/' + 'Error' +str(value_err)+'.jpg'
        elif (str__ki.isdigit()):
            path = base_path_set + sentence__k[i] + '.jpg'
        elif(str__ki.isupper()):
            path = 'D:/TheHandwriter/Handwritten_Digits/Set_'+str(value)+'/' + sentence__k[i] + sentence__k[i] + '.jpg'

        elif (str__ki == '!'):
            path = base_path_set.format() + '!' + '.jpg'
        elif (str__ki == '-'):
            path = base_path_set.format() + '-' + '.jpg'
        elif (str__ki == '%'):
            path = base_path_set.format() + '%' + '.jpg'
        elif (str__ki == '|'):
            path = base_path_set.format() + '|' + '.jpg'
        elif (str__ki == '\\'):
            path = base_path_set.format() + 'back' + '.jpg'
        elif (str__ki == '='):
            path = base_path_set.format() + '=' + '.jpg'
        elif (str__ki == '('):
            path = base_path_set.format() + '(' + '.jpg'
        elif (str__ki == ')'):
            path = base_path_set.format() + ')' + '.jpg'
        elif (str__ki == '*'):
            path = base_path_set.format() + '*' + '.jpg'
        elif (str__ki == '_'):
            path = base_path_set.format() + '_' + '.jpg'
        elif (str__ki == '/'):
            path = base_path_set.format() + 'forward' + '.jpg'
        elif (str__ki == ':'):
            path = base_path_set.format() + 'colon' + '.jpg'
        elif (str__ki == '>'):
            path = base_path_set.format() + '>' + '.jpg'
        elif (str__ki == '<'):
            path = base_path_set.format() + '<' + '.jpg'
        elif (str__ki == '?'):
            path = base_path_set.format() + '?' + '.jpg'
        elif (str__ki == '}'):
            path = base_path_set.format() + '}' + '.jpg'
        elif (str__ki == '{'):
            path = base_path_set.format() + '{' + '.jpg'
        elif (str__ki == ';'):
            path = base_path_set.format() + ';' + '.jpg'
        elif (str__ki == '+'):
            path = base_path_set.format() + '+' + '.jpg'
        elif (str__ki == '&'):
            path = base_path_set.format() + '&' + '.jpg'
        elif (str__ki == '['):
            path = base_path_set.format() + '[' + '.jpg'
        elif (str__ki == ']'):
            path = base_path_set.format() + ']' + '.jpg'
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
