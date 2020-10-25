import random

from fuzzywuzzy import process

from db_parser import gen_dict

sorry_messages = ["So its related to {}, any more information?",
                  "Ah yes, {}, whats wrong with it?",
                  "{}... whats the problem?",
                  "Okay so {}, what about it",
                  "So its the {}, tell me more"]


##############################
class ChatBot:
    # problems and solutions
    """
    base_layer = {
        'EDM': {'thing go brr': {'F': ["If F, then undie"]},
                'no powa': ["Also F"]
                },
        "CNC": {}
    }
    """

    def __init__(self):
        # best match minimum threshold
        self.MATCH_CONFIDENCE_THRESHOLD = 64
        self.RETRY_LIMIT = 2
        self.db_dict = gen_dict('./db/')
        self.base_layer = self.db_dict
        self.layer = self.base_layer  # which layer of the nested dict we are atm
        self.topic = ""
        self.troubleshooting = False
        self.retry_counter = 0  # Count attempts to provide automatic help
        self.current_advice_index = -1  # Index within deepest layer list

    #   this two to be substituted by discord bot
    async def stub_input(self, msg):
        if not self.troubleshooting:
            confidence = 100
            prevcat = ""
            looping = False
            while confidence >= self.MATCH_CONFIDENCE_THRESHOLD:
                match = process.extract(msg, self.layer.keys())
                subcat = match[0][0]
                confidence = match[0][1]
                confidence_difference = match[0][1] - match[1][1]
                print("Not troubleshooting: {}".format(subcat))

                if confidence < self.MATCH_CONFIDENCE_THRESHOLD:
                    print("Low confidence {}".format(confidence))
                    if not looping:
                        await self.stub_output("Sorry, didnt get that.")
                    self.retry_counter += 1

                    if self.retry_counter > self.RETRY_LIMIT:
                        print("Too many tries")
                        await self.print_help(self.layer)
                    return
                print("{} Reset retries, confidence {}".format(subcat, confidence))

                if confidence_difference < 5:
                    print("Confidence difference only {}, asking user".format(confidence_difference))
                    await self.stub_output(random.choice(sorry_messages).format(prevcat))
                    return

                self.retry_counter = 0
                self.layer = self.layer[subcat]

                if not isinstance(self.layer, dict):
                    self.troubleshooting = True
                    print(subcat)
                    await self.stub_output("Hmm.. lets try a few things")
                    return
                elif not looping:
                    await self.stub_output(random.choice(sorry_messages).format(subcat))
                    prevcat = subcat
                looping = True

        else:  # provide troubleshooting help
            print("Troubleshooting")
            if msg == "yes":
                await self.stub_output("", img_name="happy.gif")
                await self.stub_output("Bye!")
                await self.reset()
                return

            self.current_advice_index += 1
            if self.current_advice_index < len(self.layer):
                await self.stub_output(self.layer[self.current_advice_index])
                await self.stub_output("Did that work?")
            else:
                await self.stub_output("", img_name="sad.gif")
                await self.stub_output("Sorry I'm not too sure how to help :( Try speaking to a human.")

    # discord bot should implement exit functionality and input validations
    async def stub_output(self, msg, img_name=None):
        print(msg)

    async def print_help(self, layer):
        await self.stub_output("", img_name="confused.gif")
        problems = ', '.join(list(layer.keys()))
        await self.stub_output("It's ok we all get confused sometimes!")
        await self.stub_output("Is it related to this? {}...".format(problems))

    async def reset(self):
        return
