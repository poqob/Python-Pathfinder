import json
import os
import datetime

class HistoryManager:
    def __init__(self, filename='assets/history.json'):
        self.filename = filename

    def save_path(self, algorithm_name, path_points):
        """
        Rottayı JSON dosyasına ekler.
        path_points: Vector2 listesi gelir, bunu list of tuples'a çeviririz.
        """
        # Veriyi hazırla
        serializable_path = [(p.x, p.y) for p in path_points]
        
        entry = {
            "algorithm": algorithm_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "path": serializable_path
        }

        # Mevcut veriyi oku
        data = []
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []

        # Yeni veriyi ekle
        data.append(entry)

        # Dosyaya yaz
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Path saved to history! (Total: {len(data)})")

    def load_history(self):
        """Tüm geçmişi döndürür."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []