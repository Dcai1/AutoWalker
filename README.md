# Auto Holder

### Or More Specifically, An Auto KeyBoard Holder.

**This is a simple program that holds a key when a key is pressed.**

<img src="https://images.steamusercontent.com/ugc/9224282649912961670/9C9CBA18A17C349E040011D8CCA309FF5F284E88/" alt="Auto Keyboard Holder Image">

## Features:

- **Holds** a key when a toggle key is pressed.
- **Releases** that key when that toggle key is released.
- The held key is **rebindable**.
- Did I mention the **toggle key** is also rebindable?
- A **simple**, minimalistic GUI for easy rebinds.
- **State** updates to let you know if the program is running or not.

**IMPORTANT!** This may not work inside all games or apps. This is because these games may read raw keyboard input! If you are having issues, try running this application as **Administrator** to give it the necessary permissions.

## What’s under the hood

- Built with **Python**.
- GUI made with **PySide6**.
- Global keyboard listening and synthetic key presses handled by **pynput**.

## How it works (developer edition)

_If you don't want to see this, simply scroll down to the next section._

- `main.py` launches the app and hands a `KeyHolder` to the window.
- `holder.py` keeps track of:
  - the current **hold key**
  - the current **toggle key**
  - whether the app is currently **running**
- Press the toggle key once to start holding the chosen key, press it again to stop.
- While running, pressing the held key itself will also stop the holding state and release it.

## Minor Notes

- The UI is intentionally minimal because the goal is one thing: hold a key for you.
- It will happily listen for keybind changes and keep your hold/toggle keys separate.
- If the key-bind combo is weird, the app will refuse to let you bind the same key for both hold and toggle.

## Why I Built This (Warning: A Mini Story)

I wanted to make something that would make it easier to hold a key for you.

Alright, fine, you got me. I actually built this because I was tired of holding the same key down in a game.

Specifically, in a game called **Where Winds Meet**. There is this storyline that was interesting, but the gameplay only consisted of walking. It was an absolute walking simulator, and as if that wasn't bad enough already, they made it worse by modifying my walkspeed to be somehow slower than a snail!

And so, fed up with my snail-like walkspeed, I built this little app to make it easier for me. I hope it helps others too!
