import typing as t

from nicegui import ui


class Field(ui.element):
    def __init__(self, click, index: int):
        super().__init__("div")
        self.click = click  # ボタンのクリック用
        self.index = index  # ボタンの番号

    def build(self, value: t.Literal["X", "O", ""]):
        self.clear()  # 子要素をクリア
        self.value = value
        with self:
            # 値があるときはアイコンを、ないときはボタンを表示
            if self.value:
                name = "close" if self.value == "X" else "radio_button_unchecked"
                color = "red" if self.value == "X" else "indigo-4"
                self.icon = ui.icon(name, size="3em", color=color).classes("size-10")
            else:
                ui.button(str(self.index), on_click=self.click).classes("rounded-xl size-10 bg-cyan-2")


class Main:
    def __init__(self):
        with ui.column().style("margin: 0 auto"):
            self.fields = []  # 9つのFieldのリスト
            # メッセージ(self.messageにバインド)
            ui.label("").bind_text(self, "message").classes("text-4xl")
            with ui.card().classes("bg-cyan-1"):
                for i in range(3):
                    with ui.row():
                        self.fields.extend([Field(self.click, i * 3 + j) for j in range(3)])
            ui.button("reset", icon="refresh", on_click=self.reset).props("flat")
            self.reset()  # 画面の初期化

    def reset(self):
        self.player: t.Literal["X", "O", ""] = "X"
        self.message = f"{self.player}'s turn"
        for field in self.fields:
            field.build("")  # Fieldの再作成

    def click(self, event):
        if "won" not in self.message:
            self.fields[int(event.sender.text)].build(self.player)
            self.player = "X" if self.player == "O" else "O"
            self.set_message()

    def set_message(self):
        for combination in [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]:
            values = "".join(self.fields[i].value for i in combination)
            if values in {"OOO", "XXX"}:
                self.message = f"{values[0]} has won!"
                for i in range(9):
                    if i not in combination and hasattr(self.fields[i], "icon"):
                        self.fields[i].icon.classes("opacity-20")  # 揃ってないアイコンを薄くする
                break
        else:
            if all(field.value for field in self.fields):
                self.message = "draw"
            else:
                self.message = f"{self.player}'s turn"


def main(*, reload=False, port=8101):
    Main()
    ui.run(title="TicTacToe", reload=reload, port=port)
