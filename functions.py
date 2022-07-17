import cv2 as cv
import numpy as np


def load_gray_blur_picture(picture):
    """
    Takes the original picture, turns it gray and blurs it
    :param picture: Path of the picture with the Escudo
    :return: blurred picture, original picture
    """
    # Load image
    img = cv.imread(picture, 1)

    # Create a copy of the image
    img_original = cv.imread(picture, 1)

    # Convert the image to gray scale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Blur the image
    img = cv.medianBlur(img, 19)

    return img, img_original


def add_numbers_to_coins_ask_user(picture):
    """
    Detects the coins on the picture and adds numbers to them.
    Afterwards the user has to prompt the number of 50 Escudo coin.
    :param picture: Path to original picture
    :return: Dictionary with all relevant information of the coins, blurred picture, original picture
    """
    # Find the circles in the picture
    img, img_original = load_gray_blur_picture(picture)

    # Create a copy
    img_copy = img_original.copy()

    # Find the circles
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 0.9, 120,
                              param1=50, param2=30, minRadius=60, maxRadius=300)

    detected_circles = np.uint16(np.around(circles))

    counter = 1
    adjusted_line_factor = 0.70
    dic_coins = {}

    # Draw the circles and name them
    # Create a dictionary with y, x, r, and brightness of all circles
    for (x, y, r) in detected_circles[0]:
        # Draw rectangle inside of the circle
        adjusted_line_length = round(r * adjusted_line_factor)
        x_plus_y_minus = ((x + adjusted_line_length), (y - adjusted_line_length))
        x_plus_y_plus = ((x + adjusted_line_length), (y + adjusted_line_length))
        x_minus_y_plus = ((x - adjusted_line_length), (y + adjusted_line_length))
        x_minus_y_minus = ((x - adjusted_line_length), (y - adjusted_line_length))

        cv.line(img_original, x_plus_y_minus, x_plus_y_plus, (0, 255, 0), 3)
        cv.line(img_original, x_plus_y_plus, x_minus_y_plus, (0, 255, 0), 3)
        cv.line(img_original, x_minus_y_plus, x_minus_y_minus, (0, 255, 0), 3)
        cv.line(img_original, x_minus_y_minus, x_plus_y_minus, (0, 255, 0), 3)

        # Calculate the average brightness inside of the rectangle
        mean_brightness = round(float(np.mean(img[y - adjusted_line_length:y + adjusted_line_length,
                                              x - adjusted_line_length:x + adjusted_line_length])))

        # Draw the circle
        cv.circle(img_original, (x, y), r, (0, 255, 0), 3)
        cv.circle(img_original, (x, y), 2, (136, 8, 8), 3)

        # Add text to the circle
        cv.putText(img_original, f"Coin {counter}", [x + 2, y - 5], cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 6)

        # Add all relevant information
        dic_coins[str(counter)] = {"x": x, "y": y, "r": r, "mb": mean_brightness}
        counter += 1

    cv.imshow("Image", img_original)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return dic_coins, img_copy, img


def evaluate_escudos(photo_path: str, value_of_one_euro_in_escudo: float):
    """
    Identifies the value of the coins, adds them together and converts them to Euro.
    :param photo_path: Path to the original photo
    :param value_of_one_euro_in_escudo: Exchange Rate Euro -> Escudo as float
    :return: Nothing but show the final picture
    """
    dic_coins, img_copy, img = add_numbers_to_coins_ask_user(photo_path)

    # Ask the user for the number of the reference '50 Escudos'
    user_input = str(input("Which is the number of the 50 Escudo coin?: "))

    # Load values of the 50 Escudos coin as reference
    # reference_x = dic_coins[user_input]["x"]
    # reference_y = dic_coins[user_input]["y"]
    reference_r = dic_coins[user_input]["r"]
    reference_mb = dic_coins[user_input]["mb"]

    # Set the tolerance level
    tolerance = 0.05

    # Tolerance 2 is in case of bigger distances (hence smaller r) in order
    # to distinguish between 50 and 100 Escudos
    tolerance_2 = 0.1

    # radius_five = 0.73
    # Average Brightness of the five Escudos Coin as reference Value
    mb_five = 60
    # Average relative r-length of a ten Escudos coin in relation to r of the 50 Escudos coin
    radius_ten = 0.77
    # Average relative r-length of a twenty Escudos coin in relation to r of the 50 Escudos coin
    radius_twenty = 0.86
    # radius_hundred = 0.97
    # mb_hundred = 74

    amount_escudo = 0
    counter = 1

    for _ in dic_coins:

        if str(counter) == user_input:
            cv.putText(img_copy, "50", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                       cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
            amount_escudo += 50
        elif dic_coins[str(counter)]["mb"] < mb_five * (1 + tolerance):
            cv.putText(img_copy, "5", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                       cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
            amount_escudo += 5
        elif dic_coins[str(counter)]["r"] * (1 - tolerance) < radius_ten * reference_r < \
                dic_coins[str(counter)]["r"] * (1 + tolerance):
            cv.putText(img_copy, "10", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                       cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
            amount_escudo += 10
        elif dic_coins[str(counter)]["r"] * (1 - tolerance) < radius_twenty * reference_r < \
                dic_coins[str(counter)]["r"] * (1 + tolerance):
            cv.putText(img_copy, "20", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                       cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
            amount_escudo += 20
        # Distinguish between 50 and 100 Escudos
        # 1. Check if deviation of r is within a boundary of variable 'tolerance'
        elif dic_coins[str(counter)]["r"] * (1 - tolerance) < reference_r < dic_coins[str(counter)]["r"] * (
                1 + tolerance):
            # 2a. If the radius of the reference 50 Escudos is greater then 200:
            # Check if deviation of mb is within a boundary of variable 'tolerance'
            # If not: label coin as 100 Escudos
            if reference_r > 200:
                if dic_coins[str(counter)]["mb"] * (1 - tolerance) < reference_mb < dic_coins[str(counter)]["mb"] * \
                        (1 + 0.08):
                    cv.putText(img_copy, "50", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                               cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
                    amount_escudo += 50
                else:
                    cv.putText(img_copy, "100", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                               cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
                    amount_escudo += 100
            # 2b. If the radius of the reference 50 Escudos is smaller then 200:
            # Check if deviation of mb is within a boundary of variable 'tolerance_2'
            # If not: label coin as 100 Escudos
            else:
                if dic_coins[str(counter)]["mb"] * (1 - tolerance_2) < reference_mb < dic_coins[str(counter)]["mb"] * \
                        (1 + tolerance_2):
                    cv.putText(img_copy, "50", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                               cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
                    amount_escudo += 50
                else:
                    cv.putText(img_copy, "100", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                               cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
                    amount_escudo += 100

        else:
            cv.putText(img_copy, "100", [dic_coins[str(counter)]["x"] + 2, dic_coins[str(counter)]["y"] - 5],
                       cv.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 10)
            amount_escudo += 100

        counter += 1

    escudo_in_euro = round((float(amount_escudo) / float(value_of_one_euro_in_escudo)), 2)

    cv.putText(img_copy, f"The total amount of Escudos in the picture are ${amount_escudo}",
               [20, 100], cv.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)
    cv.putText(img_copy, f"This are approximately EUR{escudo_in_euro}",
               [20, 220], cv.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)

    cv.imshow("Final_Image", img_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()