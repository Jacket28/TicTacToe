import discord
from discord.ext import commands
import random

import json

with open('./config.json') as cjson:
    config = json.load(cjson)

client = commands.Bot(command_prefix="!")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if ctx.author != p2:
        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = ctx.author
            player2 = p2

            # print the board
            await ctx.send("[PARTIE DE " + "<@" + str(player1.id) + ">" + " ET " + "<@" + str(player2.id) + ">]")
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("Réveille-toi <@" + str(player1.id) + "> , tu dois jouer.")

                def check(message):
                    """Checks if the message author is the same as the one that invoked the
                    command, and if the user chose a valid option"""
                    return message.content.lower() in ['stoptictactoe']

                message = await client.wait_for('message', check=check)

                if message.content == "stoptictactoe":
                    await ctx.send(
                        "[PARTIE DE " + "<@" + str(player1.id) + ">" + " ET " + "<@" + str(player2.id) + "> TERMINEE]")
                    gameOver = True

            elif num == 2:
                turn = player2
                await ctx.send("Réveille-toi <@" + str(player2.id) + "> , tu dois jouer.")

                def check(message):
                    """Checks if the message author is the same as the one that invoked the
                    command, and if the user chose a valid option"""
                    return message.content.lower() in ['stoptictactoe']

                message = await client.wait_for('message', check=check)

                if message.content == "stoptictactoe":
                    await ctx.send(
                        "[PARTIE DE " + "<@" + str(player1.id) + ">" + " ET " + "<@" + str(player2.id) + "> TERMINEE]")
                    gameOver = True
        else:
            await ctx.send("Tu joues déjà une partie, termine-là !")
    else:
        await ctx.send("T'es sérieux ? T'as essayé de jouer avec toi-même ?")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                await ctx.send("[PARTIE DE " + "<@" + str(player1.id) + ">" + " ET " + "<@" + str(player2.id) + ">]")
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)

                if gameOver == True:
                    if turn == player1:
                        await ctx.send("<@" + str(player1.id) + ">" + "a gagné!")
                    else:
                        await ctx.send("<@" + str(player2.id) + ">" + "a gagné!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Ah bah Egalité ! Vous êtes tous les deux nuls ou tous les deux bons (question de "
                                   "point de vue,hein)")

                # switch turns
                if gameOver == False:
                    if turn == player1:
                        turn = player2
                        await ctx.send("A toi de jouer " + "<@" + str(player2.id) + ">")
                    elif turn == player2:
                        turn = player1
                        await ctx.send("A toi de jouer " + "<@" + str(player1.id) + ">")
            else:
                await ctx.send("Erreur ! Choisis un CHIFFRE entre 1 et 9 compris ainsi qu'une case vide")
        else:
            await ctx.send("Tcheu ! C'est pas ton tour !")
    else:
        await ctx.send("C'était cool ! Refaites une partie avec la commande !tictactoe")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Bougre d'âne ! Tu vas pas jouer tout seul, trouve un partenaire !")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Mentionne correctement quelqu'un ! (exemple : @Jacket)")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Et je suis censé deviner dans quelle case tu veux jouer ?")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("T'as pas écrit un chiffre ! Recommence...")

client.run(config["token"])
