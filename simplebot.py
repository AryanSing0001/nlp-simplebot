import tkinter.scrolledtext as tks
from datetime import datetime
from tkinter import *
from openai import OpenAI
import threading

client = OpenAI()


# OpenAI bot response function
def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant chatbot."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message.content.strip()


# Create user's message
def create_and_insert_user_frame(user_input):
    userFrame = Frame(chatWindow, bg="#d0ffff")

    Label(
        userFrame,
        text=user_input,
        font=("Arial", 11),
        bg="#d0ffff",
        wraplength=350,
        justify=LEFT
    ).grid(row=0, column=0, padx=5, pady=2)

    Label(
        userFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 8),
        bg="#d0ffff"
    ).grid(row=1, column=0, padx=5, pady=2)

    chatWindow.insert("end", "\n ", "tag-right")
    chatWindow.window_create("end", window=userFrame)


# Create bot's message
def create_and_insert_bot_frame(bot_response):
    botFrame = Frame(chatWindow, bg="#ffffd0")

    Label(
        botFrame,
        text=bot_response,
        font=("Arial", 11),
        bg="#ffffd0",
        wraplength=350,
        justify=LEFT
    ).grid(row=0, column=0, padx=5, pady=2)

    Label(
        botFrame,
        text=datetime.now().strftime("%H:%M"),
        font=("Arial", 8),
        bg="#ffffd0"
    ).grid(row=1, column=0, padx=5, pady=2)

    chatWindow.insert("end", "\n ", "tag-left")
    chatWindow.window_create("end", window=botFrame)
    chatWindow.insert(END, "\n\n")


# Send function
def send(event=None):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0", "end-2c").strip()

    if not user_input:
        chatWindow.config(state=DISABLED)
        return

    # Show user's message immediately
    create_and_insert_user_frame(user_input)

    # Clear input box
    userEntryBox.delete("1.0", "end")
    chatWindow.see("end")

    # Show typing message
    typing_start = chatWindow.index("end-1c")
    create_and_insert_bot_frame("Bot is typing...")
    typing_end = chatWindow.index("end-1c")

    chatWindow.config(state=DISABLED)

    # Run OpenAI API in background
    def worker():
        try:
            bot_response = get_bot_response(user_input)
        except Exception as e:
            bot_response = "Something went wrong while generating a response."

        # Update GUI in main thread
        def update_ui():
            chatWindow.config(state=NORMAL)

            # Remove typing message
            chatWindow.delete(typing_start, typing_end)

            # Insert actual response
            create_and_insert_bot_frame(bot_response)

            chatWindow.config(state=DISABLED)
            chatWindow.see("end")

        baseWindow.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()


# Main window
baseWindow = Tk()
baseWindow.title("The Simple Bot")
baseWindow.geometry("500x250")


# Chat window
chatWindow = tks.ScrolledText(
    baseWindow,
    font="Arial",
    wrap=WORD
)

chatWindow.tag_configure("tag-left", justify="left")
chatWindow.tag_configure("tag-right", justify="right")
chatWindow.config(state=DISABLED)


# User input box
userEntryBox = Text(
    baseWindow,
    bd=1,
    bg="white",
    width=38,
    font="Arial"
)


# Send button
sendButton = Button(
    baseWindow,
    font=("Verdana", 12, "bold"),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg="#ffffff",
    command=send
)


# Press Enter to send
baseWindow.bind("<Return>", send)


# Position widgets
chatWindow.place(
    x=1,
    y=1,
    height=200,
    width=500
)

userEntryBox.place(
    x=3,
    y=202,
    height=27
)

sendButton.place(
    x=430,
    y=200
)


# Start application
baseWindow.mainloop()
