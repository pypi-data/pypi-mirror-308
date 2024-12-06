"""
mtqdm - A macOS menu bar progress indicator for tqdm.

This module provides a drop-in replacement for tqdm that adds a menu bar
progress indicator in addition to the standard console output.

Example:
    from mtqdm import mtqdm
    
    for i in mtqdm(range(100)):
        # Your processing here
        time.sleep(0.1)
"""

from tqdm import tqdm
import rumps
import multiprocessing
from enum import Enum

def run_app(queue):
    """
    Run the menu bar app in a separate process.
    Updates the title based on messages received from the queue.
    
    Args:
        queue: multiprocessing.Queue for receiving title updates
    """
    app = rumps.App("✶")
    metrics = {}

    @rumps.timer(0.1)
    def update_title(_):
        if not queue.empty():
            data = queue.get()
            if isinstance(data, tuple) and data[0] == "MODE":
                # Handle mode change request
                queue.put(data)  # Send mode change back to main process
            elif isinstance(data, dict):
                metrics.update(data)
                update_menu()
            elif data == "QUIT":
                app.title = "✶ DONE ✶"
            else:
                app.title = data

    def format_rate(rate):
        """Format the iteration rate with proper units."""
        if rate is None:
            return "..."
        return f"{rate:.2f} it/s"

    def format_time(time_value):
        """Format time values with proper handling of edge cases."""
        if time_value is None or time_value == 'N/A':
            return "..."
        return str(time_value)

    def update_menu():
        """Update the menu with current metrics and mode options."""
        app.menu.clear()
        if metrics:
            # Create non-clickable menu items for metrics
            progress = rumps.MenuItem(f"Progress: {metrics.get('percentage', 0):.1f}%", callback=None)
            elapsed = rumps.MenuItem(f"Elapsed: {format_time(metrics.get('elapsed'))}", callback=None)
            remaining = rumps.MenuItem(f"Remaining: {format_time(metrics.get('remaining'))}", callback=None)
            rate = rumps.MenuItem(f"Rate: {format_rate(metrics.get('rate'))}", callback=None)
            
            # Create display mode menu
            display_menu = rumps.MenuItem('Display Mode')
            percentage = rumps.MenuItem('Percentage', 
                callback=lambda _: queue.put(("MODE", "PERCENTAGE")))
            bar = rumps.MenuItem('Progress Bar', 
                callback=lambda _: queue.put(("MODE", "BAR")))
            time_display = rumps.MenuItem('Time', 
                callback=lambda _: queue.put(("MODE", "TIME")))
            
            # Set checkmarks for current mode
            percentage.state = 1 if metrics.get('current_mode') == "PERCENTAGE" else 0
            bar.state = 1 if metrics.get('current_mode') == "BAR" else 0
            time_display.state = 1 if metrics.get('current_mode') == "TIME" else 0
            
            display_menu.update([percentage, bar, time_display])
            
            # Build the menu with proper order and separators
            app.menu = [
                progress,
                elapsed,
                remaining,
                rate,
                rumps.separator,  # Add separator before Display Mode
                display_menu
            ]

    app.run()

