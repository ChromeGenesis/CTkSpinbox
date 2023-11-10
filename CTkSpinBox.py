import customtkinter
from typing import Callable

class Spinbox(customtkinter.CTkFrame):
    def __init__(
            self,
            master: customtkinter.CTk,
            width: int = 100,
            height: int = 32,
            step_size: int | float = 1,
            font: tuple = ('Arial', 12),
            command: Callable = None,
            **kwargs
        ):
        super().__init__(master=master, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.font = font
        self._step_type: float | int = int
        if isinstance(step_size, float):
            self._step_type = float

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(
            self, 
            text="-", 
            font=self.font,
            width=height-6, 
            height=height-6,
            command=self.subtract_button_callback
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(
            self, 
            font=self.font,
            width=width-(2*height), 
            height=height-6, 
            border_width=0
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.entry.configure(validate="key", validatecommand=(self.register(self.validate_entry), "%P"))

        self.add_button = customtkinter.CTkButton(
            self, 
            text="+", 
            font=self.font,
            width=height-6, 
            height=height-6,
            command=self.add_button_callback
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "1" if self._step_type is int else "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        
        value = self._step_type(self.entry.get()) + self.step_size
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        
        value = self._step_type(self.entry.get()) - self.step_size
        if value < 1:
            value = 1
        self.entry.delete(0, "end")
        self.entry.insert(0, value)

    def get(self) -> int | float:
        return self._step_type(self.entry.get())

    def set(self, value: int | float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(self._step_type(value)))
    
    def validate_entry(self, P: str):
        if P == "":
            return True
        
        try:
            self._step_type(P)
            return True
        except ValueError:
            return False