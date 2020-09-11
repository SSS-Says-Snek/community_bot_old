import discord
from discord.ext import commands
import speech_recognition as sr
import time
import random


class ExtraFunCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='COMING SOON!', brief='- DMS a list of all BFB characters')
    async def bfbcharacters(self, ctx):
        """- DMs a list of all BFB characters"""
        # await ctx.message.author.send('**`list of all BFB Characters`**')
        # await ctx.message.author.send('**`')
        await ctx.send('Sorry! Work in Progress! We\'ll notify you when we fix it!')
        brandon = self.bot.get_user(683852333293109269)
        await brandon.send(f"**`WARNING 003:` {ctx.author.name} has used an INCOMPLETE command. Uh Oh!")

    @commands.command(help='COMING SOON!', brief='- Plays a Guessing Game with your microphone!')
    async def speech_recog_guess(self, ctx):
        async def recognize_speech_from_mic(recognizer, microphone):
            """Transcribe speech from recorded from `microphone`.

                Returns a dictionary with three keys:
                "success": a boolean indicating whether or not the API request was successful

                "error": `None` if no error occured, otherwise a string containing
                        an error message if the API could not be reached or
                        speech was unrecognizable
                "transcription": `None` if speech could not be ttranscribed,
                        otherwise a string containing the transcribed text
                """

            # this will check that Recognizer and Microphone are appropriate types
            if not isinstance(recognizer, sr.Recognizer):
                await ctx.send('**`PYTHONERROR 1431:`** **recognizer** must be **RECOGNIZER** instance')
            if not isinstance(microphone, sr.Microphone):
                await ctx.send('**`PYTHONERROR 1431:`** **microphone** must be **MICROPHONE** instance')

            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            response = {
                "success": True,
                "error": None,
                "transcription": None,
            }

            try:
                response["transcription"] = recognizer.recognize_google(audio)
            except sr.RequestError:
                # API says No U or become offline
                response["success"] = False
                response["error"] = "API unavailable"
            except sr.UnknownValueError:
                # Yur speech so bad that speech recognization gave up
                response["error"] = "Unable to recognize speech"

            return response

        WORDS = ['apple', 'banana', 'grape', 'orange', 'mango', 'lemon', 'delicious', 'apartment', 'cheese', 'ketchup',
                 'dinosaur', 'python']
        NUM_GUESSES = 6
        PROMPT_LIMIT = 5

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        word = random.choice(WORDS)

        instructions = (
            f"I'm thinking of one of these words: \n"
            f"{WORDS}\n"
            f"You have {NUM_GUESSES} tries to guess which one.\n"
        )

        await ctx.send(instructions)
        time.sleep(3)

        for i in range(NUM_GUESSES):
            # get guess from youser
            # if transcription is return, break loop and continue
            # if no transcription and API says No U, break and continue
            # if API request succeed but no transcription,
            # reprompt user to say guess again. Do this up to PROMPT_LIMIT times
            for j in range(PROMPT_LIMIT):
                await ctx.send(f"Guess {i + 1}. Speak!")
                guess = await recognize_speech_from_mic(recognizer, microphone)
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                await ctx.send("I didn't catch that. What did you say?\n")

            if guess["error"]:
                await ctx.send("**`ERROR ???:`** {}".format(guess["error"]))
                break

            await ctx.send("You said: {}".format(guess["transcription"]))

            guess_is_correct = guess["transcription"].lower() == word.lower()
            user_has_more_attempts = i < NUM_GUESSES - 1

            if guess_is_correct:
                await ctx.send("**`CORRECT!!`** You win!".format(word))
                break
            elif user_has_more_attempts:
                await ctx.send("**`Incorrect.`** Try again.\n")
            else:
                await ctx.send(f"Sorry, you ***_`lose!`_***\nI was thinking of {word}")
                break


def setup(bot):
    bot.add_cog(ExtraFunCommands(bot))