class mtqdm(tqdm):
    """
    A tqdm-compatible progress bar that also displays progress in the macOS menu bar.
    
    Display Modes:
        DISPLAY_PERCENTAGE: Shows percentage complete
        DISPLAY_BAR: Shows a graphical progress bar
        DISPLAY_TIME: Shows elapsed/remaining time
        
    Example:
        >>> for i in mtqdm(range(100), display_mode=mtqdm.DisplayMode.BAR):
        ...     time.sleep(0.1)
    """
    
    # Display modes
    class DisplayMode(Enum):
        PERCENTAGE = "PERCENTAGE"
        BAR = "BAR"
        TIME = "TIME"

    # Class-level variables for the menu bar app process
    _process = None
    _queue = None
    _cleanup_registered = False

    @classmethod
    def _setup_app(cls):
        """Initialize the menu bar app process if it's not already running."""
        if cls._process is None:
            cls._queue = multiprocessing.Queue()
            cls._process = multiprocessing.Process(target=run_app, args=(cls._queue,))
            cls._process.start()
            
            # Register cleanup handler if not already registered
            if not cls._cleanup_registered:
                import atexit
                atexit.register(cls._shutdown)
                cls._cleanup_registered = True

    def __init__(self, *args, display_mode=DisplayMode.PERCENTAGE, **kwargs):
        """
        Initialize the progress bar.
        
        Args:
            *args: Arguments to pass to tqdm
            display_mode: How to display progress in the menu bar
            **kwargs: Keyword arguments to pass to tqdm
        """
        super().__init__(*args, **kwargs)
        self.display_mode = display_mode
        self._setup_app()
        self.update_menu_bar()

    def update_menu_bar(self):
        """Update the menu bar title and metrics."""
        title = self._get_title_for_mode()
        self._queue.put(title)
        
        # Calculate remaining time using tqdm's internal methods
        remaining = None
        if self.n > 0:  # Only calculate if we have started iterating
            # Use tqdm's internal calculation method
            remaining = (self.total - self.n) / self.format_dict['rate'] if self.format_dict.get('rate') else None
        
        # Format times using tqdm's format_dict for consistency
        elapsed_str = self.format_dict.get('elapsed_str', '00:00')
        if remaining is not None:
            remaining_str = self.format_interval(remaining)
        else:
            remaining_str = '...'
        
        # Send metrics update
        metrics = {
            'percentage': 100 * self.n / self.total,
            'elapsed': elapsed_str,
            'remaining': remaining_str,
            'rate': self.format_dict.get('rate', None),
            'current_mode': self.display_mode.value
        }
        self._queue.put(metrics)

    def _get_title_for_mode(self):
        """Generate the appropriate title string based on the display mode."""
        if self.display_mode == self.DisplayMode.PERCENTAGE:
            return self._get_percentage_title()
        elif self.display_mode == self.DisplayMode.BAR:
            return self._get_bar_title()
        elif self.display_mode == self.DisplayMode.TIME:
            return self._get_time_title()

    def _get_percentage_title(self):
        """Generate a percentage-based title."""
        progress_percentage = int(self.n / self.total * 100)
        return f"✶ {progress_percentage:3d}% ✶"

    def _get_bar_title(self):
        """Generate a graphical progress bar title."""
        bar_length = 6  # Smaller bar length for menu bar
        filled_length = int(bar_length * self.n // self.total)
        bar = '♥' * filled_length + '♡' * (bar_length - filled_length)
        return f"✶ {bar} ✶"

    def _get_time_title(self):
        """Generate a time-based title."""
        elapsed = self.format_interval(self.format_dict['elapsed'])
        
        # Calculate remaining time
        remaining = None
        if self.n > 0:  # Only calculate if we have started iterating
            remaining = (self.total - self.n) / self.format_dict['rate'] if self.format_dict.get('rate') else None
            
        remaining_str = self.format_interval(remaining) if remaining is not None else '...'
        return f"✶ {elapsed} / {remaining_str} ✶"

    def update(self, n=1):
        """Update progress and refresh the menu bar display."""
        super().update(n)
        # Check for mode changes
        while not self._queue.empty():
            msg = self._queue.get()
            if isinstance(msg, tuple) and msg[0] == "MODE":
                self.display_mode = self.DisplayMode(msg[1])
        self.update_menu_bar()

    def handle_mode_change(self, new_mode):
        """Handle mode change requests from the menu."""
        self.display_mode = self.DisplayMode(new_mode)
        self.update_menu_bar()

    def close(self):
        """Clean up resources when the progress bar is closed."""
        super().close()
        self._cleanup_process()

    def _cleanup_process(self):
        """Terminate the menu bar app process."""
        if self._process is not None:
            self._queue.put("QUIT")
            self._process.join(timeout=1)
            if self._process.is_alive():
                self._process.terminate()

    @classmethod
    def _shutdown(cls):
        """Class method to shut down the menu bar app process."""
        if cls._process is not None:
            cls._queue.put("QUIT")
            cls._process.join(timeout=1)
            if cls._process.is_alive():
                cls._process.terminate()
