import bencodepy
import hashlib

def parse_torrent_file(file_content):
    """Parse un fichier .torrent et retourne les informations"""
    try:
        torrent_data = bencodepy.decode(file_content)
        info = torrent_data[b'info']
        
        # Calculer le hash
        info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()
        
        # Récupérer le nom
        name = info[b'name'].decode('utf-8')
        
        # Calculer la taille
        if b'length' in info:
            size = info[b'length']
        else:
            size = sum(f[b'length'] for f in info[b'files'])
        
        return {
            'name': name,
            'hash': info_hash,
            'size': size
        }
    except Exception as e:
        return None
