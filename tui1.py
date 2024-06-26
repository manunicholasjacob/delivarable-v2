import curses
import sbr
import device_control

def main(stdscr):
    curses.echo()

    # Colors and border setup
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    stdscr.bkgd(curses.color_pair(1))

    # Function to display a box with a title
    def display_box(window, y, x, height, width, title=""):
        window.attron(curses.color_pair(2))
        window.border(0)
        window.addstr(0, 2, f' {title} ')
        window.attroff(curses.color_pair(2))
        window.refresh()

    # Display available slot numbers
    slot_numbers = sbr.get_slot_numbers()
    height = max(len(slot_numbers) + 4, 10)
    slot_window = curses.newwin(height, 40, 1, 1)
    display_box(slot_window, 1, 1, height, 40, "Available Slot Numbers")
    for i, slot in enumerate(slot_numbers):
        slot_window.addstr(i + 2, 2, slot)
    slot_window.refresh()

    # Collect user inputs
    input_window = curses.newwin(15, 60, height + 2, 1)
    display_box(input_window, height + 2, 1, 15, 60, "User Inputs")

    input_window.addstr(2, 2, "Enter your password (sudo access): ")
    user_password = input_window.getstr().decode()

    input_window.addstr(4, 2, "Number of Loops: ")
    inputnum_loops = int(input_window.getstr().decode())

    input_window.addstr(6, 2, "Do you want to kill on error? (y/n): ")
    kill = input_window.getstr().decode()

    input_window.addstr(8, 2, "Choose slot numbers to test (comma separated): ")
    slot_input = input_window.getstr().decode()
    slotlist = list(map(int, slot_input.split(',')))

    input_window.clear()
    display_box(input_window, height + 2, 1, 15, 60, "Test Parameters")
    input_window.addstr(2, 2, f"Password: {'*' * len(user_password)}")
    input_window.addstr(4, 2, f"Number of Loops: {inputnum_loops}")
    input_window.addstr(6, 2, f"Kill on error: {kill}")
    input_window.addstr(8, 2, f"Slot numbers to test: {slotlist}")
    input_window.addstr(12, 2, "Press any key to start the test...")
    input_window.refresh()
    input_window.getch()

    # Set error reporting to 0
    device_window = curses.newwin(10, 60, height + 17, 1)
    display_box(device_window, height + 17, 1, 10, 60, "Device Control Status")
    device_window.addstr(2, 2, "Setting error reporting to 0...")
    device_window.refresh()

    bdfs = device_control.get_all_bdfs()
    device_control.store_original_values(bdfs)
    device_control.process_bdfs(bdfs)

    device_window.addstr(4, 2, "Error reporting set to 0.")
    device_window.refresh()

    # Run the sbr functionality
    sbr_window = curses.newwin(10, 60, height + 28, 1)
    display_box(sbr_window, height + 28, 1, 10, 60, "SBR Test Status")
    sbr_window.addstr(2, 2, "Running SBR tests...")
    sbr_window.refresh()

    sbr.run_test(stdscr, user_password, inputnum_loops, kill, slotlist)

    sbr_window.addstr(4, 2, "SBR tests completed.")
    sbr_window.refresh()

    # Reset device control registers to original values
    device_window.addstr(6, 2, "Resetting device control registers...")
    device_window.refresh()

    device_control.reset_to_original_values()

    device_window.addstr(8, 2, "Device control registers reset to original values.")
    device_window.refresh()

    # Display completion message
    stdscr.clear()
    display_box(stdscr, 1, 1, 3, 60, "Test Completed")
    stdscr.addstr(2, 2, "Test completed. Check the output.txt file for results.")
    stdscr.refresh()
    stdscr.getch()  # Wait for a key press to keep the interface open

curses.wrapper(main)
