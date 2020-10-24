import csv
import random
from fuzzywuzzy import process
from db_parser import gen_dict

sorry_messages = ["So its related to {}, any more information?",
                  "Ah yes, {}, whats wrong with it?",
                  "{}... whats the problem?",
                  "Okay so {}, what about it",
                  "So its the {}, tell me more"]


db_dict = gen_dict('./db/')


##############################
class ChatBot:
    # best match minimum threshold
    MATCH_CONFIDENCE_THRESHOLD = 50
    RETRY_LIMIT = 2

    # problems and solutions
    """
    base_layer = {
        'EDM': {'thing go brr': {'F': ["If F, then undie"]},
                'no powa': ["Also F"]
                },
        "CNC": {}
    }
    """

    base_layer = db_dict


    layer = base_layer  # which layer of the nested dict we are atm
    topic = ""
    troubleshooting = False
    retry_counter = 0  # Count attempts to provide automatic help
    current_advice_index = -1  # Index within deepest layer list

    # def __init__(self):

    #   this two to be substituted by discord bot
    async def stub_input(self, msg):
        if not self.troubleshooting:
            print("Not troubleshooting")
            match = process.extractOne(msg, self.layer.keys())
            subcat = match[0]
            confidence = match[1]

            if confidence < self.MATCH_CONFIDENCE_THRESHOLD:
                print("Low confidence")
                await self.stub_output("Sorry, didnt get that.")
                self.retry_counter += 1

                if self.retry_counter > self.RETRY_LIMIT:
                    print("Too many tries")
                    await self.print_help(self.layer)

                return
            print("Reset retries")

            self.retry_counter = 0
            self.layer = self.layer[subcat]

            if not isinstance(self.layer, dict):
                self.troubleshooting = True
                await self.stub_output("Hmm.. lets try a few things")
            else:
                await self.stub_output(random.choice(sorry_messages).format(subcat))

        else:  # provide troubleshooting help
            print("Troubleshooting")
            if msg == "yes":
                await self.stub_output("Bye!")
                await self.reset()
                return
            # print("i=")
            self.current_advice_index += 1
            if self.current_advice_index <= len(self.layer):  # Double check whether it should be < or <=
                await self.stub_output(self.layer[self.current_advice_index])
                await self.stub_output("Did that work?")

    # discord bot should implement exit functionality and input validations
    async def stub_output(self, msg):
        print(msg)

    async def print_help(self, layer):
        problems = ', '.join(list(layer.keys()))
        await self.stub_output("Is it related to this? {}...".format(problems))

    async def reset(self):
        return
