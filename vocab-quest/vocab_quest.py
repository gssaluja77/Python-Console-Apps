# Vocab Builder Game with Rich TUI

import random
from words import word_map, word_list
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align
from rich import box
from rich.columns import Columns

console = Console()

styles = {
    "success": ("✅", "bold green4"),
    "error": ("❌", "bold red3"),
    "warning": ("⚠️ ", "bold dark_orange"),
    "info": ("ℹ️ ", "bold blue3"),
    "celebration": ("🎉", "bold magenta3"),
}


def display_title():
    """Display beautiful title banner"""
    title = Text("🎓 VOCAB QUEST 🎓", style="bold purple4")
    subtitle = Text("Master Your Vocabulary!", style="italic blue3")

    title_panel = Panel(
        Align.center(f"{title}\n{subtitle}"),
        border_style="blue3",
        box=box.DOUBLE,
        padding=(1, 2),
    )
    console.print(title_panel)


def display_progress(remaining_attempts, total_attempts, words_completed, total_words):
    """Display game progress with visual indicators"""
    # Attempts progress
    attempts_text = f"[blue3]Attempts:[/blue3] [dark_orange]{remaining_attempts}[/dark_orange] / {total_attempts}"

    # Words progress
    words_text = f"[blue3]Words Mastered:[/blue3] [green4]{words_completed}[/green4] / {total_words}"

    # Create columns for side-by-side display
    columns = Columns([attempts_text, words_text], equal=True, expand=True)
    console.print(Panel(columns, border_style="dim", padding=(0, 1)))


def display_word_state(word_state, used_letters):
    """Display current word state with styling"""
    # Display the word with nice spacing
    word_display = " ".join(
        [
            (
                f"[bold blue3]{char}[/bold blue3]"
                if char != "_"
                else "[dim black]_[/dim black]"
            )
            for char in word_state
        ]
    )

    # Create table for word display
    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="blue3",
        padding=(1, 2),
    )
    table.add_row(Align.center(word_display))
    console.print(table)

    # Display used letters if any
    if used_letters:
        used_display = ", ".join(
            [
                (
                    f"[red3]{letter}[/red3]"
                    if letter not in "".join(word_state)
                    else f"[green4]{letter}[/green4]"
                )
                for letter in sorted(used_letters)
            ]
        )
        console.print(f"[dim]Used letters: {used_display}[/dim]")


def display_hint(hint):
    """Display hint in a beautiful panel"""
    hint_panel = Panel(
        f"💡 [bold dark_orange]{hint}[/bold dark_orange]",
        title="[bold purple4]Hint[/bold purple4]",
        border_style="dark_orange",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(hint_panel)


def display_message(message, style="info"):
    """Display feedback messages with appropriate styling"""
    icon, text_style = styles.get(style, styles["info"])
    console.print(f"{icon} [{text_style}]{message}[/{text_style}]")


def play_game():
    """Main game loop"""
    # Clear the screen for a clean start
    console.clear()

    max_words = len(word_list)
    random.shuffle(word_list)
    total_attempts = 6
    words_completed = 0

    display_title()
    console.print()

    while word_list:
        remaining_attempts = total_attempts
        random_word = word_list.pop()

        console.rule("[bold blue3]New Word Challenge[/bold blue3]", style="blue3")
        console.print()

        # Display progress
        display_progress(remaining_attempts, total_attempts, words_completed, max_words)
        console.print()

        # Display hint
        display_hint(word_map[random_word])
        console.print()

        # Initialize game state
        word_state = ["_"] * len(random_word)
        used_letters = []
        guessed = False

        # Display initial word state
        display_word_state(word_state, used_letters)
        console.print()

        # Game loop for current word
        while remaining_attempts > 0:
            # Get user input
            guess = Prompt.ask(
                "[bold blue1]Guess a letter (or type the full word)[/bold blue1]"
            ).lower()
            console.print()

            # Validate input
            if not guess.isalpha():
                display_message("Please enter only letters!", "warning")
                console.print()
                continue

            # Check if single letter
            if len(guess) == 1:
                if guess in used_letters:
                    display_message("You've already tried this letter!", "warning")
                    console.print()
                    continue

                used_letters.append(guess)

                # Check if letter is in word
                if guess in random_word:
                    # Update word state
                    for i in range(len(random_word)):
                        if random_word[i] == guess:
                            word_state[i] = guess

                    display_message(f"Great! '{guess}' is in the word!", "success")
                    display_message(
                        f"Attempts remaining: {remaining_attempts}", "warning"
                    )
                    console.print()
                    display_word_state(word_state, used_letters)
                    console.print()

                    # Check if word is complete
                    if "_" not in word_state:
                        guessed = True
                        break
                else:
                    remaining_attempts -= 1
                    display_message(f"Sorry, '{guess}' is not in the word!", "error")
                    display_message(
                        f"Attempts remaining: {remaining_attempts}", "warning"
                    )
                    console.print()
                    display_word_state(word_state, used_letters)
                    console.print()

            # Check if full word guess
            elif guess == random_word:
                guessed = True
                word_state = list(random_word)
                break
            else:
                display_message(f"'{guess}' is not the correct word!", "error")
                console.print()

        # Display result
        console.print()
        if guessed or "_" not in word_state:
            display_message(
                f"🎊 Awesome! You've mastered '{random_word}'!", "celebration"
            )
            words_completed += 1
        else:
            display_message(
                f"Game Over! You used all {total_attempts} attempts.", "error"
            )
            display_message(f"The word was: '{random_word}'", "info")

        console.print()

        # Check if all words completed
        if not word_list:
            console.print()
            victory_text = Text(f"🏆 CONGRATULATIONS! 🏆", style="bold dark_orange")
            victory_msg = Text(
                f"You've mastered all {max_words} words in our database!",
                style="bold green4",
            )

            victory_panel = Panel(
                Align.center(
                    f"{victory_text}\n\n{victory_msg}\n\n[blue3]We'll be adding more words for you soon![/blue3]"
                ),
                border_style="dark_orange",
                box=box.DOUBLE,
                padding=(2, 4),
            )
            console.print(victory_panel)
            break

        # Ask to continue
        console.rule(style="dim")
        if not Confirm.ask(
            "[bold dodger_blue1]🎮 Ready for the next word?[/bold dodger_blue1]",
            default=True,
        ):
            console.print()
            goodbye_panel = Panel(
                Align.center(
                    "[bold dark_orange]👋 Thanks for playing! Keep learning! 📚[/bold dark_orange]"
                ),
                border_style="purple4",
                padding=(1, 2),
            )
            console.print(goodbye_panel)
            break

        console.print()


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        console.print()
        console.print()
        goodbye_panel = Panel(
            Align.center(
                "[bold dark_orange]👋 Thanks for playing! Keep learning! 📚[/bold dark_orange]"
            ),
            border_style="purple4",
            padding=(1, 2),
        )
        console.print(goodbye_panel)
