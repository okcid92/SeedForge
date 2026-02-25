import libtorrent as lt
import time
import os

class TorrentManager:
    def __init__(self, download_path='downloads'):
        self.session = lt.session()
        self.session.listen_on(6881, 6891)
        self.download_path = download_path
        self.handles = {}
        
        if not os.path.exists(download_path):
            os.makedirs(download_path)
    
    def add_torrent(self, torrent_file_path, torrent_hash):
        """Ajoute un torrent et commence le téléchargement"""
        info = lt.torrent_info(torrent_file_path)
        params = lt.add_torrent_params()
        params.ti = info
        params.save_path = self.download_path
        handle = self.session.add_torrent(params)
        self.handles[torrent_hash] = handle
        return handle
    
    def add_magnet(self, magnet_link, torrent_hash):
        """Ajoute un magnet link"""
        params = lt.parse_magnet_uri(magnet_link)
        params.save_path = self.download_path
        handle = self.session.add_torrent(params)
        self.handles[torrent_hash] = handle
        return handle
    
    def get_status(self, torrent_hash):
        """Récupère le statut d'un torrent"""
        if torrent_hash not in self.handles:
            return None
        
        handle = self.handles[torrent_hash]
        status = handle.status()
        
        return {
            'progress': status.progress * 100,
            'download_rate': status.download_rate / 1000,  # KB/s
            'upload_rate': status.upload_rate / 1000,  # KB/s
            'num_seeds': status.num_seeds,
            'num_peers': status.num_peers,
            'state': str(status.state),
            'total_download': status.total_download,
            'total_upload': status.total_upload
        }
    
    def pause_torrent(self, torrent_hash):
        """Met en pause un torrent"""
        if torrent_hash in self.handles:
            self.handles[torrent_hash].pause()
    
    def resume_torrent(self, torrent_hash):
        """Reprend un torrent"""
        if torrent_hash in self.handles:
            self.handles[torrent_hash].resume()
    
    def remove_torrent(self, torrent_hash, delete_files=False):
        """Supprime un torrent"""
        if torrent_hash in self.handles:
            if delete_files:
                self.session.remove_torrent(self.handles[torrent_hash], lt.options_t.delete_files)
            else:
                self.session.remove_torrent(self.handles[torrent_hash])
            del self.handles[torrent_hash]

    def load_torrents_from_db(self):
        """Charge les torrents depuis la base de données au démarrage."""
        from app.models.torrent import Torrent
        print("Chargement des torrents depuis la base de données...")
        torrents = Torrent.query.filter(Torrent.status != 'completed').all()
        for torrent in torrents:
            magnet_link = f"magnet:?xt=urn:btih:{torrent.hash}&dn={torrent.name}"
            try:
                self.add_magnet(magnet_link, torrent.hash)
                print(f"Torrent '{torrent.name}' re-chargé.")
                # Si le torrent était en pause, on le met en pause dans libtorrent aussi
                if torrent.status == 'paused':
                    self.pause_torrent(torrent.hash)
            except Exception as e:
                print(f"Erreur en re-chargeant le torrent {torrent.name}: {e}")

# Instance globale
torrent_manager = TorrentManager()
