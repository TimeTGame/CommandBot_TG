import os

EXTENTIONS = {
            # Scripts and exe
            '.exe': '🖥️', '.msi': '📦', '.bat': '⚙️', '.cmd': '⚙️', 
            '.ps1': '⚙️', '.sh': '🐧', '.bash': '🐧', '.py': '🐍',
            
            # Web
            '.html': '🌐', '.htm': '🌐', '.css': '🎨', '.js': '🟨',
            '.ts': '🔷', '.php': '🐘', '.json': '📋', '.xml': '📋',
            
            # programming
            '.java': '☕', '.cpp': '⚙️', '.c': '⚙️', '.h': '⚙️',
            '.cs': '🔷', '.go': '🐹', '.rs': '🦀', '.rb': '💎',
            
            # docs and txt
            '.txt': '📝', '.md': '📄', '.doc': '📘', '.docx': '📘',
            '.pdf': '📕', '.rtf': '📄', '.tex': '📜',
            
            # tables and presentations
            '.xls': '📗', '.xlsx': '📗', '.csv': '📊', '.pptx': '🎤',
            
            # Pics
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.bmp': '🖼️',
            '.svg': '🖼️', '.ico': '🖼️', '.psd': '🎨', '.ai': '✏️',
            
            # Video and audio
            '.mp4': '🎥', '.avi': '🎥', '.mkv': '🎬', '.mp3': '🎵',
            '.wav': '🎵', '.flac': '🎵', '.ogg': '🎵',
            
            # Archives
            '.zip': '📦', '.rar': '📦', '.tar': '📦', '.7z': '🗜️',
            '.gz': '🗜️',
            
            # Databases and logs
            '.db': '🗄️', '.sql': '🗄️', '.dbf': '🗄️', '.log': '📰',
            
            # config a and systems files
            '.ini': '🎛️', '.conf': '🎛️', '.cfg': '🎛️', '.yml': '⚙️',
            '.yaml': '⚙️', '.reg': '📑', '.dll': '🧩',
            
            # Special
            '.torrent': '🌊', '.vcf': '👤', '.ics': '🗓️', '.pem': '🔑',
            '.key': '🔑', '.crt': '📜', '.iso': '📀', '.dockerfile': '🐳'
        }

def get_icon(filename):
        if os.path.isdir(filename):
            return "📁"
        
        ext = os.path.splitext(filename)[1].lower()
        return EXTENTIONS.get(ext, '📎')