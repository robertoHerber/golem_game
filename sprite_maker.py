from PIL import Image
import os

def split_image_into_sprites(input_image, output_folder="sprites"):
    img = Image.open(input_image)  # Abre a imagem
    os.makedirs(output_folder, exist_ok=True)  # Cria a pasta

    # Divide a imagem em sprites de 24x24
    for y in range(0, img.height, 24):
        for x in range(0, img.width, 24):
            sprite = img.crop((x, y, x + 24, y + 24))  # Recorta um quadrado 24x24
            sprite.save(f"{output_folder}/sprite_{x}_{y}.png")  # Salva como PNG

if __name__ == "__main__":
    split_image_into_sprites("image.png")  # Substitua pelo seu arquivo