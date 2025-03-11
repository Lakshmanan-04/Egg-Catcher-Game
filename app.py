import random
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Egg Catcher Game")
root.resizable(False, False)

# Game settings
canvas_width = 500
canvas_height = 500
egg_width = 30
egg_height = 40
basket_width = 100
basket_height = 50
basket_speed = 20
egg_speed = 5
egg_interval = 2000  # Time interval between egg drops (milliseconds)
difficulty = 0.95  # Decrease interval over time

# Create canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.pack()

# Basket
basket_x = canvas_width // 2 - basket_width // 2
basket_y = canvas_height - basket_height
basket = canvas.create_rectangle(basket_x, basket_y, basket_x + basket_width, basket_y + basket_height, fill="brown")

# Score and Lives
score = 0
lives = 3
score_text = canvas.create_text(50, 20, text=f"Score: {score}", font=("Arial", 14), fill="black")
lives_text = canvas.create_text(450, 20, text=f"Lives: {lives}", font=("Arial", 14), fill="black")

# List to store falling eggs
eggs = []

# Move basket left
def move_left(event):
    x1, y1, x2, y2 = canvas.coords(basket)
    if x1 > 0:
        canvas.move(basket, -basket_speed, 0)

# Move basket right
def move_right(event):
    x1, y1, x2, y2 = canvas.coords(basket)
    if x2 < canvas_width:
        canvas.move(basket, basket_speed, 0)

# Drop eggs
def drop_egg():
    x = random.randint(10, canvas_width - 10 - egg_width)
    egg = canvas.create_oval(x, 10, x + egg_width, 10 + egg_height, fill="red")
    eggs.append(egg)
    move_egg(egg)

    # Speed up game over time
    global egg_interval
    egg_interval = int(egg_interval * difficulty)
    root.after(egg_interval, drop_egg)

# Move eggs down
def move_egg(egg):
    if egg in canvas.find_all():
        canvas.move(egg, 0, egg_speed)
        x1, y1, x2, y2 = canvas.coords(egg)

        # Check if egg is caught
        bx1, by1, bx2, by2 = canvas.coords(basket)
        if by1 < y2 < by2 and bx1 < x1 < bx2:
            global score
            score += 10
            canvas.delete(egg)
            eggs.remove(egg)
            canvas.itemconfig(score_text, text=f"Score: {score}")

        # Check if egg missed
        elif y2 < canvas_height:
            root.after(50, lambda: move_egg(egg))
        else:
            global lives
            lives -= 1
            canvas.delete(egg)
            eggs.remove(egg)
            canvas.itemconfig(lives_text, text=f"Lives: {lives}")

            if lives == 0:
                canvas.create_text(canvas_width//2, canvas_height//2, text="Game Over", font=("Arial", 24), fill="red")
                return

# Key bindings (Use 'bind_all' instead of 'bind' to work on the whole window)
root.bind_all("<Left>", move_left)
root.bind_all("<Right>", move_right)

# Start game
drop_egg()
root.mainloop()
