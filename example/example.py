from flask import Flask
from flask import request

import sys
import os
sys.path.append("..")

from fbmsgbot.bot import Bot
from fbmsgbot.models.message import Message
from fbmsgbot.models.template import Template
from fbmsgbot.models.attachment import Button, Element

from fbmsgbot.models.receipt import ReceiptElement

import json

app = Flask(__name__)
bot = Bot(os.environ['PYBOT_TOKEN'])

def set_welcome():
    response, error = bot.set_welcome("Welcome to PyBot!")
    print response
    print error


@app.route('/', methods=['GET', 'POST'])
def webhook():
    # For webhook verification when registering app 
    if request.args.get("hub.verify_token") == 'test_token':
        return request.args.get("hub.challenge")

    # Recieve a list of available messages
    msgs = bot.messages_for_request(request)
    
    for m in msgs:
        text = m.text # Retrieve what user sent
        recipient = m.sender # Retrieve who sent it
         
        if m.text == 'template':

            web_button = Button(
                type='web_url',
                title='My Button Image',
                payload='http://www.newton.ac.uk/files/covers/968361.jpg'
            )

            postback_button = Button(
                type='postback',
                title='My Postback',
                payload="<USER DEFINED PAYLOAD>",
            )
            
            element = Element(
                title='Generic Template Element Title',
                subtitle='My subtitle',
                image_url='http://www.buffettworld.com/images/news_trump.jpg',
                buttons=[
                    web_button,
                ]
            )
            
            generic_template = Template(
                Template.generic_type,
                elements=[
                    element,                    
                ]
            )

            button_template = Template(
                Template.button_type,
                title="My Button template title",
                buttons=[
                    web_button, postback_button
                ]
            )

            msg = Message('template', button_template)
            response, error = bot.send_message(msg, recipient)

            msg2 = Message('template', generic_template)
            response, error = bot.send_message(msg2, recipient)

        
        elif m.text == 'receipt':
            element = ReceiptElement(
                title='My Title',
                subtitle='A very good subtitle',
                quantity='15',
                price=1999,
                currency='CAD',
                image_url='http://www.newton.ac.uk/files/covers/968361.jpg'
            )

            receipt = Template(Template.receipt_type,
                recipient_name= 'A name',
                order_number='12345678902',
                currency='CAD',
                payment_method='Visa',
                order_url='http://petersapparel.com/order?order_id=123456',
                elements=[element],
                address={
                    'street_1': '1 Hacker Way',
                    'city': 'Vancouver',
                    'state': 'BC',
                    'country': 'CA',
                    'postal_code': '1A1A1A'

                },
                summary={
                    'subtotal': 75.00,
                    'shipping_cost': 4.95,
                    'total_tax': 6.19,
                    'total_cost': 56.14
                }
            )

            msg = Message('template', receipt)
            response, error = bot.send_message(msg, recipient)

        else: 
            # Echo back to user
            # Send regular 'text' message
            payload = text
            msg = Message('text', payload)
            bot.send_message(msg, recipient)

    return 'OK'

if __name__ == "__main__":
    app.debug = True
    set_welcome()
    app.run(port=8000)
