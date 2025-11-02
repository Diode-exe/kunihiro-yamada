source = "token.txt"
try:
    with open(source, "r") as tf:
        tf_token = tf.read()
except FileNotFoundError:
    print(f"[WARN] {source} not found!")
    print("You need a file called source.txt with a valid Discord token")
    input("Press Enter to continue...")

channel = "channel.txt"
try:
    with open(channel, "r") as ch:
        ch_channel = ch.read()
except FileNotFoundError:
    print(f"[WARN] {channel} not found!")
    print("You need a file called channel.txt with a valid Discord channel ID")
    input("Press Enter to continue...")
