#!/usr/bin/env python3

import os, ctypes

keys = [
    (759, "IJi2eDlOtrAHECKS"),
    (265, "vXEdCHzpOhVoIUF3"),
    (35, "emMbC1RD8tyUwIhG"),
    (648, "klUySQEsxv3t6Jj2"),
    (802, "UdKjhzi8p436wY5I"),
    (708, "du4o92H0zTP7GaMv"),
    (382, "NL4eoIH2pbylRfWZ"),
    (468, "u2Zf5hJcMPx1s9mX"),
    (1, "2obeKd6Pak3guDCj"),
    (78, "FfNYByjPK5uJnA3I"),
    (708, "du4o92H0zTP7GaMv"),
    (35, "emMbC1RD8tyUwIhG"),
    (648, "klUySQEsxv3t6Jj2"),
    ]

def play():
    fname_tmmaze = "./tmmaze.so"
    if os.path.exists(fname_tmmaze):
        tmmaze = ctypes.cdll.LoadLibrary(fname_tmmaze)
    else:
        print("\n >>> tmmaze.so is Missing!!! <<<")
        return 0

    curr = "brSuV6Ys4zXkKMmO"
    curr = "Ln7Vm2RgHMQei0WZ"
    curr = "CduYaXnmPk6Hcxjb"


    for k, v in keys:
        # room_no = input("\n >> Enter the Room No. (1 ~ 999):")
        room_no = str(k);
        key = v + curr
        if room_no.isnumeric() and int(room_no) > 0 and int(room_no) < 1000:
            # key = input(" >> Enter the key:")
            room = "Room" + "{:03d}".format(int(room_no))
            decryptedtext = ctypes.create_string_buffer(128)
            if tmmaze[room](key.encode("utf-8"), decryptedtext) == 1:
                room_msg = decryptedtext.value
                print("\n >>> " + room + " Msg: " + room_msg.decode("utf-8") + " <<<")
                break
            else:
                print("\n >>> Wrong Key. Try Again. <<<")
        else:
            print("\n >>> Room No. should be between 1 and 999. <<<")
            play()


def main():
    print("\n  [[[ Welcome to Trend Micro Maze ]]]")
    print("********************************************************************************")
    print("Game Rules:\n")
    print("1. There are 999 rooms in Trend Micro Maze.")
    print("2. Players could go to any room at any time.")
    print("3. Each room has its own specific key.")
    print("4. Players need the right key to open the room and get the secret msg.")
    print("5. Players need to traverse all specific rooms in the correct order.")
    print("6. Room's key is a string with 32 characters.")
    print("7. Room's key only includes lowercase letters, uppercase letters and digits.")
    print("8. The 1st key is {****************Ln7Vm2RgHMQei0WZ}.")
    print("\n ~~ Have Fun. ~~")
    print("********************************************************************************")

    option = ""
    while option != "q":
        print("\n  [[[ Trend Micro Maze Menu ]]]")
        print("========================================")
        print("[p] Enter p to play Trend Micro Maze.")
        print("[q] Enter q to quit.")
        print("========================================\n")

        option = input("> Please eneter your choice: ")
 
        if option == "p" or option == "P":
            play()
        elif option == "q" or option == "Q":
            print("\n >>> Thank you and bye bye. <<<\n")
        else:
            print("\n>>> Couldn't understand your choice. Choose again, please. <<<\n")


if __name__ == "__main__":
    main()
