
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Application")
        self.root.geometry("600x500")
        self.root.configure(bg='red')
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Load existing notes
        self.load_notes()
    
    def init_database(self):
        """Initialize SQLite database"""
        self.db_path = "notes.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create notes table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="My Notes", 
            font=("Arial", 18, "bold"),
            bg='red',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='red')
        input_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Note entry
        tk.Label(
            input_frame, 
            text="Enter your note:", 
            font=("Arial", 12),
            bg='red',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.note_entry = tk.Text(
            input_frame, 
            height=3, 
            width=50, 
            font=("Arial", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.note_entry.pack(fill=tk.X, pady=5)
        
        # Add button
        self.add_button = tk.Button(
            input_frame,
            text="Add Note",
            command=self.add_note,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.add_button.pack(pady=5)
        
        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Notes display area
        notes_label = tk.Label(
            self.root, 
            text="Your Notes:", 
            font=("Arial", 14, "bold"),
            bg='red',
            fg='white'
        )
        notes_label.pack(anchor=tk.W, padx=20)
        
        # Scrollable frame for notes
        self.create_scrollable_frame()
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for notes"""
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.root, bg='red', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='red')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def add_note(self):
        """Add a new note to the database and display"""
        note_content = self.note_entry.get("1.0", tk.END).strip()
        
        if not note_content:
            messagebox.showwarning("Warning", "Please enter a note before adding!")
            return
        
        try:
            # Insert note into database
            self.cursor.execute("INSERT INTO notes (content) VALUES (?)", (note_content,))
            self.conn.commit()
            
            # Clear the entry field
            self.note_entry.delete("1.0", tk.END)
            
            # Reload notes to display the new one
            self.load_notes()
            
            # Show success message
            messagebox.showinfo("Success", "Note added successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding note: {e}")
    
    def delete_note(self, note_id):
        """Delete a note from the database"""
        try:
            # Confirm deletion
            result = messagebox.askyesno(
                "Confirm Delete", 
                "Are you sure you want to delete this note?"
            )
            
            if result:
                # Delete from database
                self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                self.conn.commit()
                
                # Reload notes
                self.load_notes()
                
                messagebox.showinfo("Success", "Note deleted successfully!")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting note: {e}")
    
    def load_notes(self):
        """Load and display all notes from database"""
        # Clear existing notes display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            # Fetch all notes from database
            self.cursor.execute("SELECT id, content, created_at FROM notes ORDER BY created_at DESC")
            notes = self.cursor.fetchall()
            
            if not notes:
                # Display message when no notes exist
                no_notes_label = tk.Label(
                    self.scrollable_frame,
                    text="No notes yet. Add your first note above!",
                    font=("Arial", 12),
                    fg='white',
                    bg='red'
                )
                no_notes_label.pack(pady=20)
                return
            
            # Display each note
            for i, (note_id, content, created_at) in enumerate(notes):
                self.create_note_widget(note_id, content, created_at, i)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading notes: {e}")
    
    def create_note_widget(self, note_id, content, created_at, index):
        """Create a widget for displaying a single note"""
        # Note frame
        note_frame = tk.Frame(
            self.scrollable_frame,
            bg='white',
            relief=tk.SOLID,
            borderwidth=1
        )
        note_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Note header with timestamp and delete button
        header_frame = tk.Frame(note_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Timestamp
        timestamp_label = tk.Label(
            header_frame,
            text=f"Created: {created_at}",
            font=("Arial", 9),
            fg='#666',
            bg='white'
        )
        timestamp_label.pack(side=tk.LEFT)
        
        # Delete button
        delete_button = tk.Button(
            header_frame,
            text="Delete",
            command=lambda: self.delete_note(note_id),
            bg='#f44336',
            fg='white',
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        delete_button.pack(side=tk.RIGHT)
        
        # Note content
        content_label = tk.Label(
            note_frame,
            text=content,
            font=("Arial", 11),
            bg='white',
            fg='#333',
            wraplength=500,
            justify=tk.LEFT
        )
        content_label.pack(fill=tk.X, padx=10, pady=(0, 10), anchor=tk.W)
    
    def on_closing(self):
        """Handle application closing"""
        self.conn.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = NotesApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()


