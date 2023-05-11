# Definition of a Button class
class Button:
    def __init__(self, x1, x2, y1, y2):
        # Initialize the button's properties with the provided coordinates
        self.left_side = x1
        self.right_side = x2
        self.top_side = y1
        self.bottom_side = y2

    def is_clicked(self, mouse_position):
        # Check if the provided mouse position is inside the borders of the button
        return self.left_side < mouse_position[0] < self.right_side \
            and self.top_side < mouse_position[1] < self.bottom_side
