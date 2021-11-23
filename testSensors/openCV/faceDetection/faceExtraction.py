from os import read
from PIL import Image, ImageDraw
import face_recognition as fr

borderColor = (255,0,0)

# Load the jpg file into a numpy array
image = fr.load_image_file("/home/pi32/Git/EE4201/Face_Recog/Face_Images/Michael/01.jpg")

face_locations = fr.face_locations(image)

print( "I found {} face(s) in this photograph.".format( len(face_locations) ) )

pil_image   = Image.fromarray(image)
draw        = ImageDraw.Draw(pil_image)


for face_location in face_locations:
    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print( "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format( top, left, bottom, right ) )

    draw.rectangle( ((left, top), (right, bottom)), outline = borderColor )

pil_image.show()