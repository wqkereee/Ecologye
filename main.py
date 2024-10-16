import discord
import random
import os
import requests

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np


from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

def get_class(image_path):

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    return class_name[2:]





@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error ({error})')

@bot.command()
async def nowhelp (ctx):
    await ctx.send("Сократите потребление пластика, используя многоразовые пакеты и выбирая продукты в экологичной упаковке. Сортируйте вторсырьё и участвуйте в экологических движениях, чтобы помочь сохранить природу. Также старайтесь меньше пользоваться личным авто и выбирайте пешие прогулки или общественный транспорт.")

@bot.command()
async def randomhelp(ctx):
    list = ["Убрать мусор у себя в комноте", "Помочь эко активистам"]
    await ctx.send(f"{random.choice(list)}")

@bot.command()
async def infoimg(ctx):
    await ctx.send(f'wait...')
    for i in ctx.message.attachments:
        await i.save('uploaded_image.png')
        await ctx.send(f"Trash:  {get_class('uploaded_image.png')}")
        result = get_class("uploaded_image.png").strip()
        if result == "Paper":
            await ctx.send("Это бумажное загрязнения")
        elif result == "Plastik":
            await ctx.send("Это пластиковое загрязнения")
        elif result == "Oil":
            await ctx.send("Это нефтяное загрязнения")
        elif result == "Glass":
            await ctx.send("Это стекляное загрязнения")
        await ctx.send(result)

@bot.command()
async def Papertrash(ctx):
    await ctx.send("Бумажные загрязнения: Сокращение использования бумаги и переход на цифровые форматы помогут уменьшить объем бумажных отходов, а переработка бумаги позволяет сохранить деревья и ресурсы.")
    
@bot.command()
async def Oiltrash(ctx):
    await ctx.send("Нефтяные загрязнения: Для снижения нефтяных загрязнений необходимо развивать альтернативные источники энергии, такие как солнечная и ветровая, а также улучшать технологии очистки воды от нефтепродуктов.")

@bot.command()
async def Glasstrash(ctx):
    await ctx.send("Стеклянные загрязнения: Стеклянные бутылки и упаковка могут быть переработаны бесконечно, поэтому важно сдавать их в специальные пункты сбора для повторного использования.")

@bot.command()
async def Plastiktrash(ctx):
    await ctx.send("Пластиковые загрязнения: Для борьбы с пластиковыми отходами важно использовать многоразовые сумки и контейнеры, а также поддерживать инициативы по переработке пластика.")

@bot.command()
async def Nowhelpeco(ctx):
    await ctx.send("Чтобы помочь экологии, можно сократить использование пластика, переходя на многоразовые изделия, а также активно участвовать в переработке отходов и поддерживать инициативы по охране окружающей среды. Кроме того, стоит выбирать экологически чистые продукты и сокращать потребление энергии.")

@bot.command()
async def Globalwarming(ctx):
    await ctx.send("Справиться с глобальным потеплением можно, уменьшая выбросы парниковых газов через переход на возобновляемые источники энергии, улучшение энергоэффективности и внедрение устойчивых практик в сельском хозяйстве и транспорте. Также важно поддерживать лесовосстановление и другие природные решения для поглощения углерода.")

@bot.command()
async def papertrash(ctx):
    await ctx.send("Бумажные загрязнения: Сокращение использования бумаги и переход на цифровые форматы помогут уменьшить объем бумажных отходов, а переработка бумаги позволяет сохранить деревья и ресурсы.")
    
@bot.command()
async def oiltrash(ctx):
    await ctx.send("Нефтяные загрязнения: Для снижения нефтяных загрязнений необходимо развивать альтернативные источники энергии, такие как солнечная и ветровая, а также улучшать технологии очистки воды от нефтепродуктов.")

@bot.command()
async def glasstrash(ctx):
    await ctx.send("Стеклянные загрязнения: Стеклянные бутылки и упаковка могут быть переработаны бесконечно, поэтому важно сдавать их в специальные пункты сбора для повторного использования.")

@bot.command()
async def plastiktrash(ctx):
    await ctx.send("Пластиковые загрязнения: Для борьбы с пластиковыми отходами важно использовать многоразовые сумки и контейнеры, а также поддерживать инициативы по переработке пластика.")

@bot.command()
async def nowhelpeco(ctx):
    await ctx.send("Чтобы помочь экологии, можно сократить использование пластика, переходя на многоразовые изделия, а также активно участвовать в переработке отходов и поддерживать инициативы по охране окружающей среды. Кроме того, стоит выбирать экологически чистые продукты и сокращать потребление энергии.")

@bot.command()
async def globalwarming(ctx):
    await ctx.send("Справиться с глобальным потеплением можно, уменьшая выбросы парниковых газов через переход на возобновляемые источники энергии, улучшение энергоэффективности и внедрение устойчивых практик в сельском хозяйстве и транспорте. Также важно поддерживать лесовосстановление и другие природные решения для поглощения углерода.")



