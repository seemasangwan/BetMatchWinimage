import cv2 # image loading ,displaying , manipulation and image filtering
import numpy as np # work with array
import os # we import so that we can get cuurent directory path
import pytesseract # read all image files and utilize in image to text 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from skimage.metrics import structural_similarity as ssim
## ssim assess the strcutral similarity between two images
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
## pil is used to deal with images
import re
## re : regular expression 
## specifies a set of strings that matches it
class Solution:
    def __init__(self):
        """
        # Initialize your data structures here
        """
        pass
    #  code start from here 

    # comapre_images function compare two images 
    def comapre_images(self,img1_path,img2_path):
        # load the images 
        image1=cv2.imread(img1_path)
        image2=cv2.imread(img2_path)
        # size of both image should be same so thats why resize 
        image1= cv2.resize(image1, (image2.shape[1], image2.shape[0]))
        # converting the image to grayscale
        gray_image1=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
        gray_image2=cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        # computing SSIM
        ssim_index=ssim(gray_image1,gray_image2)
        mse=np.mean((gray_image1-gray_image2)**2)
        return ssim_index,mse
    

    # find_total_win function  is used to extract win from image 
    def find_total_win(self,image_path):
        # Define custom config for Tesseract
         custom_config = r'-c tessedit_char_whitelist=0123456789'
        # Load the image
         image = Image.open(image_path)
        # Convert to grayscale
         image = image.convert('L')
        # Apply a minimum filter to remove noise
         image = image.filter(ImageFilter.MinFilter(3))
        # Perform OCR
         text = pytesseract.image_to_string(image, config=custom_config)
        # Define the regular expression pattern to extract the desired numbers
         pattern = r'\b\d{10,12}\b'  # This pattern matches numbers with 10 to 12 digits
         win_total=0
        # Find all matches in the text
         matches = re.findall(pattern, text)
        # Check and print specific matches if they exist
         if len(matches) > 0:
          win_total=int(matches[0])
         if len(matches) > 1:
          
          win_total=int(matches[1])
         return win_total
    


    # find_bet_amount function is used to extract bet_amount from image
    def find_bet_amount(self,image_path):
        ## Load the image
        image = Image.open(image_path)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Increase contrast (adjust the factor as needed)

        text=pytesseract.image_to_string(image,lang='eng')
        #pattern= r'\d{1,3}(?:,\d{3})*'
        pattern=r'\b\d{1,3}(?:,\d{3}){2,}\b'
        matches=re.findall(pattern,text)
        res=0
        if matches:
            number_str=matches[0].replace(',','')
            try:
               number=int(number_str)
               res=number
               
            except ValueError:
              print("Not find bet amount")
        return res
    

    ## d=get_image_path is used to get path of an image
    def get_image_path(self,problem_set,image_name):
        return os.path.join("Problems",problem_set,image_name)
   
    def get_answer(self, problem):
        """
        # Problem contains the name of the set to solve. You can use this to retrieve the images from the set.
        # The result should be an array of length 2 with elements of type number (integer / float)

        # YOU SHOULD WRITE YOUR CODE HERE.
        """
         #if problem not in ['Set 8', 'Set 9']:
         #   print("Solve Sets 1 to 7 here.")
        if problem.startswith('Set') and problem not in ['Set8','Set9']:
            image_path=self.get_image_path(problem,"Image.png")
            test1_path=self.get_image_path(problem,"Test1.png")
            test2_path=self.get_image_path(problem,"Test2.png")
            ssim1,mse1=self.comapre_images(image_path,test1_path)
            ssim2,mse2=self.comapre_images(image_path,test2_path)
            return [round(float(ssim1)*100,3),round(float(ssim2)*100,3)]
        # if problem is Set8
        #   print("Solve Sets 8 here.")
        elif problem=='Set8':
           test1_path=self.get_image_path(problem,"Test1.png")
           test2_path=self.get_image_path(problem,"Test2.png")

           win_amount_test1=self.find_total_win(test1_path)
           win_amount_test2=self.find_total_win(test2_path)
           return[win_amount_test1,win_amount_test2]
        # if problem is Set9
        #   print("Solve Sets 9 here.")
        elif problem=="Set9":
            test1_path = self.get_image_path(problem, "Test1.png")
            test2_path = self.get_image_path(problem, "Test2.png")
            bet_amount_test1 = self.find_bet_amount(test1_path)
            bet_amount_test2 = self.find_bet_amount(test2_path)
            return [bet_amount_test1, bet_amount_test2]
        ## else 
        ## return [0,0]
        else:
            print("Problem set not recognized.")
            return [0, 0]
