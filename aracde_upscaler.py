#============================================
# Hermanns Retro Arcade Sprite Upscaler x4/x8
# (ccc) 2026 v0.1a 28.9.2026
#============================================


import os
os.system("cls")
print("importing libs....")


#==========================================
# init
#==========================================

dir_path = os.path.dirname(os.path.realpath(__file__))


from blocksize import find_block_size
from reduce import process
from hqx import upscale_hqx

from esrgan_x4 import ESRGANUpscaler
from esrgan_x8_chain import upscale_8x_chaining
from smooth import smooth_edges_gaussian, smooth_edges_median


from datetime import datetime
from random import randrange



# === Main Loop====
while True:

    #==========================================
    # Input Files
    #==========================================

    os.system("cls")
    print("Aracde Sprite/PixelArt Upscaler x4/x8")
    print("\n\n")


    inp=input("Image > ")
    inp=inp.replace('"',"")

    file=inp


    #==============================================
    # Get largest Block Size (Pixel Blocks)
    #==============================================


    print("Get Block Size")
    block_size = find_block_size(file)
    print(f"Die automatisch ermittelte Blockgröße ist: {block_size}x{block_size} Pixel")


    #==============================================
    # get Real Image Size 1x1
    #==============================================

    print("Get Lores reduced image")
    # Ergebnis speichern oder in Python Arcade nutzen
    lo_sprite = process(file, block_size=block_size)

    file=dir_path + "/" "temp_sprite_lores.png"
    lo_sprite.save(file)
    #lo_sprite.show()

    #==============================================
    # x4 /x8 Upscaling
    #==============================================

    choice=input("4x or 8x Upscaling> (4/8) ")
    if choice=="" or choice==None:
        choice=4
    else:
        choice=int(choice)

    if choice==4:

        # Upscale ESRGAN x4
        model_path = dir_path + "/" + "RRDB_ESRGAN_x4.pth"
        upscaler = ESRGANUpscaler(model_path=model_path)

        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")
        file_out=dir_path +"/" + "upscaled_" + dt_string +".png"
    
        upscaler.upscale_image(
            input_path=file, 
            output_path=file_out
        )

    else:

        # Upscale ESRGAN x8 Chaining 4x4
        model_path = dir_path + "/" + "RRDB_ESRGAN_x4.pth"
    
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")
        file_out=dir_path +"/" + "upscaled_" + dt_string +".png"
    
        upscale_8x_chaining(input_path=file, output_path=file_out, model_path=model_path)

    #=====================================================
    # Smooth hard Edges a little bit
    #=====================================================

    # Smooth Soft Edges Scaling

    #=====================================================
    # Gaussian Smooth (not used)
    #=====================================================
    #img=smooth_edges_gaussian(file_out, radius=1.0)


    #=====================================================
    # Median Smooth
    #=====================================================
    img=smooth_edges_median(file_out, size=3)


    #=====================================================
    # Save Results
    #=====================================================

    # Save Image Smoothed
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    file_out_new = dir_path +"/" + "upscaled_new_" + dt_string +".png"
    img.save(file_out_new)
    img.show()

    #=====================================================
    # Done!
    #=====================================================
    print("Upscaling erfolgreich abgeschlossen!")
    input("wait key")








