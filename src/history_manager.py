import json
import os
import datetime

class HistoryManager:
    def __init__(self, filename='history.json'):
        self.filename = filename
        
        # --- YENİ EKLENEN KISIM: BAŞLANGIÇTA TEMİZLE ---
        # Program her açıldığında dosyayı sıfırla
        with open(self.filename, 'w') as f:
            json.dump([], f)
        print("History cleared on startup.")
        # -----------------------------------------------

    def save_path(self, algorithm_name, path_points):
        # Veriyi hazırla
        serializable_path = [(p.x, p.y) for p in path_points]
        
        entry = {
            "algorithm": algorithm_name,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"), # Sadece saat yeterli
            "path": serializable_path
        }

        # Mevcut veriyi oku
        data = self.load_history()

        # Yeni veriyi ekle
        data.append(entry)

        # Dosyaya yaz
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Path saved to history! (Total: {len(data)})")

    def load_history(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []