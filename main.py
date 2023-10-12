import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = [
    'infeliz', 'bajon', 'garron', 'deprimido', 'deprimda', 'triste',
    'complicado', 'complicada', 'miserable', 'deprimente', 'dificil',
    'no tengo grupo', 'estoy solo', 'estoy sola', 'estoy quemado',
    'estoy quemada', 'basura', 'no me sale', 'deprimo', 'sad', 'triste',
    'deprimente', 'manija', 'morir', 'matar', 'estupido', 'estupida'
]

estimulos_iniciales = [
    "Confía en tus capacidades.", "Tu esfuerzo vale la pena.",
    "Si te cansas, aprende a descansar, no a renunciar.",
    "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "Si no estas fallando, no estas innovando lo suficiente.",
    "Vamos a encontrar una manera, o crear una manera de llegar allí.",
    "Sos una gran persona / bot!",
    "Hay una fuerza motriz mas poderosa que el valor, la electricidad y la energia atómica, la voluntad.",
    "Para hacer una tarta de manzana, primero tienes que crear el universo.",
    "En la ciencia la única verdad sagrada es que no hay verdades absolutas.",
    "Un organismo que este en guerra contra el mismo está condenado.",
    "No es lo que te ocurre, sino cómo reaccionas lo que importa.",
    "Cuanto mas grande la dificultad, mas gloria hay en superarla",
    "Tener exito no es aleatorio. Es una variable dependiente del esfuerzo.",
    "La energía de la mente es la esencia de la vida.",
    "Las buenas acciones nos fortalecen e inspiran buenas acciones en los demás.",
    "Cuanto más duro el conflicto, más glorioso el triunfo. Dijo el Tomas Paine"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return (quote)


def update_estimulos(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have loged in as {0.user} '.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!motive'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = estimulos_iniciales
        if "encouragements" in db.keys():
            options += db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_estimulos(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("del", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.startswith('$responding'):
        value = msg.split('$responding ', 1)[1]

        if value.lower() == 'true':
            db['responding'] = True
            await message.channel.send('Responding is on.')
        else:
            db['responding'] = False
            await message.channel.send('Responding is off.')


keep_alive()
client.run(os.getenv('Token'))
my_secret = os.environ['Token']
