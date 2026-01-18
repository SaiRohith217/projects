import tkinter as tk
from tkinter import messagebox
import sqlite3

class FantasyCricket:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Cricket Game")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect("fantasy_cricket.db")
        self.cur = self.conn.cursor()

        self.team = []

        self.create_ui()
        self.load_players()

    def create_ui(self):
        tk.Label(self.root, text="Available Players", font=("Arial", 12)).grid(row=0, column=0, padx=10)
        tk.Label(self.root, text="Selected Team", font=("Arial", 12)).grid(row=0, column=2, padx=10)

        self.list_players = tk.Listbox(self.root, width=25, height=15)
        self.list_players.grid(row=1, column=0, padx=10)

        self.list_team = tk.Listbox(self.root, width=25, height=15)
        self.list_team.grid(row=1, column=2, padx=10)

        tk.Button(self.root, text=">>", width=5, command=self.add_player).grid(row=1, column=1)
        tk.Button(self.root, text="<<", width=5, command=self.remove_player).grid(row=2, column=1)

        tk.Button(self.root, text="Save Team", command=self.save_team).grid(row=3, column=0, pady=10)
        tk.Button(self.root, text="Evaluate Score", command=self.evaluate_score).grid(row=3, column=2, pady=10)

    def load_players(self):
        self.list_players.delete(0, tk.END)
        self.cur.execute("SELECT player FROM stats")
        for row in self.cur.fetchall():
            self.list_players.insert(tk.END, row[0])

    def add_player(self):
        try:
            player = self.list_players.get(tk.ACTIVE)
            if len(self.team) >= 11:
                messagebox.showerror("Error", "Only 11 players allowed in a team")
                return
            self.team.append(player)
            self.list_team.insert(tk.END, player)
            self.list_players.delete(tk.ACTIVE)
        except:
            pass

    def remove_player(self):
        try:
            player = self.list_team.get(tk.ACTIVE)
            self.team.remove(player)
            self.list_players.insert(tk.END, player)
            self.list_team.delete(tk.ACTIVE)
        except:
            pass

    def save_team(self):
        if not self.team:
            messagebox.showerror("Error", "No players selected")
            return
        players = ",".join(self.team)
        self.cur.execute("INSERT INTO teams VALUES (?,?,?)",
                         ("MyTeam", players, 100))
        self.conn.commit()
        messagebox.showinfo("Success", "Team saved successfully")

    def evaluate_score(self):
        total_score = 0
        for player in self.team:
            self.cur.execute("SELECT * FROM match WHERE player=?", (player,))
            data = self.cur.fetchone()
            if data:
                runs = data[1]
                fours = data[3]
                sixes = data[4]
                wickets = data[8]
                catches = data[9]
                stumpings = data[10]
                runouts = data[11]

                score = 0
                score += runs // 2
                score += fours
                score += sixes * 2
                score += wickets * 10
                score += (catches + stumpings + runouts) * 10

                total_score += score

        messagebox.showinfo("Final Score", f"Your Fantasy Team Score: {total_score}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyCricket(root)
    root.mainloop()
